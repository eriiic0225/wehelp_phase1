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
from bcrypt import hashpw, gensalt, checkpw # 用來將密碼加密儲存

#------------------- 取得環境變數內的敏感資料 --------------------
load_dotenv()
db_pwd = os.getenv("DB_PASSWORD") # 資料庫密碼
session_key = os.getenv("SECRET_KEY") # session金鑰
#------------------- 預先載入資料 --------------------
con = None
@asynccontextmanager #lifespan - 自動於程式啟動/關閉時運行
async def lifespan(app: FastAPI):
    global con
    try:
        con = mysql.connector.connect(
            user="root",
            password=db_pwd,
            host="localhost",
            database="website"
        )
        app.state.con = con
        print("✓ 資料庫連線完成")
    except mysql.connector.Error as e:
        print(f"✗ 資料庫連線失敗: {str(e)}")
        raise
    
    yield
    
    if con and con.is_connected():
        con.close()
        print("✓ 資料庫連線已關閉")

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
    try:
        # data = json.loads(body) //這邊是原始版本，前端沒給headers告知資料型態，需要手動解析
        data = body
        name = data.get("name", "").strip() #去除空字串，並在get method預設空字串為取不到資料的返回值
        mail = data.get("email", "").strip()
        pwd = data.get("password", "").strip()

        #檢查是否為空
        if not all([name, mail, pwd]):
            return {"ok": False, "msg": "欄位不能為空"}
        
        con = request.app.state.con #取得資料庫連線物件
        cursor = con.cursor() # 建立游標物件

        # 檢查電子郵件是否已存在
        cursor.execute("SELECT * FROM member WHERE email=%s", [mail])
        if cursor.fetchone(): #如果有抓到東西就代表註冊過了
            return {"ok": False, "msg": "此電子郵件已被註冊"}
        
        # ============ 新增：密碼加密 ============
        # 第 1 步：生成 salt（隨機鹽值）
        salt = gensalt()
        # 第 2 步：用 salt 加密密碼
        encode_pwd = pwd.encode('utf-8') #字串 → 位元組（bytes）/ 字符串轉成位元組
        hashed_pwd = hashpw(encode_pwd, salt) #透過hashpw()把兩個位元組(密碼本身和鹽值)透過演算法打算混合
        # =======================================

        # 存入資料庫（存加密後的密碼，不是原密碼）
        cursor.execute(
            "INSERT INTO member (name, email, password) VALUES(%s,%s,%s)", 
            [name, mail, hashed_pwd]  # ← 存的是加密後的
        )
        con.commit()
        cursor.close() # 關閉游標物件避免佔用伺服器資源

        return {"ok": True, "msg": "註冊成功"}
    
    except json.JSONDecodeError:
        return {"ok": False, "msg": "JSON 格式錯誤"}
    except Exception as e:
        print(f"伺服器錯誤: {e}")
        return {"ok": False, "msg": "伺服器錯誤"}


@app.post("/login")
def verify(request: Request,body=Body(None)):
    print(f"body 的型態: {type(body)}")
    print(f"body 的內容: {body}")
    try:
        # data = json.loads(body) //這邊是原始版本，前端沒給headers告知資料型態，需要手動解析
        data = body
        email = data.get("email", "").strip()
        pwd = data.get("password", "").strip()

        if not email or not pwd: # 如果沒有email或密碼
            return {"ok": False, "msg": "電子郵件或密碼不能為空"}
        
        con = request.app.state.con
        cursor = con.cursor()

        # 從資料庫查詢該電子郵件的用戶
        cursor.execute(
            "SELECT id, name, password FROM member WHERE email=%s",[email]
        )
        result = cursor.fetchone()

        if not result:
            cursor.close() 
            return {"ok": False, "msg": "電子郵件或密碼不正確"}
        
        user_id, user_name, stored_hashed_pwd = result

        # ============ 新增：密碼驗證 ============# 把從資料庫取出的加密密碼轉回 bytes
        # 檢查 stored_hashed_pwd 是否是字符串
        if isinstance(stored_hashed_pwd, str): #如果是 str → 轉換成 bytes
            stored_hashed_pwd = stored_hashed_pwd.encode('utf-8')
        
        # 比較：輸入的密碼加密後，是否與資料庫中的匹配
        is_password_correct = checkpw(pwd.encode('utf-8'), stored_hashed_pwd)
        # =======================================

        if not is_password_correct:
            cursor.close() 
            return {"ok": False, "msg": "電子郵件或密碼不正確"}

        # 密碼正確，設定 session
        request.session["user-info"] = {
            "user-id": user_id,
            "name": user_name,
            "email": email
        }
        
        cursor.close()
        return {"ok": True, "msg": "登入成功"}

    except json.JSONDecodeError:
        return {"ok": False, "msg": "JSON 格式錯誤"}
    except Exception as e:
        print(f"伺服器錯誤: {e}")
        return {"ok": False, "msg": "伺服器錯誤"}


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
        cursor.close() 

        context = {"request": request, "user_name": information["name"], "user_id": information["user-id"], "messages": messages}
        return templates.TemplateResponse("member.html", context)
    else:
        return RedirectResponse("/")

@app.get("/ohoh", response_class=HTMLResponse)
def error(request: Request, msg):
    return templates.TemplateResponse("error.html",{"request": request, "msg": msg})

@app.post("/createMessage")
def leave_message(request: Request, body=Body(None)):
    try:
        # ============ 第 1 步：檢查登入 ============
        user_info = request.session.get("user-info")
        if not user_info:
            return {"ok": False, "msg": "請先登入"}
        
        user_id = user_info["user-id"]

        # ============ 第 2 步：解析 JSON ============
        try:
            data = body
        except json.JSONDecodeError:
            return {"ok": False, "msg": "JSON 格式錯誤"}
        
        # ============ 第 3 步：驗證留言內容 ============
        content = data.get("content", "").strip()

        if not content:
            return {"ok": False, "msg": "留言內容不能為空"}
        
        if len(content) > 200: # 這部分不在作業要求內，但可以作為日後參考～
            return {"ok": False, "msg": "留言內容不能超過 200 字"}
        
        # ============ 第 4 步：插入資料庫 ============
        con = request.app.state.con
        cursor = con.cursor()
        try:
            cursor.execute(
                "INSERT INTO message (member_id, content) VALUES(%s, %s)",
                [user_id, content]
            )
            con.commit()
            cursor.close()
            
            return {"ok": True, "msg": "留言已發布"}
        
        except Exception as db_error:
            cursor.close()
            print(f"資料庫錯誤: {db_error}")
            return {"ok": False, "msg": "留言發布失敗"}
    
    except Exception as e:
        print(f"未預期的錯誤: {e}")
        return {"ok": False, "msg": "伺服器內部錯誤"}


@app.post("/deleteMessage")
def delete_message(request: Request, body=Body(None)):
    try:
        user_info = request.session.get("user-info")

        # ============ 第 1 步：檢查是否登入 ============
        if not user_info: #session找不到使用者的資訊 → 沒登入
            return {"ok": False, "msg": "請先登入"}
        # =============================================

        user_id = user_info["user-id"] # 這邊先抓id後面驗證比對用

        # ============ 第 2 步：解析前端傳來的資料 ============
        data = body
        message_id = data.get("id")

        if not message_id:
            return {"ok": False, "msg": "留言 ID 不能為空"}
        
        # ============ 第 3 步：驗證權限（關鍵！） ============
        con = request.app.state.con
        cursor = con.cursor()

        # 先查詢這個留言是誰寫的
        cursor.execute(
            "SELECT member_id FROM message WHERE id=%s",
            [message_id]
        )
        result = cursor.fetchone()
        if not result:
            cursor.close()
            return {"ok": False, "msg": "留言不存在"}
        
        message_owner_id = result[0]
        
        # 檢查登入者是否是留言擁有者
        if message_owner_id != user_id:
            cursor.close()
            return {"ok": False, "msg": "沒有權限刪除他人留言"}

        # ============ 第 4 步：執行刪除 ============
        cursor.execute("DELETE FROM message WHERE id=%s", [message_id])
        con.commit()
        cursor.close()

        return {"ok": True, "msg": "留言已刪除"}
    
    except json.JSONDecodeError:
        return {"ok": False, "msg": "JSON 格式錯誤"}
    except Exception as e:
        print(f"錯誤: {e}")
        return {"ok": False, "msg": "伺服器錯誤"}


# ------------------- 統一處理靜態網頁 --------------------
# 物件名稱.mount("網頁前綴", StaticFiles(directory="資料夾名稱"),name="內部名稱")
app.mount("/static", StaticFiles(directory="static"), name="static")
