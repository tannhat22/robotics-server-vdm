from typing import List, Tuple, cast

from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

from api_server.fast_io import FastIORouter, SubscriptionRequest
from api_server import schemas, database
from api_server.repositories import MapRepository

router = FastIORouter(tags=["Maps"])

get_db = database.get_db

@router.post("", status_code=status.HTTP_201_CREATED)
def create_map(request: schemas.Map, db: Session = Depends(get_db)):
    if MapRepository.check_name_exist(db, request.name):
        raise HTTPException(status_code=400, detail="Map name already exists")
    return MapRepository.create_map(db, request)

@router.get("", response_model=List[schemas.Map])
def get_maps(db: Session = Depends(get_db)):
    return MapRepository.get_maps(db)

@router.get("/{id}", status_code=status.HTTP_200_OK, response_model=schemas.Map)
def get_map(id: int, db: Session = Depends(get_db)):
    return MapRepository.get_map(db, id)

@router.put("/{id}", status_code=status.HTTP_202_ACCEPTED)
def update_map(id: int, request: schemas.Map, db: Session = Depends(get_db)):
    if MapRepository.check_name_exist(db, request.name):
        raise HTTPException(status_code=400, detail="Map name already exists")
    return MapRepository.update_map(db, id, request)

@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_map(id: int, db: Session = Depends(get_db)):
    return MapRepository.delete_map(db, id)