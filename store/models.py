from sqlalchemy import Column, String, Enum
from .database import db
from marshenum import RegisteredEnum

from marshenum import model_with_schema


class GreetingType(RegisteredEnum):
    FORMAL = 'formal'
    CAUSAL = 'casual'


@model_with_schema(register_as_scheme=True, strict=True)
class Reply(db.Model):
    __tablename__ = 'replies'

    category: GreetingType = Column(Enum(GreetingType), primary_key=True)
    reply_msg: str = Column(String)
