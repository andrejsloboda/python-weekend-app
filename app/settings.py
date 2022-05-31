from pydantic import BaseSettings


class Settings(BaseSettings):
    db_hostname: str
    db_user: str
    db_password: str
    db_port: int
    db_database: str
    redis_key_prefix: str
    redis_password: str
    redis_host: str
    redis_port: int
    redis_db: int
    redis_decode_responses: bool
    regiojet_base_url: str
    regiojet_locations_url: str
    regiojet_currency_rates: str

    """ class Config:
        env_file = "../.env" """


settings = Settings()


