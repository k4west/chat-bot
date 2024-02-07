import requests
import pandas as pd
from tqdm import tqdm
from lxml import html


class QuizCrawling:

    def __init__(self, src="quizzes.pkl"):

        self.df = None
        self.src = src
        self.start_id = 1000
        self.last_id = 30000
        self.lost_ids = []
        self.update_id()

    def update_id(self):

        try:
            df = pd.read_pickle(self.src)
            self.start_id = len(df)
        except:
            print("It's the first time!")

        headers = {"User-Agent": "Mozilla/5.0"}
        params = {"sort": "no_desc"}
        url = "https://www.acmicpc.net/problemset"
        xpath = '//*[@id="problemset"]/tbody/tr[1]/td[1]/text()'

        response = requests.get(url, params=params, headers=headers)
        self.last_id = int(html.fromstring(response.text).xpath(xpath)[0])
        print(f"start_id: {self.start_id}, last_id: {self.last_id}")

    # 문제 불러오기
    def quiz_crawling(self, losted: bool = False):

        url = "https://solved.ac/api/v3/search/problem"
        headers = {"Accept": "application/json"}
        keys = ["problemId", "titleKo", "level"]  # 문제 ID, 한국어 문제 제목, 난이도
        quizzes = []
        errors = set()

        if losted:  # 놓친 문제 crawling
            new_losted = []
            df0 = pd.read_pickle("quizzes.pkl")["problemId"]
            if not self.lost_ids:
                self.lost_ids = [
                    i for i in range(1000, 31394 + 1) if i not in df0.values
                ]

            pbar = tqdm(self.lost_ids, desc="Crawling", ncols=70, ascii=" =")

        else:  # 전체 문제 crawling
            pbar = tqdm(
                range(self.start_id, self.last_id + 1),
                desc="Crawling",
                ncols=70,
                ascii=" =",
            )

        for quiz_id in pbar:
            pbar.set_description(f"Crawling {quiz_id}th quiz")
            try:
                querystring = {"query": f"{quiz_id}"}
                response = requests.get(url, headers=headers, params=querystring).json()

                if response["count"] == 0:
                    quiz = {key: None for key in keys}
                    quiz["tags"] = []
                    quiz["problemId"] = quiz_id
                    continue

                items = response["items"]
                for item in items:
                    quiz = {key: item[key] for key in keys}

                    if item["tags"]:
                        # quiz['tags'] = [displayName['name'] for tag in item["tags"] for displayName in tag["displayNames"] if displayName['language'] == 'ko']
                        tags = []
                        for tag in item["tags"]:
                            for displayName in tag["displayNames"]:
                                if displayName["language"] == "ko":
                                    tags.append(displayName["name"])
                        quiz["tags"] = tags
                    else:
                        quiz["tags"] = []

                    quizzes.append(quiz)

            except Exception as e:
                new_losted.append(quiz_id)
                errors.add(e)

        if losted:
            self.lost_ids = new_losted
            self.df = (
                pd.concat([pd.DataFrame(quizzes), self.df])
                .drop_duplicates(subset="problemId")
                .sort_values("problemId", ignore_index=True)
            )
        else:
            self.df = pd.DataFrame(quizzes)

        print(errors)
        return self.df

    # pickle로 저장
    def save_quiz(self, dst=None):

        if not dst:
            dst = self.src

        try:
            self.df = (
                pd.concat([pd.read_pickle(self.src), self.df])
                .drop_duplicates(subset="problemId")
                .sort_values("problemId", ignore_index=True)
            )
        except:
            pass

        self.df.to_pickle(dst)


if __name__ == "__main__":
    # 문제 크롤링
    crawled_quiz = QuizCrawling(src="quizzes.pkl")
    crawled_quiz.quiz_crawling()

    # # 놓쳤을 때 주석 제거 후 다시 crawling 할 수 있음, 아래는 다시 시도를 1번만 하도록 함
    # check, i = [], 1
    # import cv2
    # while (prev := crawled_quiz.lost_ids) != check:
    #     crawled_quiz.quiz_crawling(losted=True)
    #     check = prev
    #     print(i, "번째 시도 완료")
    #     i += 1
    #     if i >= 1:
    #         break
    #     if cv2.waitKey(5) == ord('q'):
    #         break

    # # 사용할 이유는 없어보이지만, 특정 범주의 문제 번호만 crawling하는 방법
    # crawled_quiz = QuizCrawling(src="pkl 파일 저장 경로")
    # crawled_quiz.start_id = 'crwaling할 문제 첫 번호'
    # crawled_quiz.last_id = 'crwaling할 문제 마지막 번호'
    # crawled_quiz.quiz_crawling()

    # 문제 저장
    crawled_quiz.save_quiz("quizzes.pkl")
