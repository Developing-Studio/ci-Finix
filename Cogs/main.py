from discord.ext import commands
import discord
from Tools.func import sendEmbed, can_use, warn
from Tools.var import embedcolor, mainprefix, prefix
from os import listdir, remove
from datetime import datetime
from asyncio import TimeoutError
from PIL import Image

class Main(commands.Cog, name='잡다한것'):
    """
    잡다한 명령어들이 들어 있는 카테고리입니다. ~~잡것
    """
    
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name='이모지', aliases=['raw', '이모티콘'], help='이모지의 raw 값을 보여줍니다.', usage='[이모지]')
    @can_use()
    async def _emoji(self, ctx, *, emoji: discord.Emoji):
        await sendEmbed(ctx=ctx, title='이모지', content=f'`{emoji}`: {emoji}')
    
    @commands.command(name='파일생성', aliases=['makefile', '파일'], help='텍스트를 파일로 만듭니다', usage='<파일제목> [파일내용]')
    @can_use()
    @commands.cooldown(1.0, 3, commands.BucketType.user)
    async def _makefile(self, ctx, title='file.txt', *, content):
        with open(title, 'w') as f:
            f.write(content)
        dm = await ctx.author.create_dm()
        await dm.send(file=discord.File(title))
        remove(title)
        try: await ctx.message.delete()
        except: pass
        await sendEmbed(ctx=ctx, title='완료', content='DM으로 파일이 전송되었습니다.\n\n만약 전송되지 않았다면 DM을 차단하지 않았는지 확인해 보세요.')
    
    @commands.command(name='색깔보기', aliases=['색보기', 'color'], help='RGB로 입력한 색상을 보여줍니다', usage='[R] [G] [B]')
    @commands.cooldown(1.0, 5, commands.BucketType.user)
    @can_use()
    async def _seecolor(self, ctx, R: int, G: int, B: int):
        if R > 255 or G > 255 or B > 255:
            await warn(ctx=ctx, content='RGB에 해당하는 십진수 값을 올바르게 넣어 주세요')
            return
        img = Image.new("RGB", (256,256), (R, G, B))
        img.save('color.png')
        await ctx.send(file=discord.File('color.png'))
        remove('color.png')

def setup(bot):
    bot.add_cog(Main(bot))