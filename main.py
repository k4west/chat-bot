import os
from datetime import datetime
import asyncio
import discord
from discord.ext import commands
from utils.quiz_query import QuizQuery
from utils.quiz_render import QuizRender
from utils.mk_embed import DiscordEmbed
from fastapi import FastAPI

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

TOKEN = os.environ["DISCORD_TOKEN"]
src = "./data/quizzes.pkl"
quiz_channel_id = 1204354643715428362
sessac_channel_id = 1196688402880401490


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user.name}")
    quiz_ch = bot.get_channel(quiz_channel_id)

    await bot.change_presence(activity=discord.Game(name="문제를 제공해드립니다."))
    await quiz_ch.send(embed=DiscordEmbed().greeting(datetime.now()))

    sessac_ch = bot.get_channel(sessac_channel_id)  # 새싹X솔트룩스 LLM 잡담방
    while True:
        if datetime.now().weekday() < 5:
            if (cur_time := str(datetime.now().strftime("%H:%M"))) == "09:00":
                await quiz_ch.send("오늘도 열심히 풀어봅시다!")
                await sessac_ch.send(cur_time + "입니다.")
                # select_quizzes params: s=최소 난이도, e=최대 난이도, n=문제 수, tags=문제 태그, level=특정 난이도
                quizzes = QuizQuery(src=src).filter_quizzes(
                    s=1, e=7, n=2, tags=None, level=-1
                )
                result = QuizRender()
                quizzes = result.make_content(quizzes, new=True)

                if quizzes:
                    await sessac_ch.send(embed=DiscordEmbed().quiz(quizzes))

                else:
                    await sessac_ch.send("해당하는 문제가 없습니다.")
        else:
            if (cur_time := str(datetime.now().strftime("%H:%M"))) == "09:00":
                await quiz_ch.send("주말인데, 쉬엄쉬엄 하세요~")
        await asyncio.sleep(60)


@bot.command(name="문제", aliases=["quiz"])
async def quiz(ctx):
    time = 15.0

    def check_auth(message):
        return message.author == ctx.author

    # Asking baekjoon id
    baekjoon_id, s, e, n, tags, level = "", 3, 7, 2, None, -1
    req_id = await ctx.send("백준 아이디를 입력해 주세요.")
    try:
        baekjoon_id = await bot.wait_for("message", timeout=time, check=check_auth)
    except:
        pass
    quiz_query = QuizQuery(src=src, user_name=baekjoon_id.content)
    await req_id.delete()

    # Asking levels of quiz to solve
    levels_msg = DiscordEmbed().levels()
    level_list = await ctx.send(embed=levels_msg)
    req_level = await ctx.send("어떤 난이도의(0~30) 문제를 풀겠습니까? (ex): 3~7, 5)")
    try:
        level_m = await bot.wait_for("message", timeout=time, check=check_auth)
        for sep in "~-,":
            if sep in (level_ := level_m.content):
                s, e = map(int, level_.split(sep))
                break
        else:
            level = int(level_)
    except:
        pass
    await level_list.delete()
    await req_level.delete()

    # Asking tags of quiz to solve
    tags_msg = DiscordEmbed().tags()
    tag_list = await ctx.send(embed=tags_msg)
    req_tag = await ctx.send(
        """어떤 태그의 문제를 풀겠습니까?
        (ex): 수학, 다이나믹 프로그래밍, 자료 구조, 그래프 이론, 문자열, 정렬, 최단 경로 등등)"""
    )
    try:
        tags_m = await bot.wait_for("message", timeout=time, check=check_auth)
    except:
        pass
    tags = tags_m.content.split(",")
    await tag_list.delete()
    await req_tag.delete()

    # Asking the number of quiz to solve
    req_n = await ctx.send("풀고 싶은 문제수(<=8)를 입력해 주세요.")
    try:
        n_m = await bot.wait_for("message", timeout=time, check=check_auth)
        n = int(n_m.content)
    except:
        pass
    await req_n.delete()

    # filter quizzes
    quizzes = quiz_query.filter_quizzes(s=s, e=e, n=n, tags=tags, level=level)
    # select_quiz param: ids=문제 ID
    # quizzes2 = quiz_query.select_quizzes([8564])
    result = QuizRender()
    quizzes = result.make_content(quizzes, new=True)
    # result2 = result.make_content(quizzes2, new=True)

    if quizzes:
        await ctx.send(embed=DiscordEmbed().quiz(quizzes))
    else:
        await ctx.send("해당하는 문제가 없습니다.")

    await baekjoon_id.delete()
    await level_m.delete()
    await tags_m.delete()
    await n_m.delete()


app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


asyncio.create_task(bot.start(TOKEN))
