from sqlalchemy.orm import Session
from fastapi import Depends, status, HTTPException
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from api_server import schemas, models
from api_server.app_config import app_config

SQLALCHEMY_DATABASE_URL = app_config.db_url

engine = create_engine(SQLALCHEMY_DATABASE_URL)

class UserRepository:
    
    def get_or_create_user(user: schemas.User):
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        session = SessionLocal()
        userExist = session.query(models.User).filter(models.User.username == user.username).first()
        if userExist is None:
            # newUser = models.User(**user.model_dump())
            newUser = models.User(id=user.id,
                                  username=user.username,
                                  email=user.email,
                                  first_name=user.first_name,
                                  last_name=user.last_name,
                                  is_admin=user.is_admin)
            for role in user.roles:
                roleExist = session.query(models.Role).filter(models.Role.name == role.name).first()
                if roleExist is None:
                    new_role = models.Role(name=role.name)
                    session.add(new_role)
                    session.commit()
                    newUser.roles.append(new_role)
                
                else:
                    if roleExist not in newUser.roles:
                        newUser.roles.append(roleExist)
            
            session.add(newUser)
            session.commit()
            session.refresh(newUser)
            session.close()
            return newUser
        
        else:
            updated_roles = []
            for role in user.roles:
                # Kiểm tra xem vai trò đã tồn tại trong cơ sở dữ liệu hay chưa
                roleExist = session.query(models.Role).filter_by(name=role.name).first()
                if roleExist:
                    # print(f'Role exist name: {roleExist.name}, users: {len(roleExist.users)}')
                    updated_roles.append(roleExist)
                else:
                    new_role = models.Role(name=role.name)
                    session.add(new_role)
                    session.commit()
                    updated_roles.append(new_role)
            # Cập nhật vai trò của người dùng
            userExist.roles = updated_roles
            session.commit()
            session.refresh(userExist)
            session.close()
            return userExist

    def get_users(db: Session):
        return db.query(models.User).all()

    def get_user(db: Session, username: str):
        user = db.query(models.User).filter(models.User.username == username).first()
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with the 'username: {username}' not found")
        return user
    
    def delete_user(db: Session, username: str):
        user = db.query(models.User).filter(models.User.username == username).first()
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with the 'username: {username}' not found")
        # Xóa tất cả các hàng từ bảng user_roles mà tham chiếu đến người dùng được xóa
        db.query(models.user_roles).filter(models.user_roles.c.username == username).delete()
        # Xóa người dùng từ bảng users
        db.delete(user)
        db.commit()
        return {"message": "User deleted successfully"}
    
    def get_roles(db: Session):
        return db.query(models.Role).all()
