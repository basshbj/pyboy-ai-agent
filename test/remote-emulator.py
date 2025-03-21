from pyboy import PyBoy
from PIL import Image

pyboy_emu = PyBoy('roms/pokemon_red.gb')

# Load State
with open('roms/pokemon_red_start.gb.state', 'rb') as f:
  pyboy_emu.load_state(f)

pyboy_emu.tick(1, True)

# Sample move character
#for i in range(5):
pyboy_emu.button("right")
for _ in range(60):
  pyboy_emu.tick(1, True)

img = pyboy_emu.screen.image
img.save(f'test/screens/tick_.png')
  # img = pyboy_emu.screen.image
  # img.save(f'test/screens/sample_move_{i}.png')



# #pyboy_emu.set_emulation_speed(0)

# ticks = 0

# pyboy_emu.tick(1500, True)

# pyboy_emu.button('a')

# pyboy_emu.tick(1, True)

# img = pyboy_emu.screen.image
# img.save(f'test/screens/{ticks}.png')

i = 0

# while pyboy_emu.tick():
#   img = pyboy_emu.screen.image
#   img.save(f'test/screens/tick_{i}.png')
#   i += 1 
#pyboy_emu.tick(100, True)

  # if ticks % 100 == 0:
  #   print(f"Ticks: {ticks}")
  #   img = pyboy_emu.screen.image
  #   img.save(f'test/screens/{ticks}.png')

  #ticks += 1

pyboy_emu.stop()