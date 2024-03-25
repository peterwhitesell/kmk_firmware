import time
import board
import neopixel

print('start...')
n = 24
pixels = neopixel.NeoPixel(board.D2, n, auto_write=False)
colors = [
  (100, 100, 100),
  (100, 0, 0),
  (0, 100, 0),
  (0, 0, 100),
  (50, 50, 0),
  (0, 50, 50),
  (50, 00, 50),
]
for i in range(n):
  # pixels[i] = (0, 0, 0)
#   pixels[i] = ((1+i)*10, (1+i)*10, (1+i)*10)
  # pixels[i] = (255, 255, 255)
#   pixels[i] = (i*10 + 1, i*10 + 1, i*10 + 1)
  pixels[i] = (0, 0, 0)
pixels.show()
i = 0
while True:
  print('sleep...', colors[i])
  time.sleep(1)
  pixels.fill(colors[i])
  pixels.show()
  i = (i + 1) % len(colors)
