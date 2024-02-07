import discord


class DiscordEmbed:
    def __init__(self):
        self.embed = discord.Embed(
            title="문제 제공 챗봇",
            description="문제를 제공해드립니다.",
            url="https://github.com/k4west",
            color=discord.Color.random(),
        )

    def greeting(self, current_time):
        self.embed.set_thumbnail(url="https://fakeimg.pl/350x200/?text=savvy_quiz")
        self.embed.add_field(name="현재 시간", value=str(current_time), inline=False)
        self.embed.add_field(
            name="문제 요청 방법",
            value="`!문제` 또는 `!quiz`를 입력해주세요.",
            inline=False,
        )
        return self.embed

    def quiz(self, quizzes):
        self.embed.set_thumbnail(url=f"https://fakeimg.pl/400x300/?text=You_can_do_it!")
        print("문제")
        for idx, quiz in enumerate(quizzes, 1):
            quiz = quiz.split("\n")
            self.embed.add_field(
                name=f"문제_{idx}",
                value=f"[{quiz[0]}]({quiz[3]})",
                inline=True,
            )
            self.embed.add_field(
                name="난이도",
                value=quiz[1],
                inline=True,
            )
            self.embed.add_field(
                name="태그",
                value=quiz[2].replace("'", "`"),
                inline=False,
            )
            print(quiz[0], quiz[3])
        return self.embed

    def levels(self):
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
        return embed

    def tags(self):
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
        return embed
