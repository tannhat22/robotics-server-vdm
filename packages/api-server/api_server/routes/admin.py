from typing import List, Tuple, cast

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from api_server import schemas, database
from api_server.authKeycloak import get_user_info
from api_server.repositories import UserRepository

def admin_dep(user: schemas.User = Depends(get_user_info)):
    if not user.is_admin:
        raise HTTPException(403,"User does not have permission to access this content")
    
router = APIRouter(tags=["Admin"], dependencies=[Depends(admin_dep)])

get_db = database.get_db

# Tạo 1 user mới
# @router.post("", status_code=status.HTTP_201_CREATED)
# def create_user(request: schemas.UserSchema, db: Session = Depends(get_db)):
#     return UserRepository.get_or_create_user(db, request)

# Lấy tất cả dữ liệu users
@router.get("/users", response_model=List[schemas.User])
def get_users(db: Session = Depends(get_db)):
    return UserRepository.get_users(db)

# Lấy dữ liệu của user theo username
@router.get("/users/{username}", status_code=status.HTTP_200_OK, response_model=schemas.User)
def get_user(username: str, db: Session = Depends(get_db)):
    return UserRepository.get_user(db, username)

# Xóa user theo username
@router.delete("/users/{username}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(username: str, db: Session = Depends(get_db)):
    return UserRepository.delete_user(db, username)

# Lấy tất cả roles
@router.get("/roles", status_code=status.HTTP_200_OK, response_model=list[schemas.Role])
def get_roles(db: Session = Depends(get_db)):
    return UserRepository.get_roles(db)