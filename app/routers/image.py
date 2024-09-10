import random
import string
import time
import shutil
import datetime
from typing import Annotated

from fastapi import APIRouter, UploadFile, Depends, Form, HTTPException
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from PIL import Image  # Импортируем библиотеку Pillow

from app.orm import schemas
from app.dependencies import get_db, get_current_user
from app.orm import crud

router = APIRouter()

current_user = Annotated[schemas.User, Depends(get_current_user)]

IMAGE_DIR = "app/files/"
# Целевые размеры изображения
TARGET_SIZE = (800, 600)


@router.post("/images/")
async def upload_images(
    images: list[UploadFile],
    item_id: Annotated[int, Form()],
    current_user: current_user,
    db: Session = Depends(get_db)
):
    # get_item проверяет и владельца
    item_parrent = crud.get_item(db, item_id, current_user.id)

    if item_parrent is None:
        raise HTTPException(
            status_code=401, detail="The user is not the owner of the Item")

    result = []
    for image in images:
        image_format = image.filename.split(".")[-1]
        image_title = ''.join(random.choice(string.ascii_letters)
                              for i in range(16)) + str(time.time_ns())
        image_on_disck = f"{IMAGE_DIR}image_{image_title}.{image_format}"
        image_indb = f"image_{image_title}.{image_format}"

        # Открываем изображение через Pillow
        with Image.open(image.file) as img:
            width, height = img.size

            # Если размеры изображения больше, чем целевые, меняем размер
            if width > TARGET_SIZE[0] or height > TARGET_SIZE[1]:
                img = img.resize(TARGET_SIZE)

            # Сохраняем изображение на диск (с измененным или исходным размером)
            img.save(image_on_disck)

        # Сохраняем информацию об изображении в БД
        image_in_db = crud.create_image(db, schemas.ImageCreate(title=image_indb,
                                                                item_id=item_id,
                                                                owner_id=current_user.id,
                                                                created_date=datetime.datetime.now()))
        print(image_in_db.__dict__)
        result.append({
            "id": image_in_db.id,
            "title": image_in_db.title,
            "item_id": image_in_db.item_id,
            "owner_id": image_in_db.owner_id,
            "is_main": image_in_db.is_main,
            "created_date": image_in_db.created_date,
        })
    return {"success_add": result}


@router.get("/images/{title}")
async def download_image(title: str, current_user: current_user, db: Session = Depends(get_db)):
    check_owner = crud.get_image_owner_id(db, title, current_user.id)
    print(IMAGE_DIR+title)
    if check_owner is None:
        raise HTTPException(status_code=404, detail="File not found")
    return FileResponse(f"{IMAGE_DIR + title}")


@router.delete("/images/{image_id}")
def delete_image(current_user: current_user,
              image_id: int,
              db: Session = Depends(get_db)):

   image = crud.delete_image(db, image_id, current_user.id)

   if image is None:
        raise HTTPException(status_code=404, detail="Image not found")

   return {"success_remove": image}
