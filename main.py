import os, discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

intents = discord.Intents.default()
intents.message_content = True

class QuizBot(commands.Bot):
    async def setup_hook(self):
        await self.load_extension("test-y9")

bot = QuizBot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Online :)")

bot.run(os.getenv("TOKEN"))
