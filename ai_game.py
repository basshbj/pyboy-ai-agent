import asyncio
import os

from dotenv import load_dotenv
from src.gameboy import GameBoy, GameBoyActions
from src.aiagent import AIAgent

load_dotenv()


async def main():
  rom_path = 'roms/pokemon_red.gb'
  game_state_path = 'roms/pokemon_red_start.gb.state'

  # Initialize the emulator
  game_boy = GameBoy(rom_path, game_state_path, screenshot_path='./screens')
  
  # Initialize the AI agent
  ai_agent = AIAgent(
    aoai_endpoint=os.getenv("AOAI_ENDPOINT"),
    aoai_api_key=os.getenv("AOAI_API_KEY"),
    aoai_api_version=os.getenv("AOAI_API_VERSION"),
    aoai_deployment=os.getenv("AOAI_DEPLOYMENT")
  )
  
  fps = 60

  while game_boy.game_boy.tick():
    current_frame = game_boy.save_screen(save_to_file=False)    

    action = await ai_agent.generate_action(current_frame)

    print(f"AI Action >>> {action.value}")

    if action == GameBoyActions.DONE:
      break
    else:
      game_boy.execute_in_game_action(action)
      # Render 60 frames to ensure the action is processed
      for _ in range(fps):
        game_boy.game_boy.tick(1, True)

  game_boy.game_boy.stop()


if __name__ == "__main__":
  asyncio.run(main())
  

  
    