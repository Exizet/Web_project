from fastapi import APIRouter, Depends, status, HTTPException, Request, UploadFile, File, Form
from sqlalchemy.orm import Session
from typing import Annotated, Optional
from sqlalchemy import insert, select, update
from fastapi.responses import HTMLResponse, RedirectResponse
import os
from transliterate import translit, get_available_language_codes

from app.Backend.db.db_depends import get_db
from app.schemas import CreatePhoto, CreateAlbum
from app.routers.autorithation import get_current_user
from app.models.snt import Snt
from app.models.photo import Photo
from app.models.album import Album
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

UPLOAD_DIRECTORY = "app/Frontend/src/content"


router = APIRouter(prefix='/galery', tags=['galery'])
templates = Jinja2Templates(directory="app/Frontend/templates")

router.mount("/css", StaticFiles(directory="app/Frontend/css"), name="css")
router.mount("/src", StaticFiles(directory="app/Frontend/src"), name="src")


@router.get('/')
async def get_galery_page(db: Annotated[Session, Depends(get_db)], request: Request, get_user = Depends(get_current_user)):
    if get_user.get('is_user'):
        snt = db.scalars(select(Snt).where(Snt.id==get_user.get('snt_id'), Snt.is_active==True)).all()
        albums = db.scalars(select(Album).where(Album.is_active == True, Album.snt_id == get_user.get('snt_id'))).all()
        if albums == None:
            return{"Message": "Error"}

        return templates.TemplateResponse("galery.html", {"request": request, 'snt': snt[0], 'albums': albums})
    else:
        return RedirectResponse('/autorisation/')

@router.post('/', status_code=status.HTTP_201_CREATED)
async def create_album(db: Annotated[Session, Depends(get_db)], snt_id: int, create_album: CreateAlbum):
    dir_name = translit(create_album.name, 'ru', reversed=True)
    dir_name = dir_name.replace(' ','_')
    album_path = os.path.join(UPLOAD_DIRECTORY, dir_name)
    db.execute(insert(Album).values(
        name= create_album.name,
        description= create_album.description,
        path= album_path,
        snt_id = snt_id,
        photos_count = 0
    ))
    db.commit()
    os.makedirs(album_path, exist_ok=True)
    return {
        'status_code': status.HTTP_201_CREATED,
        'transaction': "Succeful"
    }

@router.get('/{album_id}')
async def get_photos_page(db: Annotated[Session, Depends(get_db)],
                          album_id: int,
                          request: Request, get_user = Depends(get_current_user)):
    if get_user.get('is_user'):
        snt = db.scalars(select(Snt).where(Snt.id==get_user.get('snt_id'), Snt.is_active==True)).all()
        photos = db.scalars(select(Photo).where(Photo.album_id == album_id, Photo.is_active==True)).all()
        album_name = db.scalars(select(Album.name).where(Album.id == album_id)).all()
        for photo in photos:
            photo.image_path = photo.image_path[12:]
        return templates.TemplateResponse('album.html', {"request": request, 'snt': snt[0], 'photos': photos, 'album_title': album_name[0]})
    else:
        return RedirectResponse('/autorisation/')

@router.post('/{album_id}', status_code=status.HTTP_201_CREATED)
async def add_photo(db: Annotated[Session, Depends(get_db)],
                    album_id: int,
                    name: str=Form(...),
                    description: Optional[str]=Form(None),
                    file: UploadFile = File(...)):

    dir_path = db.scalar(select(Album.path).where(Album.id == album_id, Album.is_active==True))
    file_location = os.path.join(dir_path, file.filename)
    with open(file_location, "wb") as f:
        f.write(await file.read())

    db.execute(insert(Photo).values(
        name= name,
        description= description,
        image_path= file_location,
        album_id= album_id
    ))
    db.commit()
    count = db.scalar(select(Album.photos_count).where(Album.id == album_id))
    count+= 1
    db.execute(update(Album).values(
        photos_count= count
    ))
    db.commit()
    return {
        'status_code': status.HTTP_201_CREATED,
        'transaction': "Succeful"
    }




