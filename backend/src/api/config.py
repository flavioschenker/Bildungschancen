from pydantic_settings import BaseSettings

class ApiSettings(BaseSettings):
    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8",
        "extra": "ignore",
    }
    postgres_host: str
    postgres_port: int
    postgres_db: str
    postgres_user: str
    postgres_password: str

settings = ApiSettings()  # type: ignore
