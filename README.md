Japanese Conversation Agent

LangGraph를 활용하여 구현한 일본어 회화 학습 에이전트입니다.
사용자는 일본어로 자유롭게 대화할 수 있으며, 에이전트는 자연스럽게 대화를 이어가는 동시에 학습에 도움이 되는 피드백을 제공합니다.
되도록이면 일본어로만 입력해주세요!

✨ 주요 기능
💬 일본어 자연 회화
📝 한국어 문법 피드백
문법(Grammar)
어휘(Vocabulary)
한자(Kanji)
경어(Register)
🌐 최신 정보가 필요한 질문은 자동 Web Search
🧠 LangGraph 기반 Node / Conditional Edge 구조
🏗️ 프로젝트 구조
START
   │
validation
   │
   ├──────────────┐
   │              │
   ▼              ▼
conversation     END
   │
   ├──── search ───► response
   │                 │
   └─────────────────┘
            │
           END

각 역할을 독립된 노드로 분리하여 구현하였습니다.

Conversation Node
일본어 문장 분석
피드백 생성
Response Mode 결정
Web Search 필요 여부 판단
Search Node
실시간 정보 검색
Response Node
일본어 자연 회화 생성
🚀 실행 방법
1. 저장소 Clone
git clone https://github.com/USERNAME/REPOSITORY.git

cd REPOSITORY
2. 패키지 설치
pip install -r requirements.txt
3. 환경 변수 설정

.env

OPENAI_API_KEY=YOUR_API_KEY
4. Streamlit 실행
streamlit run app.py

브라우저에서 접속하면 바로 사용할 수 있습니다.

💬 사용 예시
입력
今日は寿司に食べます。
회화 응답
そうなんですね！
どんなお寿司が好きですか？
학습 피드백
'寿司に食べます'는 조사 사용이 자연스럽지 않습니다.
'寿司を食べます'가 올바른 표현입니다.
🌐 Web Search 예시

입력

今日の東京の天気は？

Conversation Node가 실시간 정보가 필요하다고 판단하면 Search Node를 거쳐 최신 정보를 반영하여 답변합니다.

⚠️ 사용 시 주의사항

이 에이전트는 일본어 학습용입니다.

반드시 일본어 문장을 입력해주세요.

일본어가 아닌 입력은 처리하지 않으며 안내 메시지를 출력합니다.

🛠️ 사용 기술
Python
LangGraph
LangChain
OpenAI API
Streamlit
Pytest
📁 테스트

프로젝트에는 두 종류의 테스트가 포함되어 있습니다.

기능 테스트
pytest tests/test_conversation.py
Response Mode
Feedback 생성
Web Search 여부
LLM Judge 테스트
pytest tests/test_ai_conversation.py

pytest tests/test_ai_response.py
피드백 품질
응답 자연스러움
Response Mode 적절성
암묵적 교정 여부
🔮 향후 개선 계획

현재 구조를 유지한 채 다음 기능을 추가할 수 있도록 설계하였습니다.

🎤 STT (Speech-to-Text)
🔊 TTS (Text-to-Speech)
🧠 Conversation Memory 개선
📚 JLPT 단어장 연동
📈 학습 기록 저장
🔁 SRS(간격 반복 학습)
프로젝트 특징

이 프로젝트는 "회화"와 "교정"을 분리한 것이 핵심입니다.

회화는 자연스럽게 이어가고
문법 및 표현 오류는 한국어 피드백으로만 제공하여

실제 원어민과 대화하는 경험과 학습 효과를 동시에 얻을 수 있도록 설계하였습니다.
