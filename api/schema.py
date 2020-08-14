import attr
from marshenum import attr_with_schema
from store.models import GreetingType


@attr_with_schema(register_as_scheme=True)
@attr.s(auto_attribs=True)
class GreetingArgs:
    greeting_type: GreetingType
