from pydantic_settings import BaseSettings

class EnvConfig(BaseSettings):
    AIRTOP_API_KEY: str
    LANGCHAIN_API_KEY: str
    LANGCHAIN_TRACING_V2: bool = False
    TAVILY_API_KEY: str
    OPENAI_API_KEY: str

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

env_config = EnvConfig()
