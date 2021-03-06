"""
Create .serialize and .parse methods to handle json operations

Where orjson is installed, the performance impact is nil,
without orjson, parsing is about as fast as ujson, however
serialization is slower, although still faster than the 
native json library. 
"""
from typing import Any
import datetime
from ..logging import get_logger
try:
    # if orjson is available, use it
    import orjson

    parse = orjson.loads

    def serialize(obj: Any, indent: bool = False) -> str:
        # return a string
        if indent and isinstance(obj, dict):
            return orjson.dumps(obj, option=orjson.OPT_INDENT_2 + orjson.OPT_SORT_KEYS).decode()
        else:
            return orjson.dumps(obj, option=orjson.OPT_SORT_KEYS).decode()


except ImportError:  # pragma: no cover
    # orjson doesn't install on 32bit systems so we need a backup plan
    # however, orjson and ujson have functional differences so we can't
    # just swap the references.
    import ujson

    logger = get_logger()
    logger.warning('orjson not installed using ujson')

    def serialize(obj: Any, indent: bool = False) -> str:   # type:ignore

        def fix_fields(dt: Any) -> str:
            """
            orjson and ujson handles some fields differently,
            if one of those fields is detected, fix it. 
            """
            if isinstance(dt, (datetime.date, datetime.datetime)):
                return dt.isoformat()
            return dt

        if isinstance(obj, dict):
            obj_copy = {k:fix_fields(v) for k,v in obj.items()}

        if indent:
            return ujson.dumps(obj_copy, sort_keys=True, indent=2)
        else:
            return ujson.dumps(obj_copy, sort_keys=True)

    parse = ujson.loads  # type:ignore
