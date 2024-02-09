import os
from datetime import datetime
import pytz
import asyncio
import discord
from discord.ext import commands
from quiz_query import QuizQuery
from quiz_render import QuizRender
from level_button import LevelButton
from mk_embed import DiscordEmbed

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

TOKEN = os.environ["DISCORD_TOKEN"]
src = "../data/quizzes.pkl"
quiz_channel_id = 1204354643715428362

# 한국 시간대로 변경합니다.
korea_tz = pytz.timezone("Asia/Seoul")


def kor_now():
    # 현재 시간을 UTC로 가져옵니다.
    now_utc = datetime.now(pytz.utc)
    now_korea = now_utc.astimezone(korea_tz)
    return now_korea


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user.name}")
    quiz_ch = bot.get_channel(quiz_channel_id)

    await bot.change_presence(activity=discord.Game(name="문제를 제공해드립니다."))
    await quiz_ch.send(embed=DiscordEmbed().greeting(kor_now()))

    while True:
        if (cur_time := str(kor_now().strftime("%H:%M"))) == "09:00":
            if kor_now().weekday() < 5:
                await quiz_ch.send(cur_time + "입니다. 오늘도 열심히 풀어봅시다!")
                # select_quizzes params: s=최소 난이도, e=최대 난이도, n=문제 수, tags=문제 태그, level=특정 난이도
                quizzes = QuizQuery(src=src).filter_quizzes(
                    s=1, e=7, n=2, tags=[], level=-1
                )
                result = QuizRender()
                quizzes = result.make_content(quizzes, new=True)

                if quizzes:
                    await quiz_ch.send(embed=DiscordEmbed().quiz(quizzes))

                else:
                    await quiz_ch.send("해당하는 문제가 없습니다.")
            else:
                await quiz_ch.send("주말인데, 쉬엄쉬엄 하세요~")
        await asyncio.sleep(60)


@bot.command(name="ㅇ문제", aliases=[" 문제", "quiz", " quiz"])
async def quiz(ctx):
    time = 15.0
    button_dict = {
        "": "직접 입력",
        "1~5": "Bronze",
        "6~10": "Silver",
        "11~15": "Gold",
        "16~20": "Platinum",
        "21~25": "Diamond",
        "26~30": "Ruby",
    }

    def check_auth(message):
        return message.author == ctx.author

    # Asking baekjoon id
    baekjoon_id, s, e, n, tags, level = "", 3, 7, 2, [], -1
    baekjoon_id_m, level_m, tags_m, n_m = "", "", "", ""
    req_id = await ctx.send("백준 아이디를 입력해 주세요.", delete_after=time)
    try:
        baekjoon_id_m = await bot.wait_for("message", timeout=time, check=check_auth)
        quiz_query = QuizQuery(
            src=src, user_name=(baekjoon_id := baekjoon_id_m.content)
        )
    except:
        quiz_query = QuizQuery(src=src, user_name=baekjoon_id)
        print(baekjoon_id, "beakjoon")

    print(baekjoon_id)

    # Asking levels of quiz to solve
    levels_msg = DiscordEmbed().levels()
    await ctx.send(embed=levels_msg, delete_after=20)
    await ctx.send("버튼은 10초 안에 누르셔야 합니다~~", delete_after=time)
    await ctx.send("selcet a level", view=(lbs := LevelButton()), delete_after=time)

    await asyncio.sleep(10)
    level_ = (await ctx.send(button_dict[lbs.level], delete_after=5)).content

    if level_ == "":
        req_level = await ctx.send(
            "어떤 난이도의(0~30) 문제를 풀겠습니까? (ex): 3~7, 5)"
        )
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
        await req_level.delete()
    else:
        s, e = map(int, level_.split("~"))
    print("s, e, level:", s, e, level)

    # Asking tags of quiz to solve
    tags_msg = DiscordEmbed().tags()
    await ctx.send(embed=tags_msg, delete_after=time)
    await ctx.send(
        """어떤 태그의 문제를 풀겠습니까?
        (ex): 수학, 다이나믹 프로그래밍, 자료 구조, 그래프 이론, 문자열, 정렬, 최단 경로 등등)""",
        delete_after=time,
    )
    try:
        tags_m = await bot.wait_for("message", timeout=time, check=check_auth)
        tags = tags_m.content.split(",")
    except:
        pass

    # Asking the number of quiz to solve
    await ctx.send("풀고 싶은 문제수(<=8)를 입력해 주세요.", delete_after=time)
    try:
        n_m = await bot.wait_for("message", timeout=time, check=check_auth)
        n = int(n_m.content)
    except:
        pass

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
        await ctx.send("해당하는 문제가 없습니다.", delete_after=time * 10)

    for mm in (baekjoon_id_m, level_m, tags_m, n_m):
        try:
            await mm.delete()
        except:
            pass


@bot.command(name="ㅁ문제", aliases=["qquiz", " ㅁ문제", " qquiz"])
async def quiz(ctx, baekjoon_id="", s=2, e=7, n=2, tags=[], level=-1):
    time = 15
    quiz_query = QuizQuery(src=src, user_name=baekjoon_id)
    print(
        f"""
            baekjoon_id: {baekjoon_id} 
            s: {s} 
            e: {e} 
            n: {n} 
            tags: {tags} 
            level: {level}"""
    )

    # filter quizzes
    quizzes = quiz_query.filter_quizzes(s=s, e=e, n=n, tags=tags, level=level)
    result = QuizRender()
    quizzes = result.make_content(quizzes, new=True)

    if quizzes:
        await ctx.send(embed=DiscordEmbed().quiz(quizzes))
    else:
        await ctx.send("해당하는 문제가 없습니다.", delete_after=time * 10)


@bot.command(name="태그", aliases=[" 태그", "tag", " tag", "tags", " tags"])
async def quiz(ctx):
    # Asking tags list
    tags_list = DiscordEmbed().tags_list(src=src.replace("quizzes", "quiz_tags"))
    await ctx.send(embed=tags_list)


bot.run(TOKEN)
