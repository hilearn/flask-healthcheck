import attr
from marshenum import RegisteredEnum
from marshenum import attr_with_schema


class GreetingType(RegisteredEnum):
    FORMAL = 'formal'
    CAUSAL = 'casual'


@attr_with_schema(register_as_scheme=True)
@attr.s(auto_attribs=True)
class GreetingArgs:
    greeting_type: GreetingType


@attr_with_schema(register_as_scheme=True)
@attr.s(auto_attribs=True)
class Reply:
    greeting_type: GreetingType
    message: str
    user: dict = None
