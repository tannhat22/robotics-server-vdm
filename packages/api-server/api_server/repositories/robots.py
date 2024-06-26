from sqlalchemy.orm import Session
from fastapi import Depends, status, HTTPException

from api_server import schemas, models

# ROBOTS:
class RobotRepository:

    def create_robot(db: Session, robot: schemas.Robot):
        newRobot = models.Robot(**robot.model_dump())
        db.add(newRobot)
        db.commit()
        db.refresh(newRobot)
        return newRobot
    
    def get_robots(db: Session):
        return db.query(models.Robot).all()

    def get_robot(db: Session, id: int):
        robot = db.query(models.Robot).filter(models.Robot.id == id).first()
        if not robot:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Robot with the 'id: {id}' not found")
        return robot
    
    def update_robot(db: Session, id: int, robotUpdate: schemas.Robot):
        robot = db.query(models.Robot).filter(models.Robot.id == id)
        if not robot.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Robot with the 'id: {id}' not found")        
        robot.update(robotUpdate.model_dump())
        db.commit()
        return {"message": "Robot updated successfully"}
    
    def delete_robot(db: Session, id: int):
        robot = db.query(models.Robot).filter(models.Robot.id == id)
        if not robot.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Robot with the 'id: {id}' not found")
        
        robot.delete(synchronize_session=False)
        db.commit()
        return {"message": "Robot deleted successfully"}
    
    def check_serial_no_exist(db: Session, serial_no: str, id: int | None = None):
        # Nếu id khác None thì sẽ loại trừ id đó ra khỏi kết quả tìm kiếm
        if id is not None:
            db_robot = db.query(models.Robot).filter(models.Robot.serial_no == serial_no).first()
            if (db_robot and db_robot.id != id):
                return db_robot
            return None
        return db.query(models.Robot).filter(models.Robot.serial_no == serial_no).first()
    
    def check_name_exist(db: Session, name: str, id: int | None = None):
        # Nếu id khác None thì sẽ loại trừ id đó ra khỏi kết quả tìm kiếm
        if id is not None:
            db_robot = db.query(models.Robot).filter(models.Robot.name == name).first()
            if (db_robot and db_robot.id != id):
                return db_robot
            return None
        return db.query(models.Robot).filter(models.Robot.name == name).first()
    
    def check_ip_address_exist(db: Session, ip_address: str, id: int | None = None):
        # Nếu id khác None thì sẽ loại trừ id đó ra khỏi kết quả tìm kiếm
        if id is not None:
            db_robot = db.query(models.Robot).filter(models.Robot.ip_address == ip_address).first()
            if (db_robot and db_robot.id != id):
                return db_robot
            return None
        return db.query(models.Robot).filter(models.Robot.ip_address == ip_address).first()