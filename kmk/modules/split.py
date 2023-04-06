'''Enables splitting keyboards wirelessly or wired'''
import busio
from micropython import const
from supervisor import runtime, ticks_ms

from keypad import Event as KeyEvent
from storage import getmount

from kmk.hid import HIDModes
from kmk.kmktime import check_deadline
from kmk.modules import Module


class SplitSide:
    LEFT = const(1)
    RIGHT = const(2)


class SplitType:
    UART = const(1)
    I2C = const(2)  # unused
    ONEWIRE = const(3)  # unused
    BLE = const(4)


class Split(Module):
    '''Enables splitting keyboards wirelessly, or wired'''

    def __init__(
        self,
        split_flip=True,
        split_side=None,
        split_type=SplitType.UART,
        split_target_left=True,
        uart_interval=20,
        data_pin=None,
        data_pin2=None,
        uart_flip=True,
        use_pio=False,
        debug_enabled=False,
    ):
        self._is_target = True
        self._uart_buffer = bytearray([])
        self._uart_to_read = 0
        self._uart_receiving_msg_type = None
        self.split_flip = split_flip
        self.split_side = split_side
        self.split_type = split_type
        self.split_target_left = split_target_left
        self.split_offset = None
        self.data_pin = data_pin
        self.data_pin2 = data_pin2
        self.uart_flip = uart_flip
        self._use_pio = use_pio
        self._uart = None
        self._uart_interval = uart_interval
        self._debug_enabled = debug_enabled
        self.uart_header = 0xB2  # Any non-zero byte should work
        self._msg_receivers = {}
        self.add_receiver(self.uart_header, self._receive_msg)

        if self.split_type == SplitType.BLE:
            try:
                from adafruit_ble import BLERadio
                from adafruit_ble.advertising.standard import (
                    ProvideServicesAdvertisement,
                )
                from adafruit_ble.services.nordic import UARTService

                self.BLERadio = BLERadio
                self.ProvideServicesAdvertisement = ProvideServicesAdvertisement
                self.UARTService = UARTService
            except ImportError:
                print('BLE Import error')
                return  # BLE isn't supported on this platform
            self._ble_last_scan = ticks_ms() - 5000
            self._connection_count = 0
            self._split_connected = False
            self._uart_connection = None
            self._advertisment = None  # Seems to not be used anywhere
            self._advertising = False
            self._psave_enable = False

        if self._use_pio:
            from kmk.transports.pio_uart import PIO_UART

            self.PIO_UART = PIO_UART

    def during_bootup(self, keyboard):
        # Set up name for target side detection and BLE advertisment
        name = str(getmount('/').label)
        if self.split_type == SplitType.BLE:
            if keyboard.hid_type == HIDModes.BLE:
                self._ble = keyboard._hid_helper.ble
            else:
                self._ble = self.BLERadio()
                self._ble.name = name
        else:
            # Try to guess data pins if not supplied
            if not self.data_pin:
                self.data_pin = keyboard.data_pin

        # if split side was given, find target from split_side.
        if self.split_side == SplitSide.LEFT:
            self._is_target = bool(self.split_target_left)
        elif self.split_side == SplitSide.RIGHT:
            self._is_target = not bool(self.split_target_left)
        else:
            # Detect split side from name
            if (
                self.split_type == SplitType.UART
                or self.split_type == SplitType.ONEWIRE
            ):
                self._is_target = runtime.usb_connected
            elif self.split_type == SplitType.BLE:
                self._is_target = name.endswith('L') == self.split_target_left

            if name.endswith('L'):
                self.split_side = SplitSide.LEFT
            elif name.endswith('R'):
                self.split_side = SplitSide.RIGHT

        if not self._is_target:
            keyboard._hid_send_enabled = False

        if self.split_offset is None:
            self.split_offset = keyboard.matrix[-1].coord_mapping[-1] + 1

        if self.split_type == SplitType.UART and self.data_pin is not None:
            print('SPLIT is_target ', self._is_target)
            if self._is_target or not self.uart_flip:
                print('  tx is pin2')
                if self._use_pio:
                    self._uart = self.PIO_UART(tx=self.data_pin2, rx=self.data_pin)
                else:
                    self._uart = busio.UART(
                        tx=self.data_pin2,
                        rx=self.data_pin,
                        timeout=self._uart_interval,
                        receiver_buffer_size=2048,
                        baudrate=115200,
                    )
            else:
                print('  tx is pin1')
                if self._use_pio:
                    self._uart = self.PIO_UART(tx=self.data_pin, rx=self.data_pin2)
                else:
                    self._uart = busio.UART(
                        tx=self.data_pin,
                        rx=self.data_pin2,
                        timeout=self._uart_interval,
                        receiver_buffer_size=2048,
                        baudrate=115200,
                    )

        # Attempt to sanely guess a coord_mapping if one is not provided.
        if not keyboard.coord_mapping:
            cm = []

            rows_to_calc = len(keyboard.row_pins)
            cols_to_calc = len(keyboard.col_pins)

            # Flips the col order if PCB is the same but flipped on right
            cols_rhs = list(range(cols_to_calc))
            if self.split_flip:
                cols_rhs = list(reversed(cols_rhs))

            for ridx in range(rows_to_calc):
                for cidx in range(cols_to_calc):
                    cm.append(cols_to_calc * ridx + cidx)
                for cidx in cols_rhs:
                    cm.append(cols_to_calc * (rows_to_calc + ridx) + cidx)

            keyboard.coord_mapping = tuple(cm)

        if self.split_side == SplitSide.RIGHT:
            offset = self.split_offset
            for matrix in keyboard.matrix:
                matrix.offset = offset
                offset += matrix.key_count

    def before_matrix_scan(self, keyboard):
        if self.split_type == SplitType.BLE:
            self._check_all_connections(keyboard)
            self._receive_ble(keyboard)
        elif self.split_type == SplitType.UART:
            if self._is_target or self.data_pin2:
                self._receive_uart(keyboard)
        elif self.split_type == SplitType.ONEWIRE:
            pass  # Protocol needs written
        return

    def after_matrix_scan(self, keyboard):
        if keyboard.matrix_update:
            if self.split_type == SplitType.UART:
                if not self._is_target:
                    self._send_uart(keyboard.matrix_update)
                else:
                    pass  # explicit pass just for dev sanity...
            elif self.split_type == SplitType.BLE:
                self._send_ble(keyboard.matrix_update)
            elif self.split_type == SplitType.ONEWIRE:
                pass  # Protocol needs written
            else:
                print('Unexpected case in after_matrix_scan')

        return

    def before_hid_send(self, keyboard):
        if not self._is_target:
            keyboard.hid_pending = False

        return

    def after_hid_send(self, keyboard):
        return

    def on_powersave_enable(self, keyboard):
        if self.split_type == SplitType.BLE:
            if self._uart_connection and not self._psave_enable:
                self._uart_connection.connection_interval = self._uart_interval
                self._psave_enable = True

    def on_powersave_disable(self, keyboard):
        if self.split_type == SplitType.BLE:
            if self._uart_connection and self._psave_enable:
                self._uart_connection.connection_interval = 11.25
                self._psave_enable = False

    def _check_all_connections(self, keyboard):
        '''Validates the correct number of BLE connections'''
        self._previous_connection_count = self._connection_count
        self._connection_count = len(self._ble.connections)
        if self._is_target:
            if self._advertising or not self._check_if_split_connected():
                self._target_advertise()
            elif self._connection_count < 2 and keyboard.hid_type == HIDModes.BLE:
                keyboard._hid_helper.start_advertising()

        elif not self._is_target and self._connection_count < 1:
            self._initiator_scan()

    def _check_if_split_connected(self):
        # I'm looking for a way how to recognize which connection is on and which one off
        # For now, I found that service name relation to having other CP device
        if self._connection_count == 0:
            return False
        if self._connection_count == 2:
            self._split_connected = True
            return True

        # Polling this takes some time so I check only if connection_count changed
        if self._previous_connection_count == self._connection_count:
            return self._split_connected

        bleio_connection = self._ble.connections[0]._bleio_connection
        connection_services = bleio_connection.discover_remote_services()
        for service in connection_services:
            if str(service.uuid).startswith("UUID('adaf0001"):
                self._split_connected = True
                return True
        return False

    def _initiator_scan(self):
        '''Scans for target device'''
        self._uart = None
        self._uart_connection = None
        # See if any existing connections are providing UARTService.
        self._connection_count = len(self._ble.connections)
        if self._connection_count > 0 and not self._uart:
            for connection in self._ble.connections:
                if self.UARTService in connection:
                    self._uart_connection = connection
                    self._uart_connection.connection_interval = 11.25
                    self._uart = self._uart_connection[self.UARTService]
                    break

        if not self._uart:
            if self._debug_enabled:
                print('Scanning')
            self._ble.stop_scan()
            for adv in self._ble.start_scan(
                self.ProvideServicesAdvertisement, timeout=20
            ):
                if self._debug_enabled:
                    print('Scanning')
                if self.UARTService in adv.services and adv.rssi > -70:
                    self._uart_connection = self._ble.connect(adv)
                    self._uart_connection.connection_interval = 11.25
                    self._uart = self._uart_connection[self.UARTService]
                    self._ble.stop_scan()
                    if self._debug_enabled:
                        print('Scan complete')
                    break
        self._ble.stop_scan()

    def _target_advertise(self):
        '''Advertises the target for the initiator to find'''
        # Give previous advertising some time to complete
        if self._advertising:
            if self._check_if_split_connected():
                if self._debug_enabled:
                    print('Advertising complete')
                self._ble.stop_advertising()
                self._advertising = False
                return

            if not self.ble_rescan_timer():
                return

            if self._debug_enabled:
                print('Advertising not answered')

        self._ble.stop_advertising()
        if self._debug_enabled:
            print('Advertising')
        # Uart must not change on this connection if reconnecting
        if not self._uart:
            self._uart = self.UARTService()
        advertisement = self.ProvideServicesAdvertisement(self._uart)

        self._ble.start_advertising(advertisement)
        self._advertising = True
        self.ble_time_reset()

    def ble_rescan_timer(self):
        '''If true, the rescan timer is up'''
        return not bool(check_deadline(ticks_ms(), self._ble_last_scan, 5000))

    def ble_time_reset(self):
        '''Resets the rescan timer'''
        self._ble_last_scan = ticks_ms()

    def _serialize_update(self, update):
        buffer = bytearray(2)
        print('-----serialize_update', update)
        buffer[0] = update.key_number
        buffer[1] = update.pressed
        return buffer

    def _deserialize_update(self, update):
        kevent = KeyEvent(key_number=update[0], pressed=update[1])
        print('----deserialize-update', kevent, update, update.decode())
        return kevent

    def _send_ble(self, update):
        if self._uart:
            try:
                self._uart.write(self._serialize_update(update))
            except OSError:
                try:
                    self._uart.disconnect()
                except:  # noqa: E722
                    if self._debug_enabled:
                        print('UART disconnect failed')

                if self._debug_enabled:
                    print('Connection error')
                self._uart_connection = None
                self._uart = None

    def _receive_ble(self, keyboard):
        if self._uart is not None and self._uart.in_waiting > 0 or self._uart_buffer:
            while self._uart.in_waiting >= 2:
                update = self._deserialize_update(self._uart.read(2))
                self._uart_buffer.append(update)
            if self._uart_buffer:
                keyboard.secondary_matrix_update = self._uart_buffer.pop(0)

    def _checksum(self, update):
        checksum = bytes([sum(update) & 0xFF])

        return checksum

    def _send_uart(self, update):
        if self._uart is not None:
            self.send_msg(self.uart_header, self._serialize_update(update))

    def send_msg(self, msg_type, msg):
        print('--->  sending msg', bytes([msg_type]), msg)
        msg = bytes([msg_type]) + bytes([len(msg)]) + msg + self._checksum(msg)
        self._uart.write(msg)

    def _receive_uart(self, keyboard):
        if (not self._uart) or self._uart.in_waiting == 0:
            return
        # if self._uart.in_waiting >= 60:
        #     # This is a dirty hack to prevent crashes in unrealistic cases
        #     import microcontroller
        #     microcontroller.reset()
        if self._uart.in_waiting < 4:
            # return early. it'll get picked up in next tick
            return
        if self._uart_to_read > 0:
            print('::: continuing to read uart data. msg type: ', bytes([self._uart_receiving_msg_type]), 'buffered: ', len(self._uart_buffer), ' to read: ', self._uart_to_read)
            msg_type = self._uart_receiving_msg_type
            msg_len = len(self._uart_buffer) + self._uart_to_read - 1
            in_waiting = self._uart.in_waiting
            if in_waiting < self._uart_to_read:
                self._uart_buffer += self._uart.read(in_waiting)
                self._uart_to_read -= in_waiting
                # exit early because not enough bytes left 
                return
            msg = self._uart_buffer + self._uart.read(msg_len - len(self._uart_buffer))
            print('  msg', msg)
            checksum = self._uart.read(1)
            print('  checksum', checksum)
            self._uart_buffer = bytearray([])
            self._uart_receiving_msg_type = None
            self._uart_to_read = 0
        else:
            print('::: reading uart data :::')
            msg_type = self._uart.read(1)[0]
            print('<--- receiving msg', bytes([msg_type]))
            if msg_type not in self._msg_receivers:
                print('!!-WARNING-!! received invalid msg_type', bytes([msg_type]))
                return
            msg_len = int(self._uart.read(1)[0])
            print('  msg_len', msg_len)
            in_waiting = self._uart.in_waiting
            if in_waiting < msg_len + 1:
                self._uart_buffer += self._uart.read(in_waiting)
                self._uart_to_read = msg_len + 1 - in_waiting
                self._uart_receiving_msg_type = msg_type
                # exit early because not enough bytes left 
                return
            # while self._uart.in_waiting < msg_len + 1:
            #     print('...waiting for msg_len+1 to be in_waiting')
            msg = self._uart.read(msg_len)
            print('  msg', msg)
            checksum = self._uart.read(1)
            print('  checksum', checksum)
        if checksum != self._checksum(msg):
            print('WARNING received msg with invalid checksum')
            return
        self._msg_receivers[msg_type](msg, keyboard)

    def add_receiver(self, msg_type, receiver):
        print('----adding', msg_type, receiver, self._msg_receivers)
        if msg_type in self._msg_receivers:
            raise KeyError("The chosen msg_type is already in use. You must use a unique msg_type")
        self._msg_receivers[msg_type] = receiver
    
    def _receive_msg(self, msg, keyboard):
        keyboard.secondary_matrix_update = self._deserialize_update(msg)
