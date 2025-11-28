from contextlib import asynccontextmanager
from fastapi import FastAPI, Body, Request, HTTPException
from fastapi.responses import RedirectResponse, HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles # 靜態網頁資料處理
from fastapi.templating import Jinja2Templates # Jinja2配合html進行動態選染/產生動態路徑
from starlette.middleware.sessions import SessionMiddleware # 使用者狀態管理
import json # 解析json回覆
import mysql.connector # 連接資料庫
import os
from dotenv import load_dotenv, dotenv_values
from bcrypt import hashpw, gensalt, checkpw # 用來將密碼加密儲存
from pydantic import BaseModel, Field, EmailStr # 自動輸入驗證與型別轉換

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
    return templates.TemplateResponse("index.html",{"request": request})

# 註冊
class SignUpData(BaseModel):
    name: str = Field(..., min_length=1, max_length=10)
    email: EmailStr  # 自動驗證郵箱格式
    password: str

@app.post("/signup")
def sign_up(request: Request, data:SignUpData):
    cursor = None
    try:
        name = data.name.strip()
        mail = data.email.strip()
        pwd = data.password.strip()
        
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

        return {"ok": True, "msg": "註冊成功"}
    
    except Exception as e:
        if cursor:  # ✓ 只在有 cursor 時才 rollback
            con.rollback()
        print(f"伺服器錯誤: {e}")
        return {"ok": False, "msg": "伺服器錯誤"}
    finally:
        if cursor: # ✓ 檢查 cursor 是否存在
            cursor.close() # 統一關閉游標物件避免佔用伺服器資源

# 登入並存會員資料進 session
class LoginData(BaseModel):
    email: EmailStr
    password: str

@app.post("/login")
def verify(request: Request, data: LoginData):
    cursor = None
    try:
        email = data.email.strip()
        pwd = data.password.strip()
        
        con = request.app.state.con
        cursor = con.cursor(dictionary=True)

        # 從資料庫查詢該電子郵件的用戶
        cursor.execute(
            "SELECT id, name, password FROM member WHERE email=%s",[email]
        )
        result = cursor.fetchone() 
        # result = {'id': 17, 'name': '阿寶v2', 'password': '加密後的密碼'})

        if not result:
            return {"ok": False, "msg": "電子郵件或密碼不正確"}

        user_id = result['id']
        user_name = result['name']
        stored_hashed_pwd = result['password']

        # ============ 新增：密碼驗證 ============# 把從資料庫取出的加密密碼轉回 bytes
        # 檢查 stored_hashed_pwd 是否是字符串
        if isinstance(stored_hashed_pwd, str): #如果是 str → 轉換成 bytes
            stored_hashed_pwd = stored_hashed_pwd.encode('utf-8')
        
        # 比較：輸入的密碼加密後，是否與資料庫中的匹配
        is_password_correct = checkpw(pwd.encode('utf-8'), stored_hashed_pwd) #結果會是「布林值」
        # =======================================

        if not is_password_correct:
            return {"ok": False, "msg": "電子郵件或密碼不正確"}

        # 密碼正確，設定 session
        request.session["user-info"] = {
            "user-id": user_id,
            "name": user_name,
            "email": email
        }
        
        return {"ok": True, "msg": "登入成功"}

    except Exception as e:
        if cursor:
            con.rollback()  # 保持一致風格（不加也完全可以...）
        print(f"伺服器錯誤: {e}")
        return {"ok": False, "msg": "伺服器錯誤"}
    finally:
        if cursor:
            cursor.close()


@app.get("/logout")
def logout(request: Request):
    request.session["user-info"] = None
    return {"ok": True, "msg": "您已登出"}

# 會員頁面
@app.get("/member")
def member(request: Request):
    user_info = request.session.get("user-info")
    if not user_info:
        return RedirectResponse("/")
    
    return FileResponse("templates/member.html")

# 失敗頁面
@app.get("/ohoh")
def error(request: Request, msg):
    return templates.TemplateResponse("error.html",{"request": request, "msg": msg})

#新增 - 送使用者資料給前端
@app.get("/api/member/current-user")
def get_current_user(request: Request):
    user_info = request.session.get("user-info")
    #print(user_info) 結果： {'user-id': 17, 'name': '阿寶v2', 'email': 'fff@fff.com'}

    # 如果沒有登入
    if not user_info:
        raise HTTPException(status_code=401, detail="未登入")
        # ↑ 這裡拋出例外
        # 下面的程式碼不會執行

    user_id = user_info.get("user-id")
    user_name = user_info.get("name")
    user_email = user_info.get("email")

    return {
        "ok": True, 
        "user-id": user_id,
        "username": user_name, 
        "email": user_email
        }


# week 7 - task 1 // 依據id查詢會員資料的 API
@app.get("/api/member/{id}")
def search_user(id, request: Request):
    target_id = int(id)
    con = request.app.state.con
    cursor = con.cursor()
    try:
        # 從資料庫查詢該id的用戶
        cursor.execute(
            "SELECT name, email FROM member WHERE id=%s",[target_id]
        )
        result = cursor.fetchone()
        if not result:
            return {"data": None}
        
        # 抓取目前登入的使用者信息
        user_info = request.session.get("user-info")
        if not user_info:
            return {"data": None}
        
        user_id = user_info.get("user-id")
        target_name = result[0]
        target_email = result[1]

        if user_id != target_id:
            cursor.execute(
                "INSERT INTO search_history (executor, target) VALUES(%s, %s)",
                [user_id, target_id]
            )
            con.commit()

        return {
            "data":{
                "id": target_id,
                "name": target_name,
                "email": target_email
            }
        }

    except Exception as e: # 如果中途發生其他錯誤
        print(f"伺服器錯誤: {e}") 
        con.rollback() # 把前面commit的SQL指令回滾(取消)
        raise HTTPException(status_code=500, detail="伺服器錯誤") 
        # 這邊不把 str(e) 回給前端，避免洩露內部資訊（ex:資料庫設計結構)
    
    finally:
        cursor.close() # 在這邊統一把游標物件關閉，避免佔用資源～

# 給使用者修改名稱的API
class UpdateNameRequest(BaseModel):
    name: str = Field(...,min_length=1, max_length=10) #必傳，最小長度 1，最大長度 10

@app.patch("/api/member")
def update_name(request: Request,data: UpdateNameRequest):
    cursor = None # 先在外部宣告 這樣try/finally才都能取用
    try:
        new_name = data.name.strip()

        # 驗證
        user_info = request.session.get("user-info")
        if not user_info:
            return {"ok": False, "msg": "未登入"} # HTTPException(status_code=401, detail="未登入")

        if new_name == user_info.get("name"):
            return {"ok": False, "msg": "新名稱跟舊名稱相同！"}

        # 連線
        con = request.app.state.con
        cursor = con.cursor()

        cursor.execute(
            "UPDATE member SET name=%s WHERE id=%s", [new_name, user_info.get("user-id")]
        )
        # 確認有沒有改成功
        if cursor.rowcount == 0: # row_count函数返回的是当前连接中最近一次操作数据库的所影响的行数
            return {"ok": False, "msg": "使用者不存在"}

        con.commit() # 有成功才鎖定 execute 的執行結果

        # 一併把session內的資料更新
        user_info["name"] = new_name
        request.session["user-info"] = user_info

        return {"ok": True, "msg": "使用者名稱修改成功"}
    
    except Exception as e:
        if cursor:  # ← 只在有 cursor 時才 rollback
            con.rollback()
        print(f"伺服器錯誤: {e}")
        return {"ok": False, "msg": "伺服器錯誤"}
    
    finally:
        if cursor:  # 有 cursor 的話統一在 finally 關閉
            cursor.close()

# 搜尋查詢紀錄
@app.get("/api/search_history")
def search_history(request:Request):
    user_info = request.session.get("user-info")
    if not user_info:
        raise HTTPException(status_code=401, detail="未登入")
    user_id = user_info.get("user-id")
    con = request.app.state.con
    cursor = con.cursor(dictionary=True)
    try:
        cursor.execute(
            """SELECT member.name, search_history.time 
            FROM member INNER JOIN search_history 
            ON search_history.executor = member.id 
            WHERE search_history.target = %s 
            ORDER BY search_history.time DESC 
            LIMIT 10""", [user_id])
        history = cursor.fetchall()

        # if not history:
        #     raise HTTPException(status_code=404, detail="資料不存在")
        
        #print(history)
        return {"data": history}
    
    except HTTPException:
        raise

    except Exception as e: 
        print(f"伺服器錯誤: {e}") 
        con.rollback() # 把前面commit的SQL指令回滾(取消)
        raise HTTPException(status_code=500, detail="伺服器錯誤") 
    
    finally:
        cursor.close()


# ------------------- 統一處理靜態網頁 --------------------
# 物件名稱.mount("網頁前綴", StaticFiles(directory="資料夾名稱"),name="內部名稱")
app.mount("/static", StaticFiles(directory="static"), name="static")
