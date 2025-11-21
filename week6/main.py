from contextlib import asynccontextmanager
from fastapi import FastAPI, Body, Request
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles # 靜態網頁資料處理
from fastapi.templating import Jinja2Templates # Jinja2配合html進行動態選染/產生動態路徑
from starlette.middleware.sessions import SessionMiddleware # 使用者狀態管理
import json # 解析json回覆
import httpx # 非同步呼叫用
import mysql.connector # 連接資料庫
import os
from dotenv import load_dotenv, dotenv_values

#------------------- 取得環境變數內的資料 --------------------
load_dotenv()
db_pwd = os.getenv("DB_PASSWORD")
session_key = os.getenv("SECRET_KEY")
#------------------- 預先載入資料 --------------------
con = None
@asynccontextmanager #lifespan - 自動於程式啟動/關閉時運行
async def lifespan(app: FastAPI):
    global con
    con = mysql.connector.connect(
        user = "root",
        password = db_pwd,
        host = "localhost",
        database = "website"
    )
    app.state.con = con  # FastAPI官方建議用 state
    print("資料庫連線完成")

    yield
    con.close()
    print("斷開連線")

#------------------- 宣告 FastAPI 物件 --------------------
app = FastAPI(lifespan=lifespan)
#---------- 使用 SessionMiddleware，密鑰為任意字串 ----------
app.add_middleware(SessionMiddleware, secret_key = session_key)
# 告知templates的路徑
templates = Jinja2Templates(directory="templates") 

#----------------------- API本體 -------------------------
# 建立網站的首頁
@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
        },
        status_code=200
    )

@app.post("/signup")
def sign_up(request: Request, body=Body(None)):
    data = json.loads(body)
    # print(data)
    name = data["name"]
    mail = data["email"]
    pwd = data["password"]
    con = request.app.state.con #取得資料庫連線物件
    cursor = con.cursor()
    cursor.execute("SELECT * FROM member WHERE email=%s", [mail])
    result = cursor.fetchone()
    if result == None: #代表還沒註冊過
        cursor.execute("INSERT INTO member (name, email, password) VALUES(%s,%s,%s)", [name, mail, pwd])
        con.commit()
        return {"ok":True}
    else:
        return {"ok":False, "msg": "重複的電子郵件"}


@app.post("/login")
def verify(request: Request,body=Body(None)):
    data = json.loads(body)
    email = data["email"]
    password = data["password"]
    con = request.app.state.con
    cursor = con.cursor()
    cursor.execute("SELECT * FROM member WHERE email=%s AND password=%s", [email, password])
    result = cursor.fetchone()

    if result == None: #代表找不到相符資料
        request.session["user-info"] = None
        return {"ok": False, "msg": "帳號或密碼輸入錯誤"}
    else: #如果有找到對應使用者，就吧他的資料存進session
        request.session["user-info"] = {"user-id": result[0], "name": result[1], "email": result[2]}
        return {"ok": True}

@app.get("/logout")
def logout(request: Request):
    request.session["user-info"] = None
    return {"ok": True, "msg": "您已登出"}

@app.get("/member", response_class=HTMLResponse)
def member(request: Request):
    if request.session["user-info"] != None:
        information = request.session["user-info"]

        con = request.app.state.con
        cursor = con.cursor(dictionary=True)
        cursor.execute(
            """SELECT member.name, message.member_id, message.id, content 
            FROM member INNER JOIN message on member.id = message.member_id""")
        messages = cursor.fetchall()



        context = {"request": request, "user_name": information["name"], "user_id": information["user-id"], "messages": messages}
        return templates.TemplateResponse("member.html", context)
    else:
        return RedirectResponse("/")

@app.get("/ohoh", response_class=HTMLResponse)
def error(request: Request, msg):
    return templates.TemplateResponse("error.html",{"request": request, "msg": msg})

@app.post("/createMessage")
def leave_message(request: Request, body=Body(None)):
    data = json.loads(body)
    content = data["content"]
    member_id = request.session["user-info"]["user-id"]
    con = request.app.state.con
    cursor = con.cursor()
    cursor.execute("INSERT INTO message(member_id, content) VALUES(%s,%s)",[member_id, content])
    con.commit()
    return {"ok": True}

@app.post("/deleteMessage")
def delete_message(request: Request, body=Body(None)):
    data = json.loads(body)
    message_id = data["id"]
    con = request.app.state.con
    cursor = con.cursor()
    cursor.execute("DELETE FROM message WHERE id=%s", [message_id])
    con.commit()
    return {"ok": True}


# ------------------- 統一處理靜態網頁 --------------------
# 物件名稱.mount("網頁前綴", StaticFiles(directory="資料夾名稱"),name="內部名稱")
app.mount("/static", StaticFiles(directory="static"), name="static")
