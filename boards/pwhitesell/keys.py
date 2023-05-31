from kmk.keys import KC
from kmk.handlers.sequences import simple_key_sequence
from kmk.modules.rgbkeys import Color

_L1_ = KC.MO(1)
_L2_ = KC.MO(2)
_L3_ = KC.MO(3)
_L4_ = KC.MO(4)
SP_1 = KC.HT(KC.SPACE, KC.MO(1), tap_time=200)
SPC1 = KC.HT(KC.SPACE, KC.MO(1), tap_time=200)
BSP2 = KC.HT(KC.BSPC, KC.MO(2), tap_time=200)
_🚫_ = KC.NO
↓___ = KC.TRNS
__1_ = KC.N1
__2_ = KC.N2
__3_ = KC.N3
__4_ = KC.N4
__5_ = KC.N5
__6_ = KC.N6
__7_ = KC.N7
__8_ = KC.N8
__9_ = KC.N9
__0_ = KC.N0
_1__ = KC.N1
_2__ = KC.N2
_3__ = KC.N3
_4__ = KC.N4
_5__ = KC.N5
_6__ = KC.N6
_7__ = KC.N7
_8__ = KC.N8
_9__ = KC.N9
_0__ = KC.N0
_TAB = KC.TAB
CTAB = KC.SM(KC.TAB, KC.LCMD)
TTAB = KC.LCMD(KC.GRV)
__A_ = KC.A
__B_ = KC.B
__C_ = KC.C
__D_ = KC.D
__E_ = KC.E
__F_ = KC.F
__G_ = KC.G
__H_ = KC.H
__I_ = KC.I
__J_ = KC.J
__K_ = KC.K
__L_ = KC.L
__M_ = KC.M
__N_ = KC.N
__O_ = KC.O
__P_ = KC.P
__Q_ = KC.Q
__S_ = KC.S
__R_ = KC.R
__T_ = KC.T
__U_ = KC.U
__V_ = KC.V
__W_ = KC.W
__X_ = KC.X
__Y_ = KC.Y
__Z_ = KC.Z
SPCE = KC.SPACE
✂__← = KC.BSPC
QUOT = KC.QUOT
SCLN = KC.SCLN
EXLM = KC.EXLM
LSFT = KC.TD(KC.HT(KC.OS(KC.LSFT, tap_time=None), KC.LSFT), KC.CW)
RSFT = KC.TD(KC.HT(KC.OS(KC.RSFT, tap_time=None), KC.RSFT), KC.CW)
RCMD = KC.HT(KC.OS(KC.RCMD, tap_time=None), KC.RCMD)
LCMD = KC.HT(KC.OS(KC.LCMD, tap_time=None), KC.LCMD)
RALT = KC.HT(KC.OS(KC.RALT, tap_time=None), KC.RALT)
LALT = KC.HT(KC.OS(KC.LALT, tap_time=None), KC.LALT)
RCTL = KC.RCTL
LCTL = KC.HT(KC.OS(KC.LCTL, tap_time=None), KC.LCTL)
LCLK = KC.MB_LMB
CCLK = simple_key_sequence((
  KC.LCMD(no_release=True),
  KC.MACRO_SLEEP_MS(30),
  KC.MB_LMB,
  KC.MACRO_SLEEP_MS(30),
  KC.LCMD(no_press=True),
))
RCLK = KC.MB_RMB
ENTR = KC.ENT
CENT = KC.LCMD(KC.ENT)
PERD = KC.DOT
COMA = KC.COMM
SLSH = KC.SLSH
__↑_ = KC.UP
__↓_ = KC.DOWN
__←_ = KC.LEFT
__→_ = KC.RIGHT
_↑↑_ = KC.PGUP
_↓↓_ = KC.PGDN
_←←_ = KC.LALT(KC.LEFT)
_→→_ = KC.LALT(KC.RIGHT)
↑↑↑_ = KC.LCMD(KC.UP)
↓↓↓_ = KC.LCMD(KC.DOWN)
←←←_ = KC.LCMD(KC.LEFT)
→→→_ = KC.LCMD(KC.RIGHT)
S_↑_ = KC.LSFT(KC.UP)
S_↓_ = KC.LSFT(KC.DOWN)
S_←_ = KC.LSFT(KC.LEFT)
S_→_ = KC.LSFT(KC.RIGHT)
S↑↑_ = KC.LSFT(KC.PGUP)
S↓↓_ = KC.LSFT(KC.PGDN)
S←←_ = KC.LSFT(KC.LALT(KC.LEFT))
S→→_ = KC.LSFT(KC.LALT(KC.RIGHT))
S↑↑↑ = KC.LSFT(KC.LCMD(KC.UP))
S↓↓↓ = KC.LSFT(KC.LCMD(KC.DOWN))
S←←← = KC.LSFT(KC.LCMD(KC.LEFT))
S→→→ = KC.LSFT(KC.LCMD(KC.RIGHT))
PGUP = KC.PGUP
PGDN = KC.PGDN
✂__← = KC.BKSP
✂__→ = KC.DEL
✂_←← = KC.LALT(KC.BKSP)
✂_→→ = KC.LALT(KC.DEL)
✂←←← = KC.LCMD(KC.BKSP)
✂→→→ = KC.LCMD(KC.DEL)
_EQL = KC.EQL
MINS = KC.MINUS
UNDS = KC.UNDS
LCBR = KC.LCBR
RCBR = KC.RCBR
LPRN = KC.LPRN
RPRN = KC.RPRN
LBRC = KC.LBRC
RBRC = KC.RBRC
LABK = KC.LABK
RABK = KC.RABK
BSLS = KC.BSLS
COPY = KC.LCMD(KC.C)
_CUT = KC.LCMD(KC.X)
PAST = KC.LCMD(KC.V)
UNDO = KC.LCMD(KC.Z)
_ALL = KC.LCMD(KC.A)
SAVE = KC.LCMD(KC.S)
MTSL = KC.LCMD(KC.D)
FIND = KC.LCMD(KC.F)
SKSL = KC.LCMD(KC.K)
CLOS = KC.LCMD(KC.W)
RLOD = KC.LCMD(KC.R)
NTAB = KC.LCMD(KC.T)
TICK = KC.GRV
ESCP = KC.ESC
EMOJ = KC.LCMD(KC.LCTL(KC.SPACE))
_URL = KC.LCMD(KC.L)
LNCH = KC.LCMD(KC.SPACE)
CLPB = KC.LCMD(KC.LSFT(KC.V))
CMNT = KC.LCMD(KC.SLSH)
PRNT = KC.LCMD(KC.P)
PTSC = KC.LCMD(KC.LSFT(KC.N4))
VDSC = KC.LCMD(KC.LSFT(KC.N5))
OPEN = KC.LCMD(KC.O)
NEW_ = KC.LCMD(KC.N)
CMCT = KC.LCMD(KC.LCTL)
MSSN = KC.LCTL(KC.UP)
APPN = KC.LCTL(KC.DOWN)

class KeyColors:
  Off = Color(v=0)
  Letter = Color(h=140, s=100)
  Number = Color(h=18)
  Math = Color(h=18)
  Bracket = Color(h=42, s=200)
  Punctuation = Color(h=42)
  Mod = Color(h=205)
  Mouse = Color(h=20)
  Danger = Color(h=0)
  Space = Color(s=0)
  Nav = Color(h=150)
  Edit = Color(h=110)
  Browse = Color(s=150)
  ClipBoard = Color(h=88)
  Window = Color(h=45)
  SPC1 = Color(s=0, other=Mod)
  SP_1 = Color(s=0, other=Mod)
  BackSpace_L2 = Color(h=0, other=Mod)