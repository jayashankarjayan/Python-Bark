from typing import Dict, Any
from pydantic import BaseModel, field_validator


d = {
    "id": -100,
    "logLevel": "info",
    "serviceName": "TestPostman",
    "code": "1KE0H8",
    "msg": "Shows up in DB or not?",
    "moreData": {"name": "vaibhav"},
}


class LogObject(BaseModel):
    id: int | None = None
    log_level: str
    service_name: str
    code: str | int
    msg: str
    more_data: Dict[str, Any] = {}

    @property
    def payload(self):
        _data = {
            "id": -100,
            "logLevel": "info",
            "serviceName": "TestPostman",
            "code": "1KE0H8",
            "msg": "Shows up in DB or not?",
            "moreData": {"name": "vaibhav"},
        }
        _payload = self.model_dump()

        if not self.id:
            _payload.pop("id")

        _payload["serviceName"] = _payload.pop("service_name")
        _payload["logLevel"] = _payload.pop("log_level")
        _payload["moreData"] = _payload.pop("more_data")

        return _payload

    @field_validator("code")
    def convert_code(cls, value: str | int):
        if isinstance(value, int):
            return str(value)
