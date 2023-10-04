from pydantic import BaseModel, computed_field, field_validator, HttpUrl, IPvAnyAddress


class BarkConfig(BaseModel, validate_assignment=True):
    url: HttpUrl | IPvAnyAddress = "http://127.0.0.1"
    port: int = 8081

    @computed_field(repr=False)
    @property
    def bark_url(self) -> str:
        url = f"{self.url}:{self.port}"
        return url

    @field_validator("url")
    def url_validator(self, value: HttpUrl | IPvAnyAddress | str):
        if not isinstance(value, str):
            value = str(value)

        if value.endswith("/"):
            return value[:-1]

        return value

config = BarkConfig()
