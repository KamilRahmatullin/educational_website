from typing import Annotated

from fastapi import APIRouter, Path

# router /items/directories
items_router = APIRouter(prefix='/item')


@items_router.get('/{item_id}/')
def get_item_by_id(item_id: Annotated[int, Path(ge=1, lt=1_000_000)]):
    return {'item_id':
        {
            'id': item_id
        }
    }
