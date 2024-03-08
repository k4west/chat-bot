# chat-bot
[프로젝트 소개] 

- 크롤링한 백준 문제를 사용자의 요청에 맞게 필터를 해서 제공하는 디스코드 챗봇

[역할] 

- 데이터 수집, 서비스 구현, 배포

[과정] 

- request와 solved api 를 활용해 문제 목록을 크롤링했습니다.
- 필요한 정보를 데이터 프레임으로 저장했습니다.
- discord 라이브러리를 활용해 챗봇의 서비스를 구현했습니다.
- 무료 배포 서비스를 통해서 챗봇을 서버에 올렸습니다.

[성과] 

- 평일 랜덤 문제와 요청하는 내용에 해당되는 문제를 랜덤으로 제공하는 서비스 구현
- 코딩 테스트 학습 스터디를 좀 더 편하게 진행하고 있고, 1일 1커밋 챌린지 등 함께 동참하는 이벤트도 가졌습니다.
- 

사용법

`!` 이후에 문제를 치면 대화하듯이 문제를 요청할 수 있는데, 난이도를 버튼으로도 선택할 수 있게 추가했습니다. `!문제`, `!quiz`로 실행가능합니다.

`!ㅁ문제`, `!qquiz`
문제 앞에 ㅁ 또는 quiz 앞에 q를 적으면  띄어쓰기 기준으로 백준id, 난이도 시작, 난이도 끝, 문제 수, 태그를 순서대로 작성하면 바로 문제를 주는 명령어도 추가했습니다.
+ `!ㅁ문제`, `!qquiz`만 입력하시면 제가 기본으로 설정한 브론즈4~실버4 사이에 2문제가 랜덤으로 나옵니다.

백준 아이디를 입력하시면 풀었던 거는 제외하고 문제를 제공해줍니다.
`!태그`라고 하시면 크롤링해온 태그 이름 일부가 나옵니다.

<div className="text-center my-4 border border-black flex flex-wrap justify-center w-2/3 m-auto">
    <img src='https://github.com/k4west/chat-bot/assets/125423305/17780500-f2da-4401-b599-bee22219488a'/>
    <img src='https://github.com/k4west/chat-bot/assets/125423305/5d3cf327-1d41-4645-aaad-87cc1ab86e8d'/>
</div>
<br></br>

**문제 요청**                        /                        **빠른 문제 요청**
<div className="text-center my-4 border border-black flex flex-wrap justify-center w-2/3 m-auto">
    <img src='https://github.com/k4west/chat-bot/assets/125423305/e54fa654-ac93-46fd-9414-def6f2134dee' width="450"/>
    <img src='https://github.com/k4west/chat-bot/assets/125423305/09f66fdb-9644-4733-94a6-a858703fd229' width="450"/>
</div>
