import dataclasses

from pydantic import BaseModel


class BaseError(BaseModel):
    code: int
    details: str


class BadRequestModel(BaseError):
    code: int = 422
    details: str = "Bad request data were received. "


class TaskRunning(BaseError):
    code: int = 423
    details: str = "There is runnig task already. Only stop event is acceptable."


class TaskAborted(BaseError):
    code: int = 200
    details: str = "Task were successful aborted."


