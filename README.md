Conversation Agent

LangGraph를 이용하여 구현한 일본어 회화 에이전트입니다.
본 프로젝트는 회화 생성, ​문법 피드백, ​웹 검색의 역할을 분리하여 LangGraph의 노드와 Conditional Edge를 활용하는 것을 목표로 제작되었습니다.

❗❗❗반드시 일본어로 문장을 작성해주세요!❗❗❗
실행 방법
환경 변수 설정
OPENAI_API_KEY=YOUR_API_KEY
Notebook 실행
from src.graph import build_graph

app = build_graph().compile()

result = app.invoke(
{
"user_input": "こんにちは！"
}
)

print(result)
실행 예시

입력

今日は寿司に食べます。

Conversation Node 결과

feedback:
문법적으로 "寿司に食べます"는 부자연스럽습니다.
올바른 표현은 "寿司を食べます"입니다.

need_web_search:
False

Response Node 결과

そうなんですね！
どんなお寿司が好きですか？

문법 교정은 Feedback에서만 수행하며, Response는 사용자의 의도를 이해하여 대화를 이어갑니다.

향후 확장 예정

현재 구현 범위에는 포함하지 않았지만 다음 기능을 추가할 수 있도록 구조를 설계하였습니다.

Conversation Memory
STT (음성 인식)
TTS (음성 합성)
JLPT 단어장 연동
학습 기록 저장
SRS(간격 반복 학습)
