from __future__ import annotations

from typing import Any

from pydantic import BaseModel, ConfigDict, Field, StrictBool, field_validator, model_validator


def normalize_text(value: Any) -> str:
    if not isinstance(value, str):
        raise ValueError("text must be a string")

    normalized = value.strip()
    if not normalized:
        raise ValueError("text must not be blank")

    return normalized


class TaskCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    text: str = Field(min_length=1, max_length=200)

    @field_validator("text", mode="before")
    @classmethod
    def validate_text(cls, value: Any) -> str:
        return normalize_text(value)


class TaskReplace(BaseModel):
    model_config = ConfigDict(extra="forbid")

    text: str = Field(min_length=1, max_length=200)
    done: StrictBool

    @field_validator("text", mode="before")
    @classmethod
    def validate_text(cls, value: Any) -> str:
        return normalize_text(value)


class TaskUpdate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    text: str | None = Field(default=None, min_length=1, max_length=200)
    done: StrictBool | None = None

    @field_validator("text", mode="before")
    @classmethod
    def validate_text(cls, value: Any) -> str:
        return normalize_text(value)

    @field_validator("done", mode="before")
    @classmethod
    def validate_done(cls, value: Any) -> Any:
        if value is None:
            raise ValueError("done must be a boolean")
        return value

    @model_validator(mode="after")
    def validate_at_least_one_field(self) -> "TaskUpdate":
        if not self.model_fields_set:
            raise ValueError("at least one field is required")
        return self


class TaskRead(BaseModel):
    id: int
    text: str
    done: bool
