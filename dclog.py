import discord, asyncio
from discord.ext import commands
from dico_token import Token
 
# 수정. 2024.02.22
intents = discord.Intents.default()
intents.message_content = True
 
bot = commands.Bot(
    command_prefix=commands.when_mentioned_or("!"),
    description='디스코드 입장을 위한 테스트 코드',
    intents=intents,
)
 
@bot.event
async def on_ready():
    print('{0.user} 봇을 실행합니다.'.format(bot))
 
# 2024 08 24 수정
@bot.command(aliases=['입장'])
async def join(ctx):
    embed = discord.Embed(title = "디스코드 봇 도우미(개발용)", description = "음성 채널 개발용 디스코드 봇",color=0x00ff56)
    channel = ctx.author.voice.channel
    
    if ctx.author.voice is None:
        embed.add_field(name=':exclamation:', value="음성 채널에 유저가 존재하지 않습니다. 1명 이상 입장해주세요.")
        await ctx.send(embed=embed)
        raise commands.CommandInvokeError("사용자가 존재하는 음성 채널을 찾지 못했습니다.")
    
    if ctx.voice_client is not None:
        embed.add_field(name=":robot:",value="사용자가 있는 채널로 이동합니다.", inline=False)
        await ctx.send(embed=embed)
        print("음성 채널 정보: {0.author.voice}".format(ctx))
        print("음성 채널 이름: {0.author.voice.channel}".format(ctx))
        return await ctx.voice_client.move_to(channel)
        
    await channel.connect()
    
@bot.command(aliases=['나가기'])
async def out(ctx):
    try:
        embed = discord.Embed(color=0x00ff56)
        embed.add_field(name=":regional_indicator_b::regional_indicator_y::regional_indicator_e:",value=" {0.author.voice.channel}에서 내보냈습니다.".format(ctx),inline=False)
        await bot.voice_clients[0].disconnect()
        await ctx.send(embed=embed)
    except IndexError as error_message:
        print(f"에러 발생: {error_message}")
        embed = discord.Embed(color=0xf66c24)
        embed.add_field(name=":grey_question:",value="{0.author.voice.channel}에 유저가 존재하지 않거나 봇이 존재하지 않습니다.\\n다시 입장후 퇴장시켜주세요.".format(ctx),inline=False)
        await ctx.send(embed=embed)
    except AttributeError as not_found_channel:
        print(f"에러 발생: {not_found_channel}")
        embed = discord.Embed(color=0xf66c24)
        embed.add_field(name=":x:",value="봇이 존재하는 채널을 찾는 데 실패했습니다.")
        await ctx.send(embed=embed)
 
bot.run(Token)