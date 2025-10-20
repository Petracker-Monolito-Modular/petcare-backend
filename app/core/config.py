from pydantic_settings import BaseSettings
from pydantic import Field

class Settings(BaseSettings):
    mongo_uri: str = Field(default="mongodb://localhost:27017")
    mongo_db: str = Field(default="petcare_dev")

    jwt_secret: str = Field(default="CHANGE_ME")
    jwt_alg: str = Field(default="HS256")
    jwt_expire_min: int = Field(default=30)

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()
