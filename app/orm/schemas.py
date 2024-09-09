from typing import Union
from datetime import datetime
from pydantic import BaseModel


class ApproachBase(BaseModel):
    ammount: str
    exercise_id: int
    owner_id: int
    weight: Union[str, None] = None
   

class ApproachCreate(ApproachBase):
    created_date: Union[datetime, None] = None
    owner_id: Union[int, None] = None


class Approach(ApproachBase):
    id: int
    # item_id: int
    created_date: datetime

    class Config:
        from_attributes = True

########################################

class ExerciseBase(BaseModel):
    title: str
    item_id: int
    owner_id: int
   

class ExerciseCreate(ExerciseBase):
    created_date: Union[datetime, None] = None
    owner_id: Union[int, None] = None


class Exercise(ExerciseBase):
    id: int
    created_date: datetime
    approaches: list[Approach] = []

    class Config:
        from_attributes = True

    def approaches_dict(self):
        # Create a dictionary with the id as the key and the rest of the fields as the value
        return {str(approach.id): approach.dict(exclude={"id"}) for approach in self.approaches}

##########################################

class ImageBase(BaseModel):
    title: str
    is_main: bool = False
    item_id: int
    owner_id: int
   

class ImageCreate(ImageBase):
    created_date: Union[datetime, None] = None
    owner_id: Union[int, None] = None


class Image(ImageBase):
    id: int
    # item_id: int 
    created_date: datetime

    class Config:
        from_attributes = True

###########################################

class ItemDataset(BaseModel):
    pass


class ItemBase(BaseModel):
    title: str
    # owner_id: Union[int, None] = None
    updated_date: Union[datetime, None] = None
    owner_id: int
    description: Union[str, None] = None
    dataset: Union[ItemDataset, None] = None


class ItemCreate(ItemBase):
    owner_id: Union[int, None] = None
    created_date: Union[datetime, None] = None

class ItemUpdate(ItemCreate):
    pass
    # updated_date: Union[datetime, None] = None


class Item(ItemBase):
    id: int
    # owner_id: int
    created_date: datetime
    images: list[Image] = []
    exercises: list[Exercise] = []

    class Config:
        from_attributes = True

############################################ 

class UserBase(BaseModel):
    email: str
    nickname: str


class UserCreate(UserBase):
    password: str
    created_date: Union[datetime, None] = None


class User(UserBase):
    id: int
    items: list[Item] = []
    created_date: datetime

    class Config:
        from_attributes = True



