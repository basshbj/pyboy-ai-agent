import asyncio
import base64
import io

from src.gameboy import GameBoyActions
from openai import AsyncAzureOpenAI
from PIL import Image


class AIAgent:

  def __init__(self, aoai_endpoint: str, aoai_api_key: str, aoai_api_version: str, aoai_deployment: str):
    """
    Initialize the AI agent with Azure OpenAI API credentials.
    
    Args:
        aoai_endpoint (str): The endpoint for the Azure OpenAI API.
        aoai_api_key (str): The API key for the Azure OpenAI API.
        aoai_api_version (str): The version of the Azure OpenAI API.
        aoai_deployment (str): The deployment name for the Azure OpenAI API.
    """
    self.aoai_client = AsyncAzureOpenAI(
      api_key=aoai_api_key,
      api_version=aoai_api_version,
      azure_deployment=aoai_deployment,
      azure_endpoint=aoai_endpoint
    )

    self.aoai_deployment = aoai_deployment
    self.messages = []

    self.__reset_message_list()


  async def generate_action(self, frame: Image) -> GameBoyActions:
    """
    Generate the action to be executed.

    Args:
      frame (Image): The current frame of the game.

    Returns:
      GameBoyActions: The generated response.
    """

    self.__process_frame_as_message(frame)

    response = await self.aoai_client.chat.completions.create(
      model=self.aoai_deployment,
      messages=self.messages,
      max_tokens=800,
      temperature=1.0
    )

    return GameBoyActions[response.choices[0].message.content]
  

  def __reset_message_list(self):
    """
    Reset the message list.
    """
    self.messages = []

    with open("src/prompts/sys_prompt.txt", "r") as f:
      sys_prompt = f.read()

    self.messages = [
      {
        "role": "system",
        "content": sys_prompt
      }
    ]


  def __process_frame_as_message(self, frame: Image):
    """
    Process the frame as a message for the ChatCompletions API.

    Args:
      frame (Image): The current frame of the game.
    """

    with io.BytesIO() as buffered:
      frame.save(buffered, format="PNG")
      img_base64 = base64.b64encode(buffered.getvalue()).decode("utf-8")

    img_data_uri = f"data:image/png;base64,{img_base64}"

    self.messages.append(
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
        ] 
      } 
    )
    
