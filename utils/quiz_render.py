class QuizRender:

    def __init__(self, url="https://www.acmicpc.net/problem"):

        self.url = url
        self.results = []
        self.level_mapping = {
            0: "Unrated",
            1: "Bronze V",
            2: "Bronze IV",
            3: "Bronze III",
            4: "Bronze II",
            5: "Bronze I",
            6: "Silver V",
            7: "Silver IV",
            8: "Silver III",
            9: "Silver II",
            10: "Silver I",
            11: "Gold V",
            12: "Gold IV",
            13: "Gold III",
            14: "Gold II",
            15: "Gold I",
            16: "Platinum V",
            17: "Platinum IV",
            18: "Platinum III",
            19: "Platinum II",
            20: "Platinum I",
            21: "Diamond V",
            22: "Diamond IV",
            23: "Diamond III",
            24: "Diamond II",
            25: "Diamond I",
            26: "Ruby V",
            27: "Ruby IV",
            28: "Ruby III",
            29: "Ruby II",
            30: "Ruby I",
        }

    def make_content(self, quizzes, new=True):

        # keys = ("문제 이름: ", "난이도: ", "태그: ", "")
        tmp = []

        # new = False 할 경우 이전 생성한 문제 리스트와 합쳐집니다.
        if new:
            self.results = []

        if not quizzes.empty:
            for _, quiz in quizzes.iterrows():
                tmp.append(
                    (
                        quiz["titleKo"],
                        self.level_mapping[quiz["level"]],
                        f"{quiz['tags']}",
                        "/".join((self.url, str(quiz["problemId"]))),
                    )
                )
        else:
            print("문제가 존재하지 않습니다.")

        for result in tmp:
            # self.results.append("\n".join((k + v for k, v in zip(keys, result))) + "\n")
            self.results.append("\n".join(result))
        if not new:
            self.results = list(set(self.results))

        return self.results
