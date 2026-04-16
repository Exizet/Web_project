from fastapi import APIRouter, Depends, status, HTTPException, Request
from sqlalchemy.orm import Session
from typing import Annotated
from sqlalchemy import insert, select, update
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles


from app.Backend.db.db_depends import get_db
from app.schemas import CreateSNT
from app.models.snt import Snt
from app.routers.autorithation import get_current_user

router = APIRouter(prefix='/about', tags=['about'])

templates = Jinja2Templates(directory="app/Frontend/templates")
router.mount("/css", StaticFiles(directory="app/Frontend/css"), name="css")
router.mount("/src", StaticFiles(directory="app/Frontend/src"), name="src")

@router.get('/')
async def get_about_page(request: Request, db: Annotated[Session, Depends(get_db)], get_user = Depends(get_current_user)):
    if get_user.get('is_user'):
        snt = db.scalars(select(Snt).where(Snt.id == get_user.get('snt_id'), Snt.is_active==True)).all()
        return templates.TemplateResponse("about.html", {"request": request, "snt": snt[0]})
    else:
        return RedirectResponse('/autorisation/')

@router.put('/{snt_id}')
async def update_about_page(db: Annotated[Session, Depends(get_db)], update_snt: CreateSNT, snt_id: int):
    snt = db.scalar(select(Snt).where(Snt.id == snt_id, Snt.is_active == True))
    if snt is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="There is no SNT id"
        )

    db.execute(update(Snt).where(Snt.id == snt_id).values(
        description= update_snt.description,
        sites_quantity=update_snt.all_sites,
        free_sites=update_snt.free_sites
    ))
    db.commit()
    return{
        'status_code': status.HTTP_200_OK,
        'transaction': 'SNT update is successful'
    }