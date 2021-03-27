

import discord
import asyncio
import os

client = discord.Client()




@client.event
async def on_ready():
    print(client.user.name)
    print('봇 구동완료')
    game = discord.Game(':/help')
    await client.change_presence(status=discord.Status.online, activity=game)

async def util_support(message, _client=None):
    if _client is None:
        try:
            bot
            _client = bot
        except:
            try:
                client
                _client = client
            except:
                raise Exception("봇, 클라이언트 객체를 찾을 수 없습니다. 입력해주세요.")
    if message.guild is not None:
        if message.channel.id != 823214526114693150:
            return False
        if message.content.startswith(":/문의종료"):
            _msg = message.content.replace(":/문의종료 ", "", 1)
            _user = _client.get_user(int(_msg))
            if _user is None:
                try:
                    _user = await _client.fetch_user(int(_msg))
                except:
                    raise Exception("사용자를 찾을 수 없습니다. 혹시 이 유저가 서버를 나갔나요?")
            if _user is None:
                raise Exception("사용자를 찾을 수 없습니다. 혹시 이 유저가 서버를 나갔나요?")
            await _user.send(embed=discord.Embed(description="문의가 종료되었습니다."))
            await message.delete()
            await message.channel.send(embed=discord.Embed(description=f"{_user.mention}님의 문의가 종료되었습니다."))
            return True
        elif message.content.startswith(":/답장"):
            _msg = message.content.replace(":/답장 ","", 1)
            _msg = _msg.split(" ")
            # print(_msg)
            _user = _client.get_user(int(_msg[0]))
            if _user is None:
                try:
                    _user = await _client.fetch_user(int(_msg[0]))
                except Exception as e:
                    raise Exception(f"사용자를 찾을 수 없습니다. 혹시 이 유저가 서버를 나갔나요? (Error: {e})")
            if _user is None:
                raise Exception("사용자를 찾을 수 없습니다. 혹시 이 유저가 서버를 나갔나요?")
            del _msg[0]
            _message = " ".join(_msg)
            await _user.send(embed=discord.Embed(description=f"**관리자**: {_message}"))
            return True
    else:
        _c = await _client.fetch_channel(823214526114693150)
        await _c.send(embed=discord.Embed(description=f"{message.author} ({message.author.id}): {message.content}"))
        await message.channel.send(embed=discord.Embed(description="관리자에게 문의가 전달되었습니다.", color=discord.Colour.green()))
        return True
    


@client.event
async def on_message(message):
    if message.author.bot: 
        return
    try:
        _data = await util_support(message, client)
    except Exception as e:
        print(e)
    try:
        if _data:
            return
    except:
        pass
    if message.content == ":/help":
        embed = discord.Embed(title="KBR 도우미봇 현재기능", description="1.봇의DM 으로 문의를 주시면 DM 으로 답해드립니다.\n 2.:/관리자 서버의 관리자들 목록이나옵니다.")
        embed.set_footer(text="봇의 기능은 더 추가될 예정입니다.")
        await message.channel.send(embed=embed)


    if message.content == ":/관리자":
        embed = discord.Embed(title="현재 KBR 관리자 목록", description="OWNER [OwOReple] \n CO-OWNER[srum0916] \nADMIN&HELPER&MOD&DEVELOPER[Me_aster]\n DEVELOPER[FSanchir]")
        embed.set_footer(text="현재 관리자는 이상태로 유지될 전망입니다..")
        await message.channel.send(embed=embed)

    # if str(message.channel.type) == 'private':
    #     embed = discord.Embed(title="**현재 문의기능은 개발중입니다.**")
    #     embed.set_footer(text="봇의 기능은 더 추가될 예정입니다.")
    #     await message.author.send(embed=embed)


access_token = os.environ["BOT_TOKEN"]
client.run(access_token)
