from enum import Enum
from functools import partial

import attr
import marshmallow as ma
from marshmallow_annotations import registry
from marshmallow_annotations.ext.attrs import AttrsSchema
from marshmallow_enum import EnumField


class ConvertException(Exception):
    def __init__(self, **kwargs):
        self.attr = kwargs


class MarshEnum(str, Enum):
    """
    Custom enum class that works with marshmellow and attrs
    """
    @classmethod
    def convert(cls, value, default):
        try:
            if value is None:
                return cls[default]
            return cls[value]
        except KeyError as e:
            raise ConvertException(cls=cls.__name__, messgae=str(e))

    @classmethod
    def converter(cls, converter, subtypes, opts):
        return cls.field(**opts)

    @classmethod
    def field(cls, **kwargs):
        return EnumField(cls,
                         validate=ma.validate.OneOf(cls),
                         load_by=EnumField.VALUE,
                         dump_by=EnumField.VALUE,
                         **kwargs)

    def __new__(cls, *args, **kwargs):
        x = super().__new__(cls, *args, **kwargs)

        registry.register(cls, cls.converter)

        return x

    @classmethod
    def attrib(cls, **kwargs):
        return attr.ib(converter=partial(cls.convert,
                                         default=kwargs.get('default', None)),
                       validator=attr.validators.instance_of(cls),
                       **kwargs)


class GreetingType(MarshEnum):
    FORMAL = 'formal'
    CAUSAL = 'casual'


class GreetingArgs(ma.Schema):
    greeting_type = GreetingType.field()


@attr.s(auto_attribs=True)
class Reply:
    greeting_type: GreetingType
    message: str
    user: dict = None


class ReplySchema(AttrsSchema):
    class Meta:
        target = Reply
        register_as_scheme = True
