from fastapi import FastAPI, Form, Depends, HTTPException, Cookie, Response
from fastapi.responses import RedirectResponse
from pydantic import BaseModel
from typing import List
from fastapi.staticfiles import StaticFiles
from starlette.responses import HTMLResponse
from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse, FileResponse
import uvicorn
import json
import os

app = FastAPI()

# 임시적으로 저장할 데이터베이스
rooms = []  
users = []
img_dir = os.listdir("./img")
game_text = ["어떤 종류의 음식이 땡기는 날인가요?", "밥, 면, 고기, 밀가루 등등 당신의 선택은?", "맵기는 몇 단계?", "칼로리는 얼마나 섭취할 예정?", "예산은 어느 정도가 예상하시나요?", "밥 먹는 지금, 과연 낮인가요? 아님 밤인가요?", "밥과 함께 술 한잔?", "설레이는 상대와 같이 밥을 먹나요?", "같이 밥을 먹는 사람은 몇 명?"]
left_text = ["일식", "밥, 고기", "안 매워", "적당히", "가성비", "점심", "술 X", "NO", "2명"]
right_text = ["한식", "면, 밀가루", "매워~", "풍족히", "가심비", "저녁", "술 O", "YES", "4명 이상"]
image_left = ["photo_3.PNG", "photo_12.PNG", "photo_5.PNG", "photo_110.PNG", "photo_9.PNG", "photo_34.PNG", "photo_0.PNG", "photo_310.PNG", "photo_49.PNG", "photo_49.PNG",  "photo_49.PNG"]
image_right = ["photo_7.PNG", "photo_15.PNG", "photo_8.PNG", "photo_01.PNG", "photo_32.PNG", "photo_31.PNG", "photo_26.PNG", "photo_14.PNG", "photo_111.PNG", "photo_111.PNG", "photo_111.PNG"]


result_img_dict = {"떡볶이":"photo_6.PNG", "라면":"photo_8.PNG", "김밥":"photo_3.PNG", "족발 보쌈":"photo_01.PNG", "만두":"photo_9.PNG", "닭도리탕":"src.png", "설렁탕":"photo_310.PNG", "국밥":"photo_310.PNG", "냉면":"photo_04.PNG", "닭발":"photo_16.PNG", "부타동":"photo_1.PNG", "초밥":"photo_14.PNG", "돈가스":"photo_35.PNG", "오코노미":"photo_25.PNG", "우동":"photo_0.PNG", "장어덮밥":"photo_05.PNG", "라멘":"photo_8.PNG", "오무라이":"photo_37.PNG", "해물파전":"photo_17.PNG", "비빔밥":"photo_07.PNG", "칼국수":"photo_28.PNG", "쌈밥":"photo_38.PNG", "규동":"photo_39.PNG", "회":"photo_49.PNG", "샤브샤브":"photo_29.PNG", "굴비":"photo_09.PNG", "부대찌개":"src1.png", "제육덮밥":"src2.png", "결과 취합 중...":""}

result_des_dict = {"떡볶이":"온국민의 국민 간식", "라면":"후루루 짭짭~ 후루루 짭짭~ 맛좋은 라면", "김밥":"잘 말아줘~ 잘 눌러줘~", "족발 보쌈":"야심한 밤에 자꾸 생각나는", "만두":"한 입 가득 행복한 맛", "닭도리탕":"매운 맛에 깊은 감칠맛이 어우러진 푸짐한 닭요리", "설렁탕":"산뜻한 육수에 고기가 촉촉하게 우러난 국민 영양식", "국밥":"주모 여기 국밥 한그릇이요~", "냉면":"차가워 너무나~ 속이 시려 너무나~", "닭발":"매콤한 양념에 푹 빠져든 닭발의 매력에 푸욱 빠져보세요", "부타동":"부드럽고 쫄깃한 돼지고기의 달콤한 맛이 입안 가득히 퍼지는 일본식 덮밥", "초밥":"신선한 회와 다양한 재료가 색다르게 어우러진 일본 전통 요리", "돈가스":"스윙스가 환장하는, 바삭한 튀김옷으로 포장된 속은 부드럽고 촉촉한 돼지고기의 만남", "오코노미":"고기와 해산물, 채소 등이 듬뿍 올라간 다이너마이트한 일본 요리", "우동":"뚝딱 끓여낸 국물에 쫄깃한 우동면이 어우러진 일본식 면요리","장어덮밥":"달콤한 소스와 부드러운 장어가 고소하게 어우러진 일본식 영양식", "라멘":"부드럽고 탱탱한 면과 진한 육수가 어우러진 일본식 면요리", "오무라이":"계란이랑 볶음밥의 완벽한 조화", "해물파전":"비가 오고 네가 생각나, 해물파전", "비빔밥":"다채로운 색감과 매콤한 양념이 어우러진 한식의 대표적인 메뉴", "칼국수":"부드러운 국물에 쫄깃한 칼국수면이 어우러진 국민 영양식", "쌈밥":"신선한 채소와 고기를 곁들여 말아먹는 건강하고 맛있는 한식요리", "규동":"부드럽고 촉촉한 소고기와 신선한 채소가 올라간 일본식 돈부리", "회":"바다내음과 소주한잔이 그리워질 때", "샤브샤브":"다양한 고기와 채소를 뜨거운 국물에 삶아 삶아~", "굴비":"보릿굴비 한마리면 이만한 밥도둑이 없지", "부대찌개":"매콤한 국물에 찐하고 나쁜 맛 가득한 재료들이 어우러진 한 그릇", "제육덮밥":"직장인과 남자들의 소울 푸드"}

class Room(BaseModel):
    owner: str
    id: int
    users: list
    usernum: int
    endnum: int
    flag: int
    result: dict
    endresult: str

class User(BaseModel):
    username: str

# 정적 파일을 제공하기 위해 디렉토리 설정
app.mount("/static", StaticFiles(directory="static"), name="static")


# 홈 페이지에 index.html 제공
@app.get("/", response_class=HTMLResponse)
async def index_response():
    return FileResponse("static/index.html")

@app.post("/register/")
def register_user(response:Response, name: str = Form(...)):
    # 받은 이름을 users 리스트에 추가
    if (name in users):
        return {"message": f"ALREADY have {name} "}
    else:
        users.append(name)
        cookie_value = str({'user_name':name})
        response = RedirectResponse(url="/home")
        response.set_cookie(key="example_cookie", value=cookie_value)
        return response
    
@app.post("/home/")
def home():
    return FileResponse("static/home.html")
@app.post("/create-room/")
async def create_room(room_id: int = Form(...), example_cookie: str = Cookie(None)):
    for test_room in rooms:
        if room_id == test_room.id:
            return {"message: type other room"}
    # 통과
    print(room_id)
    cookie_dict = eval(example_cookie)
    room = Room(id=room_id, users=[cookie_dict['user_name']], usernum=1, endnum = 0,owner=cookie_dict['user_name'], flag=0,result={cookie_dict['user_name']:[]}, endresult="")
    rooms.append(room)
    cookie_dict['room_id'] = room_id
    cookie_value = str(cookie_dict)
    print(cookie_value)
    #room_url = f"/room/{room_id}param1={room_id}"
    room_url = f"/room/{room_id}"
    response = RedirectResponse(url=room_url)
    response.set_cookie(key="example_cookie", value=cookie_value)
    print("here")
    return response


@app.post("/join-room/")
async def join_room(join_id: int = Form(...), example_cookie: str = Cookie(None)):
    i = 0
    for test_room in rooms:
        if join_id == test_room.id:
            print("find room", join_id)
            i = 1
            break
    if (i == 0):
        return {"message: there is no room"}
    #통과
    cookie_dict = eval(example_cookie)
    test_room.users.append(cookie_dict['user_name'])
    test_room.usernum += 1
    test_room.result[cookie_dict['user_name']] = []
    cookie_dict['room_id'] = join_id
    cookie_value = str(cookie_dict)
    #room_url = f"/room/{join_id}param1={join_id}"
    room_url = f"/room/{join_id}"
    response = RedirectResponse(url=room_url)
    response.set_cookie(key="example_cookie", value=cookie_value)
    print("here")
    return response


@app.post("/room/{room_id}")
def test():
    return FileResponse("static/room.html")

@app.get("/room/{room_id}")
async def room_info(room_id: int):
    print("HAHA")
    print(room_id)
    for test_room in rooms:
        if room_id == test_room.id:
            break
    return {"user_list": test_room.users, "userCount": test_room.usernum}

@app.post("/get-play")
async def get_play(response:Response, example_cookie: str = Cookie(None)):
    cookie_dict = eval(example_cookie)
    print(cookie_dict)
    room_id = cookie_dict['room_id']
    user_name = cookie_dict['user_name']
    i = 0
    for test_room in rooms:
        if room_id == test_room.id:
            if test_room.owner == user_name:
                #방장
                test_room.flag = 1
                cookie_dict['game_ctr'] = 0
                response = RedirectResponse("/room/"+str(room_id)+"/game/"+str(cookie_dict['game_ctr']))
                cookie_value = str(cookie_dict)
                response.set_cookie(key="example_cookie", value=cookie_value)
                return response
            else:
                #참여자
                if test_room.flag == 0:
                    #아직 시작 안함
                    return RedirectResponse("/room/"+str(cookie_dict['room_id']))
                else:
                    #시작함.
                    cookie_dict['game_ctr'] = 0
                    response = RedirectResponse("/room/"+str(room_id)+"/game/"+str(cookie_dict['game_ctr']))
                    cookie_value = str(cookie_dict)
                    response.set_cookie(key="example_cookie", value=cookie_value)
                    return response
            

@app.post("/room/{room_id}/game/{game_ctr}")
def test():
    return FileResponse("static/game.html")

@app.get("/room/{room_id}/game/{game_ctr}")
async def game_info(room_id: int, game_ctr: int):
    print("HOHO")
    
    return {"left_img":image_left[game_ctr], "right_img":image_right[game_ctr], "left_text":left_text[game_ctr], "right_text":right_text[game_ctr], "game_text":game_text[game_ctr]}

@app.get("/get_img/{img_path}", response_class=HTMLResponse)
async def game_info(img_path: str):
    media_type = "image/png"
    print("HE")
    return FileResponse("img/" + img_path, media_type=media_type)

@app.post("/left/")
async def get_left(example_cookie: str = Cookie(None)):
    print("left")
    cookie_dict = eval(example_cookie)
    room_id = cookie_dict['room_id']
    for test_room in rooms:
        if room_id == test_room.id:
            break
    user_name = cookie_dict['user_name']
    test_room.result[user_name].append(0)
    print(test_room.result[user_name])
    cookie_dict['game_ctr'] += 1
    cookie_value = str(cookie_dict)
    if cookie_dict['game_ctr'] > 8: #갯수!
        test_room.endnum += 1
        response = RedirectResponse("/room/" + str(room_id) + "/end")
        response.set_cookie(key="example_cookie", value=cookie_value)
        return response
    else:    
        response = RedirectResponse("/room/"+str(room_id)+"/game/"+str(cookie_dict['game_ctr']))
        response.set_cookie(key="example_cookie", value=cookie_value)
        return response
    

@app.post("/right/")
async def get_right(example_cookie: str = Cookie(None)):
    print("right")
    cookie_dict = eval(example_cookie)
    room_id = cookie_dict['room_id']
    for test_room in rooms:
        if room_id == test_room.id:
            break
    user_name = cookie_dict['user_name']
    test_room.result[user_name].append(1) #right is 1
    print(test_room.result[user_name])
    cookie_dict['game_ctr'] += 1
    cookie_value = str(cookie_dict)
    if cookie_dict['game_ctr'] > 8: #갯수!
        test_room.endnum += 1
        response = RedirectResponse("/room/" + str(room_id) + "/end")
        response.set_cookie(key="example_cookie", value=cookie_value)
        return response
    else:    
        response = RedirectResponse("/room/"+str(room_id)+"/game/"+str(cookie_dict['game_ctr']))
        response.set_cookie(key="example_cookie", value=cookie_value)
        return response

@app.post("/room/{room_id}/end")
async def end_room():
    return FileResponse("static/end.html")
@app.get("/room/{room_id}/end")
async def get_endresult(room_id: int):
    for test_room in rooms:
        if room_id == test_room.id:
            break
    print(test_room.endnum)
    if test_room.endresult == "":
        if test_room.usernum == test_room.endnum:
            # 알고리즘 동작 지역
            result_dict = {}
            for key in test_room.result:
                list = test_room.result[key]
                print("list")
                print(list)
                if list == [1,1,1,1,0,0,0,0,0]:
                    update_dict("떡볶이", result_dict)
                elif list == [1,1,1,1,0,1,0,0,0]:
                    update_dict("라면", result_dict)
                elif list == [1,0,0,0,0,0,0,0,0]:
                    update_dict("김밥", result_dict)
                elif list == [1,0,0,1,1,1,1,0,1]:
                    update_dict("족발 보쌈", result_dict)
                elif list == [1,1,0,1,0,0,0,0,0]:
                    update_dict("만두", result_dict)
                elif list == [1,0,1,1,1,1,0,0,0]:
                    update_dict("닭도리탕", result_dict)
                elif list == [1,0,0,1,0,1,0,0,0]:
                    update_dict("설렁탕", result_dict)
                elif list == [1,0,0,1,0,1,0,0,0]:
                    update_dict("국밥", result_dict)
                elif list == [1,0,0,1,0,1,0,0,0]:
                    update_dict("냉면", result_dict)
                elif list == [1,0,0,1,0,1,0,0,0]:
                    update_dict("닭발", result_dict)
                elif list == [1,0,1,1,0,1,1,0,0]:
                    update_dict("부타동", result_dict)
                elif list == [0,0,0,0,0,0,0,0,0]:
                    update_dict("초밥", result_dict)
                elif list == [0,0,0,1,0,0,0,1,0]:
                    update_dict("돈가스", result_dict)
                elif list == [0,1,0,1,1,1,1,1,0]:
                    update_dict("오코노미", result_dict)
                elif list == [0,1,0,0,0,0,0,1,0]:
                    update_dict("우동", result_dict)
                elif list == [0,0,0,0,1,0,0,1,0]:
                    update_dict("장어덮밥", result_dict)
                elif list == [0,0,0,1,0,0,0,1,0]:
                    update_dict("라멘", result_dict)
                elif list == [0,0,0,0,0,0,0,1,0]:
                    update_dict("오무라이", result_dict)
                elif list == [1,1,0,1,1,1,1,1,1]:
                    update_dict("해물파전", result_dict)
                elif list == [1,0,1,0,0,1,0,1,0]:
                    update_dict("비빔밥", result_dict)
                elif list == [1,0,0,0,0,0,0,1,0]:
                    update_dict("칼국수", result_dict)
                elif list == [1,0,0,0,0,0,0,1,0]:
                    update_dict("쌈밥", result_dict)
                elif list == [0,0,0,1,0,0,0,1,0]:
                    update_dict("규동", result_dict)
                elif list == [0,0,0,0,1,1,1,1,0]:
                    update_dict("회", result_dict)
                elif list == [0,0,0,0,1,1,1,1,0]:
                    update_dict("샤브샤브", result_dict)
                elif list == [1,0,0,0,1,0,0,0,0]:
                    update_dict("굴비", result_dict)
                elif list == [1,0,1,1,0,0,0,0,1]:
                    update_dict("부대찌개", result_dict)
                elif list == [1,0,1,1,0,0,0,0,0]:
                    update_dict("제육덮밥", result_dict)
                else:
                    update_dict("떡볶이", result_dict)
            max_value = max(result_dict.values())
            max_key = None
            for key, value in result_dict.items():
                if value == max_value:
                    max_key = key
                    break  # 최댓값에 대응하는 키를 찾았으므로 반복 중단
            test_room.endresult = max_key
        return {"endresult": "결과 취합 중...", "result_img":result_img_dict["결과 취합 중..."], "result_description":result_des_dict[test_room.endresult]}
    else:
        return {"endresult": test_room.endresult, "result_img":result_img_dict[test_room.endresult], "result_description":result_des_dict[test_room.endresult]}
def update_dict(key, my_dict):
    if key in my_dict:
        my_dict[key] += 1
    else:
        my_dict[key] = 1
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
