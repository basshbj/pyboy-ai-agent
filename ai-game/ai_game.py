import base64
import os
import io
import time

from dotenv import load_dotenv
from openai import AzureOpenAI
from pyboy import PyBoy
from PIL import Image

load_dotenv()

# ------- PyBoy Emulator -------
def init_emulator(rom_path: str, game_state_path) -> PyBoy:
  """
  Initialize the Game Boy emulator.

  Args:
    rom_path (str): Path to the ROM file.
    game_state_path (str): Path to the game state file.

  Returns:
      PyBoy: The initialized emulator.
  """
  game_boy = PyBoy(rom_path)

  if game_state_path:
    with open(game_state_path, 'rb') as f:
      game_boy.load_state(f)

  game_boy.tick(1, True)

  return game_boy

def save_screen(game_boy: PyBoy) -> Image:
  """
  Save the current screen.

  Args:
    game_bot: PyBoy: The emulator instance.

  Returns:
      bytes: The image of the current screen.
  """
  img = game_boy.screen.image
  img.save(f'ai-game/screens/{int(time.time())}.png')

  return img

def excute_in_game_action(game_boy: PyBoy, action: str):
  """
  Execute an action in the game.

  Args:
    game_boy (PyBoy): The emulator instance.
    action (str): The action to perform.
  """
  game_boy.button(action)
  for _ in range(60):
    game_boy.tick(1, True)


# ------- Azure OpenAI API -------
def init_aoai() -> AzureOpenAI:
  """
  Initialize the Azure OpenAI API.

  Returns:
      aoai_client: The initialized API client.
  """

  azure_openai = AzureOpenAI(
    api_key=os.getenv("AOAI_API_KEY"),
    api_version=os.getenv("AOAI_API_VERSION"),
    azure_deployment=os.getenv("AOAI_DEPLOYMENT"),
    azure_endpoint=os.getenv("AOAI_ENDPOINT")
  )

  return azure_openai

def generete_action(aoai_client: AzureOpenAI, messages: list) -> str:
  """
  Generate a response from the OpenAI API.

  Args:
    aoai_client (AzureOpenAI): The API client.
    messages (list): The messages to send to the API.

  Returns:
      str: The generated response.
  """
  max_tokens = 100

  response = aoai_client.chat.completions.create(
      model=os.getenv("AOAI_DEPLOYMENT"),
      messages=messages,
      max_tokens=800,
      temperature=1.0
      #response_format={"type": "json_object"}
  )

  return response.choices[0].message.content

def init_messege_list() -> list:
  """
  Initialize the message list.

  Returns:
      list: The initialized message list.
  """
  with open("ai-game/prompts/system-prompt.txt", "r") as f:
    sys_prompt = f.read()

  messages = [
      {
          "role": "system",
          "content": sys_prompt
      }
  ]

  return messages

def create_user_message(messages:list, img: Image) -> list:
  """
  Create a user message.

  Args:
    messages (list): The message list.
    img (Image): The current screen image.

  Returns:
      list: The updated message list.
  """
  buffered = io.BytesIO()
  img.save(buffered, format="PNG")

  img_base64 = base64.b64encode(buffered.getvalue()).decode("utf-8")

  img_data_uri = f"data:image/png;base64,{img_base64}"

  messages.append(
    { "role": "user", "content": [  
        { 
          "type": "text", 
          "text": "Predict the next action: " 
        },
        { 
          "type": "image_url",
          "image_url": {
            "url": img_data_uri
          }
        }
    ] } 
  )

  # Save the current screen image
  img.save('test/screens/screen.png')

  return messages

if __name__ == "__main__":
  rom_path = 'roms/pokemon_red.gb'
  game_state_path = 'roms/pokemon_red_start.gb.state'

  # Initialize the emulator
  game_boy = init_emulator(rom_path, game_state_path)
  
  aoai_client = init_aoai()
  messages = init_messege_list()

  while True:
    #time.sleep(1)
    current_screen = save_screen(game_boy)

    messages = create_user_message(messages, current_screen)
    action = generete_action(aoai_client, messages)

    print(f"AI Action >>> {action}")

    if action.lower() == "up":
      print("Moving Up")
      excute_in_game_action(game_boy, "up")
    elif action.lower() == "down":
      print("Moving Down")
      excute_in_game_action(game_boy, "down")
    elif action.lower() == "left":
      print("Moving Left")
      excute_in_game_action(game_boy, "left")
    elif action.lower() == "right":
      print("Moving Right")
      excute_in_game_action(game_boy, "right")
    elif action.lower() == "done":
      break

  game_boy.stop()
  
    