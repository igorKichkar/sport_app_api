from datetime import datetime

from typing import Annotated

from fastapi import Depends, APIRouter, HTTPException
from sqlalchemy.orm import Session

from app.orm import crud, schemas
from app.dependencies import get_db, get_current_user

router = APIRouter()

current_user = Annotated[schemas.User, Depends(get_current_user)]

@router.get("/exercise/{exercise_id}", response_model=schemas.Exercise)
def get_exercise(current_user: current_user, 
              exercise_id: int, 
              db: Session = Depends(get_db)):
    exercise = crud.get_exercise(db, exercise_id)

    if exercise is None:
        raise HTTPException(status_code=404, detail="Exercise not found")
    
    if (exercise.owner_id != current_user.id):
        raise HTTPException(status_code=401, detail="Not Allowed")
    
    return exercise
  

@router.post("/exercise/", response_model=schemas.Exercise)
def create_exercise(current_user: current_user,
              exercise: schemas.ExerciseCreate, 
              db: Session = Depends(get_db)):
    
    item_parrent = crud.get_item(db, exercise.item_id, current_user.id)  #get_item проверяет и владельца

    if item_parrent is None:
       raise HTTPException(status_code=401, detail="The user is not the owner of the Item")

    exercise.owner_id = current_user.id
    exercise.created_date = datetime.now()

    return crud.create_item_exercise(db, exercise)


@router.delete("/exercise/{exercise_id}", response_model=schemas.Exercise)
def delete_exercise(current_user: current_user,
              exercise_id: int, 
              db: Session = Depends(get_db)):
   
   exercise = crud.delete_exercise(db, exercise_id, current_user.id)

   if exercise is None:
        raise HTTPException(status_code=404, detail="Item not found") 
   
   return exercise
  