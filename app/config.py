from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    app_name: str = "Vehicle Tracking API"
    secret_key: str = "change-this-secret-in-production"
    access_token_expire_minutes: int = 60 * 24
    database_url: str = "postgresql+psycopg://postgres:postgres@db:5432/tracking"
    mqtt_host: str = "mqtt"
    mqtt_port: int = 1883
    mqtt_topic: str = "vehicles/+/gps"
    cors_origins: str = "*"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()
