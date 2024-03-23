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
image_left = img_dir[5:]
image_right = img_dir[:5]
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
    return {"user_list": test_room.users}

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
    return {"left_img":image_left[game_ctr], "right_img":image_right[game_ctr]}

@app.get("/get_img/{img_path}", response_class=HTMLResponse)
async def game_info(img_path: str):
    print("HE")
    return FileResponse("img/" + img_path, media_type="image/jpeg")

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
        print("2222")
        if test_room.usernum == test_room.endnum:
            # 알고리즘 동작 지역
            result_dict = {}
            for key in test_room.result:
                for list in test_room.result[key]:
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
                        update_dict("간장게장", result_dict)
                    elif list == [1,0,1,0,0,1,0,0,1]:
                        update_dict("김치찌개", result_dict)
                    elif list == [0,0,0,0,1,1,0,1,0]:
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
        return {"endresult": "wait"}
    else:
        return {"endresult": test_room.endresult}
def update_dict(key, my_dict):
    if key in my_dict:
        my_dict[key] += 1
    else:
        my_dict[key] = 1
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
