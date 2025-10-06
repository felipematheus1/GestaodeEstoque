from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    APP_NAME:str = "API Loja"
    DATABASE_URL:str = "sqlite:///./banco_de_dados.db" 
    ALLOW_NEGATIVE_STOCK: bool = False  # altere para True se quiser permitir saldo negativo
    SQLALCHEMY_ECHO: bool = False

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

# objeto settings da classe Settings
settings = Settings() 
