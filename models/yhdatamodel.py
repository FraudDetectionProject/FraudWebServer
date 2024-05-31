from pydantic import BaseModel, Field
from typing import Any

class FileasJSON(BaseModel):
    checkfraud: bool
    file: str

class DataModel(BaseModel):
    transcript: str = ''

class SuccessResponse(BaseModel):
    resultCode: bool = True
    fraudCode: int = Field(-1, description="Fraud code")
    probability: float = Field(0.0, description="Probability of fraud")
    reasoncode: int = Field(0, description="Reason code")
    reasondetails: str = Field('success', description="Reason details")
    data: Any = Field(DataModel(), description="Data")

class FailureResponse(BaseModel):
    resultCode: bool = False
    reasoncode: int = Field(..., description="Reason code")
    reasondetails: str = Field(..., description="Reason details")

FLAGREASONS = {
    1: 'Audio duration is less then 30',
    2: 'File type is not valid'
}