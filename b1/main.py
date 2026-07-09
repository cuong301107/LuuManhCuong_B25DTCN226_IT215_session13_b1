from fastapi import FastAPI, Depends, Request
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from database import engine, get_db, Base
import schemas
import service

Base.metadata.create_all(bind=engine)

app = FastAPI()


def build_response(status_code: int, message: str, path: str, data=None, error=None):
    safe_data = jsonable_encoder(data) if data else None
    response_obj = schemas.BaseResponse(
        statusCode=status_code, message=message, path=path, data=safe_data, error=error
    )
    return JSONResponse(status_code=status_code, content=jsonable_encoder(response_obj))


@app.post("/menu-items")
def create(item: schemas.MenuItemCreate, request: Request, db: Session = Depends(get_db)):
    data, error = service.create_item(db, item)
    if error == "Dish code already exists":
        return build_response(400, "Mã món ăn đã tồn tại", request.url.path, error="Bad Request")
    elif error:
        return build_response(500, "Lỗi hệ thống", request.url.path, error=error)
    return build_response(201, "Thêm món ăn thành công", request.url.path, data=data)


@app.get("/menu-items")
def get_all(request: Request, db: Session = Depends(get_db)):
    data = service.get_all_items(db)
    return build_response(200, "Lấy danh sách thành công", request.url.path, data=data)


@app.get("/menu-items/{item_id}")
def get_one(item_id: int, request: Request, db: Session = Depends(get_db)):
    data = service.get_item_by_id(db, item_id)
    if not data:
        return build_response(404, "Menu item not found", request.url.path, error="Not Found")
    return build_response(200, "Lấy thông tin thành công", request.url.path, data=data)


@app.put("/menu-items/{item_id}")
def update(item_id: int, item: schemas.MenuItemUpdate, request: Request, db: Session = Depends(get_db)):
    data, error = service.update_item(db, item_id, item)
    if error == "Menu item not found":
        return build_response(404, "Menu item not found", request.url.path, error="Not Found")
    elif error == "Dish code already exists":
        return build_response(400, "Mã món ăn đã tồn tại", request.url.path, error="Bad Request")
    elif error:
        return build_response(500, "Lỗi hệ thống", request.url.path, error=error)
    return build_response(200, "Cập nhật món ăn thành công", request.url.path, data=data)


@app.delete("/menu-items/{item_id}")
def delete(item_id: int, request: Request, db: Session = Depends(get_db)):
    success, error = service.delete_item(db, item_id)
    if error == "Menu item not found":
        return build_response(404, "Menu item not found", request.url.path, error="Not Found")
    elif error:
        return build_response(500, "Lỗi hệ thống", request.url.path, error=error)
    return build_response(200, "Xóa món ăn thành công", request.url.path)
