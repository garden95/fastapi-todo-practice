

from fastapi import FastAPI #FastAPI 클래스 호출 / 웹서버 요청을 받고 응답을 돌려주는 모든 규칙과 기능 담당
from fastapi import status
from pydantic import BaseModel, Field #Pydantic은 타입 힌트(str, int, bool 등)를 이용해 데이터를 검증하고 변환해 주는 외부 라이브러리

# BaseModel - 강력한 검증 도구, class가 BaseModel을 상속받으면 자동 검증 기능을 갖추게 된다.
class TodoCreate(BaseModel): 
    text : str = Field(min_length=1)

#FastAPI 애플리케이션 인스턴스(본체) 생성
app = FastAPI() #앞으로 만들 모든 API 주소(엔드포인트), 데이터 검증 규칙, 문서 설정 등이 모두 이 `app`이라는 객체에 등록

TODOS = [] # 서버 메모리에 저장할 리스트
NEXT_ID = 1

'''
 - 루트 경로("/")에 대한 GET요청 처리기(라우터 등록)
 - @는 데코레이터 아래 함수를 가로채서 `app`에 "이 함수는 웹 요청을 처리하는 함수야"라고 등록하는 역할
 - .get 은 HTTP 통신 규약 중 데이터를 단순히 조회(가져오기)할 때 사용하는 `GET` 메서드
'''

@app.get("/") 
def home():
    return {"message" : "안녕하세요"} # `GET /`로 접속했을 때 실행될 실제 작업 로직

# uvicorn main:app --reload <- 서버 실행 명령어
#기본 접속 주소 [http://127.0.0.1:8000]


'''
 - post - HTTP 규약(RESTful 원칙)에서 새로운 리소스를 생성할 때는 관례적으로 `POST` 메서드
'''
#할일 등록 API
@app.post("/todo", status_code=status.HTTP_201_CREATED) #새로운데이터 성공적 생성은 201, 수정 성공은 200
def create_todo(data : TodoCreate):
    global NEXT_ID

    todo = {"id" : NEXT_ID, "text" : data.text, "done" : False}
    NEXT_ID += 1
    TODOS.append(todo)
    return todo