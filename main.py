import discord
from discord.ext import commands
import asyncio

intents = discord.Intents.default()
intents.members = True
intents.messages = True
intents.message_content = True

ascii_art = """
░█████╗░░█████╗░███████╗███╗░░██╗██╗░█████╗░  ░██████╗██████╗░░█████╗░███╗░░░███╗███╗░░░███╗███████╗██████╗░
██╔══██╗██╔══██╗██╔════╝████╗░██║██║██╔══██╗  ██╔════╝██╔══██╗██╔══██╗████╗░████║████╗░████║██╔════╝██╔══██╗
███████║██║░░╚═╝█████╗░░██╔██╗██║██║██║░░╚═╝  ╚█████╗░██████╔╝███████║██╔████╔██║██╔████╔██║█████╗░░██████╔╝
██╔══██║██║░░██╗██╔══╝░░██║╚████║██║██║░░██╗  ░╚═══██╗██╔═══╝░██╔══██║██║╚██╔╝██║██║╚██╔╝██║██╔══╝░░██╔══██╗
██║░░██║╚█████╔╝███████╗██║░╚███║██║╚█████╔╝  ██████╔╝██║░░░░░██║░░██║██║░╚═╝░██║██║░╚═╝░██║███████╗██║░░██║
╚═╝░░╚═╝░╚════╝░╚══════╝╚═╝░░╚══╝╚═╝░╚════╝░  ╚═════╝░╚═╝░░░░░╚═╝░░╚═╝╚═╝░░░░░╚═╝╚═╝░░░░░╚═╝╚══════╝╚═╝░░╚═╝
"""

owner_details = """
Made by: @Naitik.exe_
Base code by: @MICH_EL
"""

async def start_bot(token):
    bot = commands.Bot(command_prefix='!', intents=intents)

    @bot.event
    async def on_ready():
        print(f'{bot.user} is online!')

    @bot.command()
    async def dm(ctx, user_id: int, *, message):
        print(f"Received !dm command with user_id={user_id} and message={message}")
        user = bot.get_user(user_id)
        if user:
            await ctx.send(f"How many times do you want to send the message to {user}?")
            
            def check(m):
                return m.author == ctx.author and m.channel == ctx.channel and m.content.isdigit()
            
            try:
                response = await bot.wait_for('message', check=check, timeout=30)
                message_count = int(response.content)
                
                for _ in range(message_count):
                    await user.send(message)
                    
                await ctx.send(f'Successfully sent {message_count} message(s) to {user}!')
                
            except asyncio.TimeoutError:
                await ctx.send("You didn't respond in time. Command cancelled.")
            
        else:
            await ctx.send("User not found.")

    @bot.command()
    async def invite(ctx):
        app_info = await bot.application_info()
        invite_url = f"https://discord.com/api/oauth2/authorize?client_id={app_info.id}&permissions=8&scope=bot"
        await ctx.send(f"Click the following link to invite the bot to your server: {invite_url}")

    await bot.start(token)

async def main():
   
    print(ascii_art)
    print(owner_details)
    
    with open('tokens.txt', 'r') as file:
        tokens = file.readlines()

    tokens = [token.strip() for token in tokens if token.strip()]

    tasks = [start_bot(token) for token in tokens]
    await asyncio.gather(*tasks)

if __name__ == "__main__":
    asyncio.run(main())
