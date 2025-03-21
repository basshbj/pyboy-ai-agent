from pyboy import PyBoy

pyboy_emu = PyBoy('roms/pokemon_red.gb')

while pyboy_emu.tick():
    pass

pyboy_emu.stop()