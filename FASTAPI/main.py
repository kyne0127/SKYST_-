from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from fastapi.staticfiles import StaticFiles
from starlette.responses import HTMLResponse

app = FastAPI()

# 임시적으로 저장할 데이터베이스
rooms = []
users = {}


class Room(BaseModel):
    name: str
    us
    capacity: int


class User(BaseModel):
    username: str

# 정적 파일을 제공하기 위해 디렉토리 설정
app.mount("/static", StaticFiles(directory="static"), name="static")


# 홈 페이지에 index.html 제공
@app.get("/", response_class=HTMLResponse)
async def get_home():
    return open("static/index.html", "r").read()

@app.post("/create_room/")
async def create_room(room: Room):
    rooms.append(room)
    return {"message": f"Room '{room.name}' created with capacity {room.capacity}"}


@app.post("/invite_user/{room_name}/")
async def invite_user(room_name: str, user: User):
    room_found = False
    for room in rooms:
        if room.name == room_name:
            room_found = True
            if len(users.get(room_name, [])) < room.capacity:
                users.setdefault(room_name, []).append(user.username)
                return {"message": f"User '{user.username}' invited to room '{room_name}'"}
            else:
                raise HTTPException(status_code=400, detail="Room is full")
    if not room_found:
        raise HTTPException(status_code=404, detail="Room not found")


@app.get("/users/{room_name}/")
async def get_users(room_name: str):
    room_users = users.get(room_name, [])
    if room_users:
        return {"users": room_users}
    else:
        raise HTTPException(status_code=404, detail="Room not found")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
