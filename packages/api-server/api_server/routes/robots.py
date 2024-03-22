from typing import List, Tuple, cast

from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

from api_server.fast_io import FastIORouter, SubscriptionRequest
from api_server import schemas, database
from api_server.repositories import RobotRepository

router = FastIORouter(tags=["Robots"])

get_db = database.get_db

# Tạo 1 robot mới
@router.post("", status_code=status.HTTP_201_CREATED)
def create_robot(request: schemas.Robot, db: Session = Depends(get_db)):
    if RobotRepository.check_serial_no_exist(db, request.serial_no):
        raise HTTPException(status_code=400, detail="Serial_no already exists")
    elif RobotRepository.check_name_exist(db, request.name):
        raise HTTPException(status_code=400, detail="Robot Name already exists")
    elif RobotRepository.check_ip_address_exist(db, request.ip_address):
        raise HTTPException(status_code=400, detail="IP address already exists")
    return RobotRepository.create_robot(db, request)

# Lấy toàn bộ dữ liệu robots
@router.get("", response_model=List[schemas.Robot])
def get_robots(db: Session = Depends(get_db)):
    return RobotRepository.get_robots(db)

# Lấy dữ liệu 1 robot theo ID
@router.get("/{id}", status_code=status.HTTP_200_OK, response_model=schemas.Robot)
def get_robot(id: int, db: Session = Depends(get_db)):
    return RobotRepository.get_robot(db, id)

# Sửa dữ liệu robot
@router.put("/{id}", status_code=status.HTTP_202_ACCEPTED)
def update_robot(id: int, request: schemas.Robot, db: Session = Depends(get_db)):
    if RobotRepository.check_serial_no_exist(db, request.serial_no, id):
        raise HTTPException(status_code=400, detail="Serial_no already exists")
    elif RobotRepository.check_name_exist(db, request.name, id):
        raise HTTPException(status_code=400, detail="Robot name already exists")
    elif RobotRepository.check_ip_address_exist(db, request.ip_address, id):
        raise HTTPException(status_code=400, detail="IP address already exists")
    return RobotRepository.update_robot(db, id, request)

# Xóa dữ liệu robot
@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def destroy(id: int, db: Session = Depends(get_db)):
    return RobotRepository.delete_robot(db, id)