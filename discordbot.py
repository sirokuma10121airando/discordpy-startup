
import sys
import discord
import random
import asyncio
import time
import datetime
import urllib.request
import json
import re
import os
import traceback
import math
from discord.ext import tasks
from datetime import datetime, timedelta, timezone

JST = timezone(timedelta(hours=+9), 'JST')
TOKEN = os.environ['DISCORD_BOT_TOKEN']
client = discord.Client()

test_ch = None
test_ch_numch = None
test_ch_num = 0
test_flag = False
t_flag = False


@tasks.loop(seconds=30)
async def t_loop():
    if t_flag==True:
        t_ch = client.get_channel(660456253524541456)
        tao=client.get_user(526620171658330112)
        if tao:
            def test_check (t_msg):
                if t_msg.author != tao:
                    return 0
                if t_msg.channel!=t_ch:
                    return 0
                return 1

            try:
                t_res=await client.wait_for('message',timeout=10,check = test_check)
            except asyncio.TimeoutError:
                await t_ch.send('::t')
            else:
                pass

@tasks.loop(seconds=30)
async def test_check_loop():
    if test_flag==True:
        tao=client.get_user(526620171658330112)
        if tao:
            def test_check (d_msg):
                if d_msg.author != tao:
                    return 0
                if d_msg.channel!=test_ch:
                    return 0
                return 1

            try:
                t_res=await client.wait_for('message',timeout=30,check = test_check)
            except asyncio.TimeoutError:
                await test_ch.send('::attack とまってない?')
            else:
                pass


@tasks.loop(seconds=60)
async def st_loop():
    await client.change_presence(activity=discord.Game(name="s!help│専属BOTです！"))

@client.event
async def on_ready():


    #起動時刻（日本時刻）
    dateTime = datetime.now(JST)
    st_loop.start()
    test_check_loop.start()
    t_loop.start()
    await client.change_presence(activity=discord.Game(name="s!help│専属BOTです！"))
    print('◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢')
    print("‣BOT NAME\n '+(client.user.name)")
    print('‣BOT ID\n '+str(client.user.id))
    print('‣LOGIN TIME\n '+str(dateTime.now(JST)))
    print('◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢')


@client.event
async def on_message(message):

    if message.content=='s!ping':

        embed=discord.Embed(title='**Ping測定中**')
        msg=await message.channel.send(embed=embed)

        result=(msg.created_at - message.created_at).microseconds // 1000
        await msg.edit(embed=discord.Embed(title=f'**Pong!\n{result}ms**'))




    if message.content == "s!help":
        desc = 's!say [内容]\n```言ったことをオウム返しだよ```'
        desc += "\ns!ping```現在のサクラのping値を測定するよ```"
        desc += "\ns!ch [チャンネルメンション]\n```指定チャンネルで自動で戦うよ```"
        desc += "\ns!stop\n```上のシステムを止めるよ```"
        desc += "\ns!tstart\n```トレーニングをする（はずだ）よ```"
        desc += "\ns!tstop\n```トレーニングを終わらせる（はずだ）よ```"

        embed = discord.Embed(title="サクラ取扱説明書",description=f"{desc}",color=discord.Colour.green())
        await message.channel.send(embed=embed)


    me = client.user
    tao = client.get_user(526620171658330112)
    startlog_ch = client.get_channel(660440756514979880)
    stoplog_ch = client.get_channel(660440659995525143)


    if message.embeds and message.embeds[0].description and message.author == tao :
        dateTime = datetime.now()

        if f"{client.user.mention}はレベルアップした！" in message.embeds[0].description:
            lv = message.embeds[0].description.split("`")[1]
            embed = discord.Embed(
                title = "━LvUP━",
                description = f"**__{lv}__**",
                color = discord.Color.blue())
            embed.set_footer(text = datetime.now(JST))
            await asyncio.gather(*(c.send(embed=embed) for c in client.get_all_channels() if c.name == 'サクラレベルアップログ'))


    global test_ch
    global test_flag
    if message.content.startswith("s!ch "):
        test_ch_m = message.content.split('s!ch ')[1]
        test_ch = discord.utils.get(message.guild.text_channels, mention=test_ch_m)
        embed=discord.Embed(
            title=f"( 'ω'o[**testch**]oログ🌸",
            description=f'```使用者　│『{message.author}』\n使用者ID│『{message.author.id}』\n使用ch名│『{message.channel.name}』\n指定ch名│『{test_ch.name}』```チャンネルのメンション\n{test_ch.mention}'
        )
        embed.set_thumbnail(url=message.author.avatar_url)
        await startlog_ch.send(embed=embed)
        embed=discord.Embed(title='Play開始')
        await message.author.send(embed=embed)
        await asyncio.sleep(1)
        test_flag=True
        await test_ch.send("::attack")


    if message.content=='s!stop':
        test_flag=False
        await asyncio.sleep(5)
        await test_ch.send('::re')
        embed=discord.Embed(title='Play停止')
        await message.author.send(embed=embed)

    if message.channel == test_ch and message.embeds and test_flag==True:
        if message.embeds[0].title and 'が待ち構えている' in message.embeds[0].title:
            if test_ch.id == 660434662597984266:
                lv=message.embeds[0].title.split('Lv.')[1].split(' ')[0]
                await test_ch.edit(name=f'┃honpen┃lv.{lv}')
            await asyncio.sleep(1)
            await test_ch.send("::attack 先手必勝!!")

    if message.embeds and message.embeds[0].title and 'が待ち構えている' in message.embeds[0].title:
        lv=message.embeds[0].title.split('Lv.')[1].split(' ')[0]
        type=message.embeds[0].title.split('[')[1].split(']')[0]
        rank=message.embeds[0].title.split('【')[1].split('】')[0]
        name=message.embeds[0].title.split('】')[1].split('が待ち構えている')[0]
        image_url=message.embeds[0].image.url
        hp=message.embeds[0].title.split(':')[3]
        invite = await message.channel.create_invite()
        logch=client.get_channel(659965763050012703)
        exp=int(lv)
        if rank=='超強敵' or rank=='レア':
            exp=int(lv)*5
        elif rank=='激レア':

            exp=int(lv)*33
        elif rank=='強敵':
            exp=int(lv)*1.6
        elif rank=='超激レア':
            exp=int(lv)*100
        embed=discord.Embed(
        title=f'**モンスター出現ログ**\n**Name:**{name}\n**Type Rank:**\n{type}┃{rank}\n**Status:**\nLv.{lv}┃HP.{hp}\n**Exp:**\n{exp}',
        description = f"[このモンスターへの直通URL]({invite.url})",
        color=discord.Color.green())
        embed.set_thumbnail(url=image_url)
        embed.set_footer(text = datetime.now(JST))
        log_ch = client.get_channel(660445668074061834)
        await log_ch.send(embed=embed)


    if message.channel==test_ch and test_flag==True:
        if f"{me.display_name}はやられてしまった" in message.content:
            def test_check (d_msg):
                if d_msg.author != tao:
                    return 0
                if d_msg.channel!=test_ch:
                    return 0
                return 1
            try:
                t_res=await client.wait_for('message',timeout=3,check = test_check)
            except asyncio.TimeoutError:
                await test_ch.send('::item e 残念ペットは攻撃しなかったね！')
            else:
                if ']の攻撃' in t_res.content and 'のHP' in t_res.content:
                    await test_ch.send(f'::item e あ、petナイスアタック')



        elif f"{me.display_name}の攻撃" in message.content and "のHP" in message.content and not "やられてしまった" in message.content:

            def test_check (d_msg):
                if d_msg.author != tao:
                    return 0
                if d_msg.channel!=test_ch:
                    return 0
                return 1

            try:
                t_res=await client.wait_for('message',timeout=3,check = test_check)
            except asyncio.TimeoutError:
                await test_ch.send('::attack pet攻撃して欲しい')
            else:
                if ']の攻撃' in t_res.content and 'のHP' in t_res.content:
                    await test_ch.send(f'::attack ')


        elif message.embeds and message.embeds[0].description:
            if 'このチャンネルの全てのPETが全回復した！' in message.embeds[0].description:
                await asyncio.sleep(0.5)
                await test_ch.send('::attack 復活乁( ˙ ω˙乁)')

            elif f"{client.user.mention}はもうやられている！" in message.embeds[0].description:
                await asyncio.sleep(0.5)
                await test_ch.send("::i e 復活！")



    if message.content == "s!t":
        await message.channel.send("::t")

    global t_flag
    t_ch = client.get_channel(660456253524541456)
    if message.channel == t_ch and message.author == tao and t_flag==True:
        if message.embeds:
            if "正解" in message.embeds[0].description:
                await asyncio.sleep(0.3)
                await t_ch.send("::t")

    if message.channel == t_ch:
        if message.embeds:
            if message.embeds[0].footer.text and "TAOのトレーニング" in message.embeds[0].footer.text:
                await t_ch.send((message.embeds[0].description).split("`")[1])

    if message.content=='s!tstart':
        t_flag=True
        embed = discord.Embed(
        title=f"トレーニング開始\nt_flag = {t_flag}"
        )
        await message.author.send(embed = embed)

    if message.content=='s!tstop' :
        t_flag=False
        embed = discord.Embed(
        title=f"トレーニング終了\nt_flag = {t_flag}"
        )
        await message.author.send(embed = embed)

    if message.content.startswith("s!say "):
        await message.delete()
        await message.channel.send(message.content.split("s!say ")[1])


    if message.content == 's!st':
        await message.channel.send('::status window　私のステータスが見たいなんて、君もエッチだな')

    # 「りせ」と発言したら「::re」が返る処理
    if message.content == 's!re':
        await message.channel.send('::reset')

    if message.content == 's!atk':

        await message.channel.send("::attack")

    if message.content == 's!i e':
        await message.channel.send('::i e')


    if message.content == 's!i f' and message.author_id!=446610711230152706:
            await message.channel.send('::i f')


    if message.content == 's!rmap':
        await message.channel.send('::rmap')

    if message.content.startswith('s!sinka '):
        await message.channel.send('::sinka')
        reaction=message.content.split('s!sinka ')[1]
        def role_check(tao_msg):
            if not tao_msg.embeds:
                return 0
            if tao_msg.channel != message.channel:
                return 0
            return 1

        try:
            ans_msg = await client.wait_for('message', timeout=40, check=role_check)
        except:
            embed = discord.Embed(title='Error!!', description='もう一度試して見てね（￣▽￣;）\nもしかして以下の点が該当してないかな？\n‣TAOからの反応が40秒以内に来なかった\n‣TAOがオフライン\n‣TAOが修理中', color=discord.Color.green())
            await message.channel.send(embed=embed)
        else:
            await asyncio.sleep(2)
            await ans_msg.add_reaction(reaction)
    if message.content.startswith('s!role '):
        role_num = message.content.split('s!role ')[1]
        if not role_num in ["0","1","2","3"]:
            embed = discord.Embed(title='番号エラー!',
                              description=f'{role_num}に該当する役職はないよ!\n**役職番号**\n0│Adventure系\n1│Warrior系\n2│Mage系\n3│Thief系\nコマンドは`y!role [役職番号]`だよ。',
                              color=discord.Color.red())
            embed.set_footer(icon_url={message.author.avater_url},text=f"{message.author.name}")
            await message.channel.send(embed=embed)
        else:
            await message.channel.send('::role')

            def role_check(tao_msg):
                if not tao_msg.embeds:
                    return 0
                if tao_msg.channel != message.channel:
                    return 0
                return 1

            try:
                ans_msg = await client.wait_for('message', timeout=40, check=role_check)
            except:
                embed = discord.Embed(title='Error!!', description='もう一度試して見てね（￣▽￣;）\nもしかして以下の点が該当してないかな？\n‣TAOからの反応が40秒以内に来なかった\n‣TAOがオフライン\n‣TAOが修理中', color=discord.Color.green())
                await message.channel.send(embed=embed)
            else:
                await asyncio.sleep(2)
                if role_num == '0':
                    await ans_msg.add_reaction(f'\u0030\u20e3')
                elif role_num == '1':
                    await ans_msg.add_reaction(f'\u0031\u20e3')
                elif role_num == '2':
                    await ans_msg.add_reaction(f'\u0032\u20e3')
                elif role_num == '3':
                    await ans_msg.add_reaction(f'\u0033\u20e3')

    # 「あいてむ」と発言したら「::i」が返る処理
    if message.content == 's!i':
        await message.channel.send('::i')

    # 「ろぐいん」と発言したら「::login」が返る処理
    if message.content == 's!login':
        await message.channel.send('::login')



client.run(TOKEN)
