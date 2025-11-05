from typing import Annotated
from fastapi import FastAPI, Path, Query, Body, Request
from fastapi.responses import FileResponse, RedirectResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware
import json
import httpx

app = FastAPI()
# 使用 SessionMiddleware，密鑰為任意字串
app.add_middleware(SessionMiddleware, secret_key="task3")

templates = Jinja2Templates(directory="templates") #告知templates的路徑

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

@app.post("/login")
def verify(request: Request,body=Body(None)):
    data = json.loads(body)
    mail = data["email"]
    pwd = data["password"]
    if mail == "abc@abc.com" and pwd == "abc":
        request.session["LOGGED-IN"] = True
        return {"ok": True, "msg": "登入成功"}

    elif mail == "" or pwd == "":
        return {"ok": False, "msg": "請輸入信箱和密碼"}

    elif mail != "abc@abc.com" or pwd != "abc":
        return {"ok": False, "msg": "帳號或密碼輸入錯誤"}
    

@app.get("/logout")
def logout(request: Request, body=Body(None)):
    request.session["LOGGED-IN"] = False
    return {"ok": True, "msg": "您已登出"}


@app.get("/member", response_class=HTMLResponse)
def member(request: Request):
    if request.session["LOGGED-IN"]:
        return templates.TemplateResponse("member.html",{"request": request})
    else:
        return RedirectResponse("/")

@app.get("/ohoh", response_class=HTMLResponse)
def error(request: Request, msg):
    return templates.TemplateResponse("error.html",{"request": request, "msg": msg})

@app.get("/hotel/{id}", response_class=HTMLResponse)
async def search_hotel(request: Request, id:int): #收到的路徑參數會是字串，要記得轉數字
    cn_url = "https://resources-wehelp-taiwan-b986132eca78c0b5eeb736fc03240c2ff8b7116.gitlab.io/hotels-ch"
    eng_url = "https://resources-wehelp-taiwan-b986132eca78c0b5eeb736fc03240c2ff8b7116.gitlab.io/hotels-en"
    async with httpx.AsyncClient() as client:
        resp = await client.get(cn_url)
        data_cn = resp.json()["list"]
    async with httpx.AsyncClient() as eng_client:
        response = await eng_client.get(eng_url)
        data_eng = response.json()["list"]

    cn_list = {hotel["_id"]:hotel for hotel in data_cn}
    eng_list = {eng_hotel["_id"]:eng_hotel for eng_hotel in data_eng}
    ids = cn_list.keys()
    if id in ids:
        hotel_list = {hid:f"{cn_list[hid]['旅宿名稱']}、{eng_list[hid]['hotel name']}、{cn_list[hid]['電話或手機號碼']}" for hid in ids}
        return templates.TemplateResponse("hotel.html",{"request": request, "information": hotel_list.get(id)})

    return templates.TemplateResponse("hotel.html",{"request": request, "information": "查詢不到相關資料"})

#!串接外部API
# @app.get("/get-data/{id}")
# async def getData(id:int) -> dict:
#     cn_url = "https://resources-wehelp-taiwan-b986132eca78c0b5eeb736fc03240c2ff8b7116.gitlab.io/hotels-ch"
#     eng_url = "https://resources-wehelp-taiwan-b986132eca78c0b5eeb736fc03240c2ff8b7116.gitlab.io/hotels-en"
#     async with httpx.AsyncClient() as client:
#         resp = await client.get(cn_url)
#         data_cn = resp.json()["list"]
#     async with httpx.AsyncClient() as eng_client:
#         response = await eng_client.get(eng_url)
#         data_eng = response.json()["list"]

#     cn_list = {hotel["_id"]:hotel for hotel in data_cn}
#     eng_list = {eng_hotel["_id"]:eng_hotel for eng_hotel in data_eng}
#     ids = cn_list.keys()
#     if id in ids:
#         hotel_list = {hid:f"{cn_list[hid]['旅宿名稱']}、{eng_list[hid]['hotel name']}、{cn_list[hid]['電話或手機號碼']}" for hid in ids}
#         return {"ok": True, "info": hotel_list.get(id)}

#     return {"ok": True, "info": "查詢不到相關資料"}









# 統一處理靜態網頁
# 物件名稱.mount("網頁前綴", StaticFiles(directory="資料夾名稱"))
app.mount("/static", StaticFiles(directory="static"), name="static")