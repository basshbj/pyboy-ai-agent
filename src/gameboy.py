import time

from enum import Enum
from pyboy import PyBoy
from PIL import Image


class GameBoyActions(Enum):
  """
  List of actions that can be performed in the game.
  """
  UP = 'UP'
  DOWN = 'DOWN'
  LEFT = 'LEFT'
  RIGHT = 'RIGHT'
  A = 'A'
  B = 'B'
  START = 'START'
  SELECT = 'SELECT'
  DONE = 'DONE'


class GameBoy:

  def __init__(self, rom_path: str, game_state_path: str = None, screenshot_path: str = None):
    """
    Initialize the Game Boy emulator.
    Args:
        rom_path (str): Path to the ROM file.
        game_state_path (str): Path to the game state file.
        screenshot_path (str): Path to save the screenshot.
    """
    self.screenshot_path = screenshot_path
    self.game_boy = PyBoy(rom_path)

    if game_state_path:
      with open(game_state_path, 'rb') as f:
        self.game_boy.load_state(f)

    self.game_boy.tick(1, True)
  

  def save_screen(self, save_to_file: bool = True) -> Image:
    """
    Take a screenshot of the current screen and save it.

    Args:
      save_to_file (bool): Whether to save the screenshot to a file.
        Defaults to True.

    Returns:
        bytes: The image of the current screen.
    """
    img = self.game_boy.screen.image

    if save_to_file and self.screenshot_path:
      img.save(f'{self.screenshot_path}/{int(time.time())}.png')

    return img
  

  def execute_in_game_action(self, action: GameBoyActions):
    """
    Execute an action in the game.

    Args:
      action (GameBoyActions): The action to perform.
    """
    self.game_boy.button(action.value)

    # Render 60 frames to ensure the action is processed
    # for _ in range(60):
    #   self.game_boy.tick(1, True)
