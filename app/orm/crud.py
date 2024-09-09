from sqlalchemy.orm import Session
from passlib.context import CryptContext

from . import models, schemas


def get_password_hash(password):
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    return pwd_context.hash(password)


def get_user(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def get_user_by_id(db: Session, id: int):
    return db.query(models.User).filter(models.User.id == id).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = get_password_hash(user.password)
    db_user = models.User(
        email=user.email, hashed_password=hashed_password, nickname=user.nickname)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_item(db: Session, item_id: int, user_id: int):
    return db.query(models.Item).filter(
        models.Item.id == item_id).filter(models.Item.owner_id == user_id).first()


def get_items(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Item).offset(skip).limit(limit).all()


def create_user_item(db: Session, item: schemas.ItemCreate):
    db_item = models.Item(**item.model_dump())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


def delete_item(db: Session, item_id: int, user_id: int):
    item = db.query(models.Item).filter(models.Item.id == item_id).filter(
        models.Item.owner_id == user_id).first()

    if item is None:
        return None

    db.delete(item)
    db.commit()
    return item


def create_image(db: Session, image: schemas.ImageCreate):
    db_image = models.Image(**image.model_dump())
    db.add(db_image)
    db.commit()
    db.refresh(db_image)
    return db_image


def delete_image(db: Session, image_id: int, user_id: int):
    image = db.query(models.Image).filter(models.Image.id == image_id).filter(models.Image.owner_id == user_id
                                                                              ).first()

    if image is None:
        return None

    db.delete(image)
    db.commit()
    return image


def get_exercise(db: Session, exercise_id: int):
    return db.query(models.Exercise).filter(models.Exercise.id == exercise_id).first()


def create_item_exercise(db: Session, exercise: schemas.ExerciseCreate):
    db_exercise = models.Exercise(**exercise.model_dump())
    db.add(db_exercise)
    db.commit()
    db.refresh(db_exercise)
    return db_exercise


def delete_exercise(db: Session, exercise_id: int, user_id: int):
    exercise = db.query(models.Exercise).filter(models.Exercise.id == exercise_id).filter(models.Exercise.owner_id == user_id
                                                                                          ).first()

    if exercise is None:
        return None

    db.delete(exercise)
    db.commit()
    return exercise


def get_approach(db: Session, approach_id: int):
    return db.query(models.Approach).filter(models.Approach.id == approach_id).first()


def create_exercise_approach(db: Session, approach: schemas.ApproachCreate):
    db_approach = models.Approach(**approach.model_dump())
    db.add(db_approach)
    db.commit()
    db.refresh(db_approach)
    return db_approach


def delete_approach(db: Session, approach_id: int, user_id: int):
    approach = db.query(models.Approach).filter(models.Approach.id == approach_id).filter(models.Approach.owner_id == user_id
                                                                                          ).first()

    if approach is None:
        return None

    db.delete(approach)
    db.commit()
    return approach


def get_image_owner_id(db: Session, image_title: str, user_id):
    return db.query(models.Image).filter(models.Image.title == image_title).filter(models.Image.owner_id == user_id).first()


def update_item(db: Session, item: schemas.ItemUpdate, item_id: int, user_id: int):

    updating_item = db.query(models.Item).filter(
        models.Item.id == item_id).filter(models.Item.owner_id == user_id).first()
    if updating_item is None:
        return None

    if item.title is not None:
        updating_item.title = item.title
    if item.description is not None:
        updating_item.description = item.description
    updating_item.updated_date = item.updated_date

    db.add(updating_item)
    db.commit()
    db.refresh(updating_item)
    return updating_item
