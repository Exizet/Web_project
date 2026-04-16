from fastapi import FastAPI, Request
from pydantic import  BaseModel
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from app.routers import about, announcement, contacts, home, galery, autorithation, verificade, documents, scheme, fire_safety, map, bus, water, shop_time, dibates

app = FastAPI()
templates = Jinja2Templates(directory="app/Frontend/templates")
app.mount("/css", StaticFiles(directory="app/Frontend/css"), name="css")
app.mount("/src", StaticFiles(directory="app/Frontend/src"), name="src")

snt_db = {'snt_1': 'Информация об СНТ 1', 'snt_2': 'Информация об СНТ2'}

app.include_router(home.router)
app.include_router(about.router)
app.include_router(announcement.router)
app.include_router(contacts.router)
app.include_router(galery.router)
app.include_router(autorithation.router)
app.include_router(verificade.router)
app.include_router(documents.router)
app.include_router(scheme.router)
app.include_router(fire_safety.router)
app.include_router(map.router)
app.include_router(bus.router)
app.include_router(water.router)
app.include_router(shop_time.router)
app.include_router(dibates.router)

@app.get("/")
async def redirect_home_page():
    return {"Msg": "debil"}#RedirectResponse("/home/")
'''
@app.get("/home")
async def get_home_page(request: Request, snt: str) -> HTMLResponse:
    return templates.TemplateResponse("index.html", {"request": request, "snt": snt})

@app.get("/announcement")
async def get_announcement_page(request: Request) -> HTMLResponse:
    return templates.TemplateResponse("announcement.html", {"request": request})

@app.get("/dibates")
async def get_dibates_page(request: Request) -> HTMLResponse:
    return templates.TemplateResponse("dibates.html", {"request": request})

@app.get("/contacts")
async def get_contacts_page(request: Request)-> HTMLResponse:
    return templates.TemplateResponse("kontact.html", {"request": request})
@app.get("/PersonalAccount")
async def get_account_page(request: Request) -> HTMLResponse:
    return templates.TemplateResponse('PersonalAccaunt.html', {"request": request})

@app.get("/about")
async def get_about_page(request: Request, snt: str) -> HTMLResponse:
    return templates.TemplateResponse("about.html", {"request": request, "snt": snt, "snt_db": snt_db})

@app.get("/{diff_page}")
async def get_dif_page(request: Request, diff_page: str) -> HTMLResponse:
    return templates.TemplateResponse(f"{diff_page}.html", {"request": request})
'''

