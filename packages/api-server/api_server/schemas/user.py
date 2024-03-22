from pydantic import BaseModel

class UserBase(BaseModel):
    id: str
    username: str
    email: str
    first_name: str
    last_name: str
    is_admin: bool

    class Config:
        from_attributes = True

class Role(BaseModel):
    name: str

    class Config:
        from_attributes = True

class User(UserBase):
    roles: list[Role] = []

# class RoleSchema(RoleBase):
#     users: list[UserBase] = []


