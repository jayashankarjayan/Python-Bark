from pydantic import BaseModel, computed_field, field_validator


class BarkConfig(BaseModel):
    url: str = "http://127.0.0.1"
    port: int = 8081

    @field_validator("url")
    def validate_url(cls, value: str):
        if not value.startswith("http"):
            raise TypeError("Invalid url provided")
        return value.strip()

    @computed_field
    @property
    def bark_url(self) -> str:
        if not self.url.startswith("http"):
            raise TypeError("Invalid url provided")
        url = f"{self.url}:{self.port}"
        if url.endswith("/"):
            return url[:-1]
        return url


config = BarkConfig()
