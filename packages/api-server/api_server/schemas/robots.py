from pydantic import BaseModel, Field, IPvAnyAddress

class Robot(BaseModel):
    serial_no: str = Field (
        description="The serial number is preset at the factory"
    )
    name: str
    ip_address: IPvAnyAddress

    class Config:
        from_attributes = True
