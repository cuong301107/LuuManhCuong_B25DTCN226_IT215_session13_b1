from pydantic import BaseModel, Field
from enum import Enum
from typing import Optional, Any
from datetime import datetime, timezone


class MenuStatus(str, Enum):
    AVAILABLE = "AVAILABLE"
    OUT_OF_STOCK = "OUT_OF_STOCK"


class MenuItemBase(BaseModel):
    dish_code: str = Field(
        min_length=1, description="Mã món ăn không được rỗng")
    dish_name: str = Field(
        min_length=1, description="Tên món ăn không được rỗng")
    calorie_count: int = Field(gt=0, description="Calo phải lớn hơn 0")
    price: float = Field(gt=0, description="Giá phải lớn hơn 0")
    status: MenuStatus = MenuStatus.AVAILABLE


class MenuItemCreate(MenuItemBase):
    pass


class MenuItemUpdate(BaseModel):
    dish_code: Optional[str] = Field(None, min_length=1)
    dish_name: Optional[str] = Field(None, min_length=1)
    calorie_count: Optional[int] = Field(None, gt=0)
    price: Optional[float] = Field(None, gt=0)
    status: Optional[MenuStatus] = None


class BaseResponse(BaseModel):
    statusCode: int
    message: str
    data: Optional[Any] = None
    error: Optional[Any] = None
    timestamp: str = Field(default_factory=lambda: datetime.now(
        timezone.utc).isoformat().replace("+00:00", "Z"))
    path: str