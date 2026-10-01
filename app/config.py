from dataclasses import dataclass
import os

@dataclass(frozen=True)
class Config:
    bot_token: str
    bot_name: str = "SB24"
    bot_username: str = "@SBWordBot"

def load_config() -> Config:
    token = os.getenv("BOT_TOKEN")
    if not token:
        raise RuntimeError("BOT_TOKEN environment variable is required.")
    return Config(bot_token=token)
