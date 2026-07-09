from dataclasses import dataclass
import os

from dotenv import load_dotenv


@dataclass(frozen=True)
class Settings:
    bot_token: str
    admin_ids: list[int]
    data_dir: str
    telegram_proxy_url: str | None


def _parse_admin_ids(raw_value: str) -> list[int]:
    admin_ids: list[int] = []

    for value in raw_value.split(","):
        value = value.strip()
        if not value:
            continue
        try:
            admin_ids.append(int(value))
        except ValueError as exc:
            raise ValueError(
                f"Некорректный Telegram ID администратора: {value}"
            ) from exc

    return admin_ids


def load_settings() -> Settings:
    load_dotenv()

    bot_token = os.getenv("BOT_TOKEN", "").strip()
    if not bot_token:
        raise RuntimeError(
            "Не задан BOT_TOKEN. Создайте .env по примеру .env.example."
        )

    data_dir = os.getenv("DATA_DIR", "data").strip() or "data"
    telegram_proxy_url = os.getenv("TELEGRAM_PROXY_URL", "").strip() or None

    return Settings(
        bot_token=bot_token,
        admin_ids=_parse_admin_ids(os.getenv("ADMIN_IDS", "")),
        data_dir=data_dir,
        telegram_proxy_url=telegram_proxy_url,
    )
