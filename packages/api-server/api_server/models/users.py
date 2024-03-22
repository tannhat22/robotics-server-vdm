from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Table
from sqlalchemy.orm import relationship

from api_server.database import Base

user_roles = Table("user_roles", Base.metadata,
                   Column("username", String(255), ForeignKey("users.username")),
                   Column("role_name", String(255), ForeignKey("roles.name")))

class User(Base):
    __tablename__ = "users"

    id = Column(String(255))
    username = Column(String(255), primary_key=True)
    email = Column(String(255))
    first_name = Column(String(255))
    last_name = Column(String(255))
    is_admin = Column(Boolean)

    roles = relationship('Role', secondary=user_roles, back_populates="users")

class Role(Base):
    __tablename__ = "roles"

    name = Column(String(255), primary_key=True)

    users = relationship('User', secondary=user_roles, back_populates='roles')
