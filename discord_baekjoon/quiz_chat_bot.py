import os
from datetime import datetime
import asyncio
import discord
from discord.ext import commands

from quiz_query import QuizQuery
from quiz_render import QuizRender


intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

TOKEN = os.environ["DISCORD_TOKEN"]


# 봇이 켜졌을 때
@bot.event
async def on_ready():
    print(f"Logged in as {bot.user.name}")
    quiz_ch = bot.get_channel(1204354643715428362)

    # 현재 시간을 가져옴
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M")
    embed = discord.Embed(
        title="문제 제공 챗봇",
        description="문제를 제공해드립니다.",
        url="https://github.com/k4west",
        color=discord.Color.random(),
    )
    embed.set_thumbnail(url="https://fakeimg.pl/350x200/?text=savvy_quiz")
    embed.add_field(name="현재 시간", value=str(current_time), inline=False)
    embed.add_field(
        name="문제 요청 방법",
        value="`!문제` 또는 `!quiz`를 입력해주세요.",
        inline=False,
    )
    await bot.change_presence(activity=discord.Game(name="문제를 제공해드립니다."))
    if datetime.now().weekday() < 5:
        await quiz_ch.send("오늘도 열심히 풀어봅시다!")
    else:
        await quiz_ch.send("주말인데, 쉬엄쉬엄 하세요~")

    await quiz_ch.send(embed=embed)

    sessac_ch = bot.get_channel(1196688402880401490)  # 새싹X솔트룩스 LLM 잡담방

    while True:
        if datetime.now().weekday() < 5:
            if (cur_time := str(datetime.now().strftime("%H:%M"))) == "09:00":
                await sessac_ch.send(cur_time + "입니다.")
                quiz_query = QuizQuery(src="quizzes.pkl")
                quizzes = quiz_query.filter_quizzes(s=1, e=7, n=2, tags=None, level=-1)
                result = QuizRender()
                _quizzes = result.make_content(quizzes, new=True)

                if _quizzes:
                    embed = discord.Embed(
                        title="문제 제공 챗봇",
                        description="문제를 제공해드립니다.",
                        url="https://github.com/k4west",
                        color=discord.Color.random(),
                    )
                    embed.set_thumbnail(
                        url=f"https://fakeimg.pl/600x500/?text=You_can_do_it!"
                    )
                    for idx, _quiz in enumerate(_quizzes, 1):
                        _quiz = _quiz.split("\n")
                        embed.add_field(
                            name=f"문제_{idx}",
                            value="",
                            inline=False,
                        )
                        embed.add_field(
                            name="문제",
                            value=f"[{_quiz[0]}]({_quiz[3]})",
                            inline=True,
                        )
                        embed.add_field(
                            name="난이도",
                            value=_quiz[1],
                            inline=True,
                        )
                        embed.add_field(
                            name="태그",
                            value=_quiz[2].replace("'", "`"),
                            inline=False,
                        )

                    await sessac_ch.send(embed=embed)

                else:
                    await sessac_ch.send("해당하는 문제가 없습니다.")
        await asyncio.sleep(60)


@bot.command(name="문제", aliases=["quiz"])
async def quiz(ctx):

    timeout = 15.0

    def check_auth(message):
        return message.author == ctx.author

    # Asking baekjoon id
    baekjoon_id, s, e, n, tags, level = "", 3, 7, 2, None, -1
    chat_bot = await ctx.send("문제를 제공하는 챗봇입니다.")

    req_id = await ctx.send("백준 아이디를 입력해 주세요.")
    try:
        baekjoon_id = await bot.wait_for("message", timeout=timeout, check=check_auth)
    except:
        pass
    else:
        quiz_query = QuizQuery(src="quizzes.pkl", user_name=baekjoon_id.content)
    await req_id.delete()

    # Asking levels of quiz to solve
    embed = discord.Embed(
        title="난이도!",
        description="""원하는 난이도를 입력하거나
        `~`로 이어서 입력해주세요.""",
        color=discord.Color.random(),
    )
    embed.add_field(name="Unranked", value="0")
    embed.add_field(name="브론즈", value="1~5")
    embed.add_field(name="실버", value="6~10")
    embed.add_field(name="골드", value="11~15")
    embed.add_field(name="플레티넘", value="16~20")
    embed.add_field(name="다이아몬드", value="21~25")
    embed.add_field(name="루비", value="26~30")
    level_list = await ctx.send(embed=embed)
    req_level = await ctx.send("어떤 난이도의 문제를 풀겠습니까? (ex): 3~7, 5)")
    try:
        _level = await bot.wait_for("message", timeout=timeout, check=check_auth)
        _level = _level.content
        if "~" in _level:
            s, e = map(int, _level.split("~"))
        else:
            level = int(_level)
    except:
        pass

    await level_list.delete()
    await req_level.delete()

    # Asking tags of quiz to solve
    embed = discord.Embed(
        title="태그!",
        description="""원하는 태그를 입력하세요.
        상관 없으면 엔터를 치거나 기다려주세요.""",
        color=discord.Color.random(),
    )
    embed.add_field(
        name="예시",
        value="""`수학`, `구현`, `다이나믹 프로그래밍`, `자료 구조`, `그래프 이론`, `그리디 알고리즘`, 
        `문자열`, `브루트포스 알고리즘`, `그래프 탐색`, `정렬`, `기하학`, `정수론`, `트리`, 
        `이분 탐색`, `너비 우선 탐색`, `깊이 우선 탐색`, `최단 경로`, `데이크스트라`, `백트래킹`""",
    )
    tag_list = await ctx.send(embed=embed)
    req_tag = await ctx.send(
        "어떤 태그의 문제를 풀겠습니까? \n(ex): 수학, 다이나믹 프로그래밍, 자료 구조, 그래프 이론, 문자열, 정렬, 최단 경로)"
    )
    try:
        tags = await bot.wait_for("message", timeout=timeout, check=check_auth)
    except:
        pass
    else:
        tags = tags.content.split(",")
    await tag_list.delete()
    await req_tag.delete()

    # Asking the number of quiz to solve
    req_n = await ctx.send("풀고 싶은 문제수를 입력해 주세요.")
    try:
        n = await bot.wait_for("message", timeout=timeout, check=check_auth)
    except:
        pass
    else:
        n = int(n.content)
    await req_n.delete()

    # select_quizzes params: s=최소 난이도, e=최대 난이도, n=문제 수, tags=문제 태그, level=특정 난이도
    quizzes = quiz_query.filter_quizzes(s=s, e=e, n=n, tags=tags, level=level)

    # select_quiz param: ids=문제 ID
    # quizzes2 = quiz_query.select_quizzes([8564])
    result = QuizRender()
    _quizzes = result.make_content(quizzes, new=True)
    # result2 = result.make_content(quizzes2, new=True)

    if _quizzes:
        embed = discord.Embed(
            title="문제 제공 챗봇",
            description="문제를 제공해드립니다.",
            url="https://github.com/k4west",
            color=discord.Color.random(),
        )
        embed.set_thumbnail(url=f"https://fakeimg.pl/500x500/?text=You_can_do_it!")
        for idx, _quiz in enumerate(_quizzes, 1):
            _quiz = _quiz.split("\n")
            embed.add_field(
                name=f"문제_{idx}",
                value="",
                inline=False,
            )
            embed.add_field(
                name="문제",
                value=f"[{_quiz[0]}]({_quiz[3]})",
                inline=True,
            )
            embed.add_field(
                name="난이도",
                value=_quiz[1],
                inline=True,
            )
            embed.add_field(
                name="태그",
                value=_quiz[2].replace("'", "`"),
                inline=False,
            )

        await ctx.send(embed=embed)
    else:
        await ctx.send("해당하는 문제가 없습니다.")
    await chat_bot.delete()


bot.run(TOKEN)
