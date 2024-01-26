import dataclasses

from pydantic import BaseModel


class BaseError(BaseModel):
    code: int
    details: str


class BadRequestModel(BaseError):
    code = 422
    details = "Bad request data were received. "


class TaskRunning(BaseError):
    code = 423
    details = "There is runnig task already. Only stop event is acceptable."


class TaskAborted(BaseError):
    code = 200
    details = "Task were successful aborted."


