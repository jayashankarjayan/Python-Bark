from pydantic import BaseModel, computed_field, field_validator, HttpUrl, IPvAnyAddress


class BarkConfig(BaseModel, validate_assignment=True):
    url: HttpUrl | IPvAnyAddress = "http://127.0.0.1"
    port: int = 8081

    @computed_field(repr=False)
    @property
    def bark_url(self) -> str:
        url = f"{self.url}:{self.port}"
        if url.endswith("/"):
            return url[:-1]
        return url


config = BarkConfig()
