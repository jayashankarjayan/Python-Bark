from typing import Dict, Any
from pydantic import BaseModel, field_validator, Field


class LogObject(BaseModel):
    id: int | None = None
    log_level: str = Field(serialization_alias="logLevel")
    service_name: str = Field(serialization_alias="serviceName")
    code: str | int
    msg: str
    more_data: Dict[str, Any] | None = Field(
        serialization_alias="moreData", default_factory=dict
    )

    @property
    def payload(self):
        _payload = self.model_dump(by_alias=True)

        if not self.id:
            _payload.pop("id")

        return _payload

    @field_validator("code")
    def convert_code(cls, value: str | int):
        if isinstance(value, int):
            return str(value)
        return value

    @field_validator("more_data")
    def validate_more_data(cls, value: Dict[str, Any] | None):
        if not value:
            value = {}

        return value
