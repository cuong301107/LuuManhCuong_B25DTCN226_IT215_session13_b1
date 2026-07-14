from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
import models
import schemas


def create_item(db: Session, item: schemas.MenuItemCreate):
    try:
        new_item = models.MenuItem(**item.model_dump())
        db.add(new_item)
        db.commit()
        db.refresh(new_item)
        return new_item, None
    except IntegrityError:
        db.rollback()
        return None, "Dish code already exists"
    except Exception as e:
        db.rollback()
        return None, str(e)


def get_all_items(db: Session):
    return db.query(models.MenuItem).all()


def get_item_by_id(db: Session, item_id: int):
    return db.query(models.MenuItem).filter(models.MenuItem.id == item_id).first()


def update_item(db: Session, item_id: int, item_in: schemas.MenuItemUpdate):
    item = get_item_by_id(db, item_id)
    if not item:
        return None, "Menu item not found"

    try:
        update_data = item_in.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(item, key, value)

        db.commit()
        db.refresh(item)
        return item, None
    except IntegrityError:
        db.rollback()
        return None, "Dish code already exists"
    except Exception as e:
        db.rollback()
        return None, str(e)


def delete_item(db: Session, item_id: int):
    item = get_item_by_id(db, item_id)
    if not item:
        return False, "Menu item not found"

    try:
        db.delete(item)
        db.commit()
        return True, None
    except Exception as e:
        db.rollback()
        return False, str(e)