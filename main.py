import datetime
import random
import math
import discord
import asyncio
import matplotlib.pyplot as plt
import sqlite3
from discord.ext import commands
from datetime import datetime
bot = commands.Bot(command_prefix='!')

con = sqlite3.connect("Test.db", isolation_level = None)
cur = con.cursor()
cur.execute("CREATE TABLE IF NOT EXISTS User_Info(id INTEGER PRIMARY KEY, coin INTEGER, money INTEGER)")

arr = []
brr = []
ttt = []
cntk = 0
prevvi = 100000
moneyhave = 10000000
coinhave = 0
coinp = 100000
flag = True

token = "OTE0NTExNzQ0MjE3NTM0NDY0.YaOHbg.bpaUxI0sff9Jep1SQhxOYvVTu44"

def checkuser(id):
    alr_exist = []
    con = sqlite3.connect(r'Test.db', isolation_level = None)
    cur = con.cursor()
    cur.execute("SELECT id FROM User_Info WHERE id = ?", (id,))
    rows = cur.fetchall()
    for i in rows:
        alr_exist.append(i[0])

    if id not in alr_exist:
        return 0
    elif id in alr_exist:
        return 1
    con.close()


@bot.event
async def on_message(msg):
    if(msg.author.bot): return None
    await bot.process_commands(msg)

@bot.event
async def on_ready():
    global arr, cntk, ttt, prevvi
    global coinp
    await bot.change_presence(status=discord.Status.online, activity=discord.Game('HRX COIN!'))
    print('[DEBUG]=================\nbot status : on\n=================')
    channel = bot.get_channel(id=916560954853032009)
    while True:
        y = random.randint(-1000,1000)
        coinp += y
        coinp = min(200000, coinp)
        coinp = max(10000, coinp)
        arr.append(coinp)
        ttt.append(cntk)
        cntk+=1
        now = datetime.now()
        if(coinp >= int(prevvi*1.1)):
            embed = discord.Embed(title='HRX코인 거래소',
                                  description='상승성완화(UL) 발동!\n과도한 상승을 막기위해 1분간 가격변동을 제한합니다.',
                                  colour=0xD0F5A9)
            embed.add_field(name='> 현재가', value='{}원'.format(format(coinp, ",")))
            embed.set_footer(text='기준일시 : {}시 {}분 {}초'.format(now.hour, now.minute, now.second))
            await channel.send(embed=embed)
            await asyncio.sleep(60)
            prevvi = coinp
        elif(coinp <= int(prevvi*0.9)):
            embed = discord.Embed(title='HRX코인 거래소',
                                  description='하락성완화(DL) 발동!\n과도한 하락을 막기위해 1분간 가격변동을 제한합니다.',
                                  colour=0x0080FF)
            embed.add_field(name='> 현재가', value='{}원'.format(format(coinp, ",")))
            embed.set_footer(text='기준일시 : {}시 {}분 {}초'.format(now.hour, now.minute, now.second))
            await channel.send(embed=embed)
            await asyncio.sleep(60)
            prevvi = coinp
        else:
            await asyncio.sleep(30)

@bot.command()
async def 가입신청(ctx):
    id = ctx.author.id
    con = sqlite3.connect(r'Test.db', isolation_level=None)
    cur = con.cursor()
    chk = checkuser(id)
    if(chk==0):
        cur.execute("INSERT INTO User_Info VALUES(?, ?, ?)", (id, 0, 10000000))
        await ctx.channel.send(f'{ctx.message.author.mention} 가입완료')
    elif(chk==1):
        await ctx.channel.send("STOP!")
    con.close()

@bot.command()
async def 탈퇴(ctx):
    id = ctx.author.id
    con = sqlite3.connect(r'Test.db', isolation_level=None)
    cur = con.cursor()
    chk = checkuser(id)
    if(chk==0):
        pass
    elif(chk==1):
        cur.execute("DELETE FROM User_Info WHERE id = ?", (id,))
    con.close()

@bot.command()
async def 지갑(ctx):
    await ctx.channel.send(f'{ctx.message.author.mention}')
    tid = ctx.author.id
    con = sqlite3.connect(r'Test.db', isolation_level=None)
    cur = con.cursor()
    chk = checkuser(tid)
    if (chk == 0):
        embed = discord.Embed(title='HRX코인 거래소',
                              description=f'{ctx.message.author.mention}님의 지갑현황을 조회할 수 없습니다.',
                              colour=0xFA5858)
        embed.add_field(name='> 실패사유', value='DB에 정보가 없습니다.\n!가입신청 을 입력해주세요.')
        await ctx.channel.send(embed=embed)
    elif (chk == 1):
        cur.execute("SELECT money FROM User_Info WHERE id = ?", (tid, ))
        k1 = int(cur.fetchone()[0])
        cur.execute("SELECT coin FROM User_Info WHERE id = ?", (tid, ))
        k2 = int(cur.fetchone()[0])
        embed = discord.Embed(title='HRX코인 거래소',
                              description=f'{ctx.message.author.mention}님의 지갑현황입니다.',
                              colour=0xD0F5A9)
        embed.add_field(name='> 지갑현황', value='HRX : {}개\n잔고 : {}원\n추정자산 : {}원'.format(format(k2, ","), format(k1, ","), format(k2*coinp + k1, ",")))
        await ctx.channel.send(embed=embed)
    con.close()

@bot.command()
async def 코인시세(ctx):
    now = datetime.now()
    await ctx.channel.send(f'{ctx.message.author.mention}')
    embed = discord.Embed(title='HRX코인 거래소',
                          description='현재 HRX코인 시세를 알려드립니다.',
                          colour=0xD0F5A9)
    embed.add_field(name='> 현재가', value='{}원'.format(format(coinp,",")))
    embed.set_footer(text='기준일시 : {}시 {}분 {}초'.format(now.hour, now.minute, now.second))
    await ctx.channel.send(embed=embed)

@bot.command()
async def 코인매수(ctx, *input):
    now = datetime.now()
    await ctx.channel.send(f'{ctx.message.author.mention}')
    try:
        tid = ctx.author.id
        con = sqlite3.connect(r'Test.db', isolation_level=None)
        cur = con.cursor()
        chk = checkuser(tid)
        if (chk == 0):
            embed = discord.Embed(title='HRX코인 거래소',
                                  description=f'{ctx.message.author.mention}님의 거래결과를 알려드립니다.',
                                  colour=0xFA5858)
            embed.add_field(name='> 거래여부', value='실패')
            embed.add_field(name='> 실패사유', value='DB에 정보가 없습니다.\n!가입신청 을 입력해주세요.')
            embed.set_footer(text='거래일시 : {}시 {}분 {}초'.format(now.hour, now.minute, now.second))
            await ctx.channel.send(embed=embed)
        elif (chk == 1):
            cur.execute("SELECT money FROM User_Info WHERE id = ?", (tid, ))
            k = int(cur.fetchone()[0])
            r = int(input[0])
            if(r==0):
                embed = discord.Embed(title='HRX코인 거래소',
                                      description=f'{ctx.message.author.mention}님의 거래결과를 알려드립니다.',
                                      colour=0xFA5858)
                embed.add_field(name='> 거래여부', value='실패')
                embed.add_field(name='> 실패사유', value='입력에 불필요한 입력이 있습니다.\n숫자 또는 1 이상의 숫자만 입력해주세요.')
                embed.set_footer(text='거래일시 : {}시 {}분 {}초'.format(now.hour, now.minute, now.second))
                await ctx.channel.send(embed=embed)
            elif(k/r <= 0 or k-coinp*r<0):
                embed = discord.Embed(title='HRX코인 거래소',
                                      description=f'{ctx.message.author.mention}님의 거래결과를 알려드립니다.',
                                      colour=0xFA5858)
                embed.add_field(name='> 거래여부', value='실패')
                embed.add_field(name='> 실패사유', value='잔고가 부족합니다.')
                embed.set_footer(text='거래일시 : {}시 {}분 {}초'.format(now.hour, now.minute, now.second))
                await ctx.channel.send(embed=embed)
            else:
                kk = -1*r*coinp
                con.close()
                con = sqlite3.connect(r'Test.db', isolation_level=None)
                cur = con.cursor()
                cur.execute("UPDATE User_info SET money = money + ? WHERE id = ?", (int(kk),tid,))
                cur.execute("UPDATE User_info SET coin = coin + ? WHERE id = ?", (int(r),tid,))
                cur.execute("SELECT money FROM User_Info WHERE id = ?", (tid, ))
                m1 = int(cur.fetchone()[0])
                cur.execute("SELECT coin FROM User_Info WHERE id = ?", (tid, ))
                c1 = int(cur.fetchone()[0])
                embed = discord.Embed(title='HRX코인 거래소',
                                      description=f'{ctx.message.author.mention}님의 거래결과를 알려드립니다.',
                                      colour=0xD0F5A9)
                embed.add_field(name='> 거래여부', value='성공')
                embed.add_field(name='> 현재가', value='{}원'.format(format(coinp, ",")))
                embed.add_field(name='> 거래개수', value='{}개'.format(format(int(input[0]), ",")))
                embed.add_field(name='> 지갑현황', value='HRX : {}개\n잔고 : {}원'.format(format(c1, ","), format(m1, ",")))
                embed.set_footer(text='거래일시 : {}시 {}분 {}초'.format(now.hour, now.minute, now.second))
                await ctx.channel.send(embed=embed)
    except:
        embed = discord.Embed(title='HRX코인 거래소',
                              description=f'{ctx.message.author.mention}님의 거래결과를 알려드립니다.',
                              colour=0xFA5858)
        embed.add_field(name='> 거래여부', value='실패')
        embed.add_field(name='> 실패사유', value='입력에 불필요한 입력이 있습니다.\n!코인매수 [개수(숫자)] 형식으로 입력해주세요.')
        embed.set_footer(text='거래일시 : {}시 {}분 {}초'.format(now.hour, now.minute, now.second))
        await ctx.channel.send(embed=embed)
    con.close()

@bot.command()
async def 코인매도(ctx, *input):
    now = datetime.now()
    await ctx.channel.send(f'{ctx.message.author.mention}')
    try:
        tid = ctx.author.id
        con = sqlite3.connect(r'Test.db', isolation_level=None)
        cur = con.cursor()
        chk = checkuser(tid)
        if (chk == 0):
            embed = discord.Embed(title='HRX코인 거래소',
                                  description=f'{ctx.message.author.mention}님의 거래결과를 알려드립니다.',
                                  colour=0xFA5858)
            embed.add_field(name='> 거래여부', value='실패')
            embed.add_field(name='> 실패사유', value='DB에 정보가 없습니다.\n!가입신청 을 입력해주세요.')
            embed.set_footer(text='거래일시 : {}시 {}분 {}초'.format(now.hour, now.minute, now.second))
            await ctx.channel.send(embed=embed)
        elif (chk == 1):
            cur.execute("SELECT coin FROM User_Info WHERE id = ?", (tid, ))
            k = int(cur.fetchone()[0])
            r = int(input[0])
            if(r==0):
                embed = discord.Embed(title='HRX코인 거래소',
                                      description=f'{ctx.message.author.mention}님의 거래결과를 알려드립니다.',
                                      colour=0xFA5858)
                embed.add_field(name='> 거래여부', value='실패')
                embed.add_field(name='> 실패사유', value='입력에 불필요한 입력이 있습니다.\n숫자 또는 1 이상의 숫자만 입력해주세요.')
                embed.set_footer(text='거래일시 : {}시 {}분 {}초'.format(now.hour, now.minute, now.second))
                await ctx.channel.send(embed=embed)
            elif(k-r<0 or k==0):
                embed = discord.Embed(title='HRX코인 거래소',
                                      description=f'{ctx.message.author.mention}님의 거래결과를 알려드립니다.',
                                      colour=0xFA5858)
                embed.add_field(name='> 거래여부', value='실패')
                embed.add_field(name='> 실패사유', value='잔고가 부족합니다.')
                embed.set_footer(text='거래일시 : {}시 {}분 {}초'.format(now.hour, now.minute, now.second))
                await ctx.channel.send(embed=embed)
            else:
                kk = r*coinp
                con.close()
                con = sqlite3.connect(r'Test.db', isolation_level=None)
                cur = con.cursor()
                cur.execute("UPDATE User_info SET money = money + ? WHERE id = ?", (int(kk), tid, ))
                cur.execute("UPDATE User_info SET coin = coin + ? WHERE id = ?", (int(-r), tid, ))
                cur.execute("SELECT money FROM User_Info WHERE id = ?", (tid, ))
                m1 = int(cur.fetchone()[0])
                cur.execute("SELECT coin FROM User_Info WHERE id = ?", (tid, ))
                c1 = int(cur.fetchone()[0])
                embed = discord.Embed(title='HRX코인 거래소',
                                      description=f'{ctx.message.author.mention}님의 거래결과를 알려드립니다.',
                                      colour=0xD0F5A9)
                embed.add_field(name='> 거래여부', value='성공')
                embed.add_field(name='> 현재가', value='{}원'.format(format(coinp, ",")))
                embed.add_field(name='> 거래개수', value='{}개'.format(format(int(input[0]), ",")))
                embed.add_field(name='> 지갑현황', value='HRX : {}개\n잔고 : {}원'.format(format(c1, ","), format(m1, ",")))
                embed.set_footer(text='거래일시 : {}시 {}분 {}초'.format(now.hour, now.minute, now.second))
                await ctx.channel.send(embed=embed)
    except:
        embed = discord.Embed(title='HRX코인 거래소',
                              description=f'{ctx.message.author.mention}님의 거래결과를 알려드립니다.',
                              colour=0xFA5858)
        embed.add_field(name='> 거래여부', value='실패')
        embed.add_field(name='> 실패사유', value='입력에 불필요한 입력이 있습니다.\n!코인매도 [개수(숫자)] 형식으로 입력해주세요.')
        embed.set_footer(text='거래일시 : {}시 {}분 {}초'.format(now.hour, now.minute, now.second))
        await ctx.channel.send(embed=embed)
    con.close()

@bot.command()
async def 코인차트(ctx):
    plt.figure(figsize=(6.5, 5))
    plt.fill_between(ttt, arr, color='blue', alpha=0.3)
    plt.axhline(arr[len(arr)-1], 0, 1, color='lightgray', linestyle='--', linewidth=2)
    plt.axhline(int(prevvi*1.1), 0, 1, color='red', linestyle='--', linewidth=2)
    plt.axhline(int(prevvi*0.9), 0, 1, color='blue', linestyle='--', linewidth=2)
    plt.xlim(max(len(arr)-50, 0), len(arr))
    plt.ylim(coinp-15000, coinp+15000)
    plt.xlabel('time')
    plt.ylabel('price')
    plt.legend(['now_price', 'UL', 'DL', 'price'])
    plt.title('Haru Coin Price Graph')
    plt.grid(True)
    plt.savefig(fname='plot')
    await ctx.channel.send(file=discord.File('plot.png'))

bot.run(token)