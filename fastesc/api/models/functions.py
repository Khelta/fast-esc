from typing import Type

from pydantic import BaseModel, Field


def add_id(base: Type[BaseModel]) -> Type[BaseModel]:
    """Return a new Pydantic model based on `base` with an `id` field added."""
    namespace = {
        '__annotations__': {'id': int},
        'id': Field()
    }
    cls_name = f"{base.__name__}WithId"
    return type(cls_name, (base,), namespace)
