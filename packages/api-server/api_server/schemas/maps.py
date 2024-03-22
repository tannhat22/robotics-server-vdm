import os
from pydantic import BaseModel, validator

class Map(BaseModel):
    name: str 
    directory: str

    @validator('directory')
    def validate_directory(cls, v):
        # Thực hiện kiểm tra về đường dẫn ở đây
        if not os.path.isdir(v):
            raise ValueError('Invalid directory path')
        return v

    class Config:
        from_attributes = True
