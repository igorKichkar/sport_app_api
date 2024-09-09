from datetime import datetime

from typing import Annotated

from fastapi import Depends, APIRouter, HTTPException
from sqlalchemy.orm import Session

from app.orm import crud, schemas
from app.dependencies import get_db, get_current_user

router = APIRouter()

current_user = Annotated[schemas.User, Depends(get_current_user)]

@router.get("/item/{item_id}", response_model=schemas.Item)
def read_item(current_user: current_user, 
              item_id: int, 
              db: Session = Depends(get_db)):
    item = crud.get_item(db, item_id, current_user.id)

    # crud.create_image(db, image = schemas.ImageCreate(path="some/path", item_id=1))

    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return item
  
@router.post("/item/", response_model=schemas.Item)
def create_item(current_user: current_user, 
              item: schemas.ItemCreate, 
              db: Session = Depends(get_db)):
    item.owner_id = current_user.id
    item.created_date = datetime.now()
    new_item = crud.create_user_item(db, item)
    return new_item


@router.put("/item/{item_id}", response_model=schemas.Item)
def update_item(current_user: current_user,
              item: schemas.ItemUpdate, 
              item_id: int, 
              db: Session = Depends(get_db)):
    item.updated_date = datetime.now()
    item = crud.update_item(db, item, item_id, current_user.id)

    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return item

@router.delete("/item/{item_id}", response_model=schemas.Item)
def delete_item(current_user: current_user,
            
              item_id: int, 
              db: Session = Depends(get_db)):
   
   item = crud.delete_item(db, item_id, current_user.id)

   if item is None:
        raise HTTPException(status_code=404, detail="Item not found") 
   
   return item

    