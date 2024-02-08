# from time import sleep
# from datetime import datetime
# import pytz


# # 한국 시간대로 변경합니다.
# korea_tz = pytz.timezone("Asia/Seoul")


# def kor_now():
#     # 현재 시간을 UTC로 가져옵니다.
#     now_utc = datetime.now(pytz.utc)
#     now_korea = now_utc.astimezone(korea_tz)
#     return now_korea


# for _ in range(3):
#     print("현재 한국 시간:", kor_now().strftime("%H:%M"))
#     sleep(5)

import pandas as pd

tags = pd.read_pickle("./data/quiz_tags.pkl").values[0]

print(type(str(tags)))
