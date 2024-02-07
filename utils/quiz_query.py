import re
import requests
import pandas as pd
from lxml import html


class QuizQuery:

    def __init__(self, src="../data/quizzes.pkl", user_name: str = None):

        self.src = src
        self.quizzes = pd.read_pickle(self.src).dropna(axis=0)

        # 한글, 영어, 숫자, 특수기호를 제외한 문자 탐색 > 다른 언어로 작성된 문제는 어려워서;;
        pattern = re.compile(
            r"[^a-zA-Z0-9ㄱ-ㅎㅏ-ㅣ가-힣/s!@#$%^&*()-_=+`~{}\[\]|;:\'\",.<>?]+"
        )
        self.quizzes = self.quizzes[
            self.quizzes["titleKo"].apply(lambda x: not bool(re.match(pattern, x)))
        ]
        self.user_name = user_name

        # 푼 문제 제외
        if self.user_name:
            headers = {"User-Agent": "Mozilla/5.0"}
            url = f"https://www.acmicpc.net/user/{self.user_name}"
            xpath = '//div[@class="problem-list"]/a/text()'

            response = requests.get(url, headers=headers)
            solved_id = set(map(int, html.fromstring(response.text).xpath(xpath)))
            if not solved_id:
                print("존재하지 않는 아이디거나 아직 푼 문제가 없습니다.")
            self.quizzes = self.quizzes[
                self.quizzes["problemId"].apply(lambda x: x not in solved_id)
            ]

        self.filtered_quizzes = self.quizzes

    def filter_quizzes(
        self, s=0, e=30, n=2, tags: list = None, level=-1, random_state=None
    ):

        # 난이도 필터
        if level >= 0:
            quizzes = self.quizzes[self.quizzes["level"].apply(lambda x: x == level)]
        else:
            quizzes = self.quizzes[self.quizzes["level"].apply(lambda x: s <= x <= e)]

        # 태그 필터
        org_tags = pd.read_pickle(
            "/".join("../data/quizzes.pkl".split("/")[:-1] + ["quiz_tags.pkl"])
        ).values.tolist()[0]
        if (tags := set(tags)) & set(org_tags):
            # quizzes = quizzes[set(quizzes.tags) & tags]
            quizzes = quizzes[
                quizzes["tags"].apply(lambda x: set(x) & tags).astype(bool)
            ]

        # 반환
        if quizzes.empty:
            if self.user_name:
                print("해당하는 문제를 모두 푸셨거나,", end=" ")
            print("해당하는 문제가 없습니다.")
        else:
            self.filtered_quizzes = quizzes
        return self.filtered_quizzes.sample(
            n=min(n, len(quizzes)), random_state=random_state
        )

    def select_quizzes(self, ids):

        quizzes = self.quizzes[self.quizzes["problemId"].apply(lambda x: x in ids)]
        if quizzes.empty:
            if self.user_name:
                print("해당하는 문제를 모두 푸셨거나,", end=" ")
            print(
                f"해당 문제가 존재하지 않습니다. {1000}에서 {len(self.quizzes) - 1000} 사이의 값을 입력해주세요.\n 위 범위 내에도 문제가 존재하지 않는 번호도 있습니다."
            )
        else:
            no_quiz = [id for id in quizzes.problemId if id not in ids]
            if no_quiz:
                if self.user_name:
                    print("해당하는 문제를 모두 푸셨거나,", end=" ")
                print("[", ",".join(no_quiz), "] 는 존재하지 않습니다.")
        return quizzes
