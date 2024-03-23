# from typing import List, Tuple, cast
from fastapi import APIRouter, Depends, HTTPException, status
# from sqlalchemy.orm import Session

# from api_server.fast_io import FastIORouter, SubscriptionRequest
from api_server import schemas, models
from api_server.authenticator import user_dep
# from api_server.authKeycloak import get_user_info
# from api_server.repositories import UserRepository

router = APIRouter()


@router.get("/user", response_model=schemas.User)
async def get_user(user: schemas.User = Depends(user_dep)):
    """
    Get the currently logged in user
    """
    return user

