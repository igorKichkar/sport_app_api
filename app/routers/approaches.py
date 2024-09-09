from datetime import datetime

from typing import Annotated

from fastapi import Depends, APIRouter, HTTPException
from sqlalchemy.orm import Session

from app.orm import crud, schemas
from app.dependencies import get_db, get_current_user

router = APIRouter()

current_user = Annotated[schemas.User, Depends(get_current_user)]

@router.get("/approach/{approach_id}", response_model=schemas.Approach)
def read_user(current_user: current_user, 
              approach_id: int, 
              db: Session = Depends(get_db)):
    approuch = crud.get_approach(db, approach_id)

    # crud.create_image(db, image = schemas.ImageCreate(path="some/path", item_id=1))

    if approuch is None:
        raise HTTPException(status_code=404, detail="Exercise not found")
    
    if (approuch.owner_id != current_user.id):
        raise HTTPException(status_code=401, detail="Not Allowed")
    
    return approuch
  

@router.post("/approach/", response_model=schemas.Approach)
def read_user(current_user: current_user,
              approach: schemas.ApproachCreate, 
              db: Session = Depends(get_db)):
    
    exercise = crud.get_exercise(db, approach.exercise_id)

    if exercise is None:
        raise HTTPException(status_code=404, detail="Exercise not found")
    
    approach.owner_id = current_user.id
    approach.created_date = datetime.now()

    return crud.create_exercise_approach(db, approach)


@router.delete("/approach/{approach_id}", response_model=schemas.Approach)
def delete_approach(current_user: current_user,
              approach_id: int, 
              db: Session = Depends(get_db)):
   
   approach = crud.delete_approach(db, approach_id, current_user.id)

   if approach is None:
        raise HTTPException(status_code=404, detail="Item not found") 
   
   return approach
  