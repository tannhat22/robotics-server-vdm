from sqlalchemy.orm import Session
from fastapi import Depends, status, HTTPException

from api_server import schemas, models

# MAPS:
class MapRepository:

    def create_map(db: Session, map: schemas.Map):
        # Thêm lưu map và file cấu hình map vào folder static
        # save_map

        newMap = models.Map(**map.model_dump())
        db.add(newMap)
        db.commit()
        db.refresh(newMap)
        return newMap
    
    def get_maps(db: Session):
        return db.query(models.Map).all()

    def get_map(db: Session, id: int):
        map = db.query(models.Map).filter(models.Map.id == id).first()
        if not map:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Map with the 'id: {id}' not found")

        # Cần thêm trả về file map cho front-end
        # map.png
        return map
    
    def update_map(db: Session, id: int, mapUpdate: schemas.Map):
        map = db.query(models.Map).filter(models.Map.id == id)
        if not map.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Map with the 'id: {id}' not found")        
        map.update(mapUpdate.model_dump())
        db.commit()
        return {"message": "Map updated successfully"}
    
    def delete_map(db: Session, id: int):
        map = db.query(models.Map).filter(models.Map.id == id)
        if not map.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Map with the 'id: {id}' not found")
        map.delete(synchronize_session=False)
        db.commit()
        return {"message": "Map deleted successfully"}
    
    def check_name_exist(db: Session, name: str, id: int | None = None):
        # Nếu id khác None thì sẽ loại trừ id đó ra khỏi kết quả tìm kiếm
        if id is not None:
            db_map = db.query(models.Map).filter(models.Map.name == name).first()
            if (db_map and db_map.id != id):
                return db_map
            return None
        return db.query(models.Map).filter(models.Map.name == name).first()
    
    def check_directory_exist(db: Session, directory: str, id: int | None = None):
        # Nếu id khác None thì sẽ loại trừ id đó ra khỏi kết quả tìm kiếm
        if id is not None:
            db_map = db.query(models.Map).filter(models.Map.directory == directory).first()
            if (db_map and db_map.id != id):
                return db_map
            return None
        return db.query(models.Map).filter(models.Map.directory == directory).first()
    