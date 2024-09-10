import random
import string
import time
import shutil
import datetime
from typing import Annotated
from fastapi import APIRouter, UploadFile, Depends, Form, HTTPException
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from PIL import Image
import io

from app.orm import schemas
from app.dependencies import get_db, get_current_user
from app.orm import crud

router = APIRouter()

current_user = Annotated[schemas.User, Depends(get_current_user)]

IMAGE_DIR = "app/files/"
MAX_SIZE_MB = 0.2  # Максимальный размер файла в мегабайтах
MAX_SIZE_BYTES = int(MAX_SIZE_MB * 1024 * 1024)  # Переводим в байты


def resize_image_proportional(image: Image.Image, max_width: int, max_height: int) -> Image.Image:
    width, height = image.size
    width_ratio = max_width / width
    height_ratio = max_height / height
    min_ratio = min(width_ratio, height_ratio)
    new_width = int(width * min_ratio)
    new_height = int(height * min_ratio)
    return image.resize((new_width, new_height), Image.ANTIALIAS)


@router.post("/images/")
async def upload_images(
    images: list[UploadFile],
    item_id: Annotated[int, Form()],
    current_user: current_user,
    db: Session = Depends(get_db)
):
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
            # Изменяем размер изображения пропорционально
            resized_img = resize_image_proportional(img, 800, 600)

            # Сохраняем изображение на диск (с измененным размером)
            img_byte_arr = io.BytesIO()
            resized_img.save(img_byte_arr, format=img.format, quality=95)

            # Сжимаем изображение до тех пор, пока его размер не станет меньше или равен 200 КБ
            quality = 95
            while img_byte_arr.tell() > MAX_SIZE_BYTES and quality > 10:
                img_byte_arr = io.BytesIO()
                resized_img.save(img_byte_arr, format=img.format, quality=quality)
                quality -= 5

            img_byte_arr.seek(0)
            with open(image_on_disck, "wb") as f:
                f.write(img_byte_arr.read())

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
