from dataclasses import dataclass
import os
import re

from dotenv import load_dotenv


@dataclass(frozen=True)
class Settings:
    bot_token: str
    admin_ids: list[int]
    data_dir: str
    telegram_proxy_url: str | None
    bot_mode: str
    webhook_base_url: str | None
    webhook_path: str
    webhook_secret: str | None
    web_host: str
    web_port: int


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


def _normalize_webhook_secret(raw_value: str) -> str | None:
    secret = raw_value.strip()
    if not secret:
        return None

    normalized = re.sub(r"[^A-Za-z0-9_-]", "_", secret)
    return normalized[:256] or None


def load_settings() -> Settings:
    load_dotenv()

    bot_token = os.getenv("BOT_TOKEN", "").strip()
    if not bot_token:
        raise RuntimeError(
            "Не задан BOT_TOKEN. Создайте .env по примеру .env.example."
        )

    data_dir = os.getenv("DATA_DIR", "data").strip() or "data"
    telegram_proxy_url = os.getenv("TELEGRAM_PROXY_URL", "").strip() or None
    bot_mode = os.getenv("BOT_MODE", "polling").strip().lower() or "polling"
    webhook_path = os.getenv("WEBHOOK_PATH", "/webhook").strip() or "/webhook"
    webhook_secret = _normalize_webhook_secret(os.getenv("WEBHOOK_SECRET", ""))
    web_host = os.getenv("WEB_HOST", "0.0.0.0").strip() or "0.0.0.0"

    webhook_base_url = os.getenv("WEBHOOK_BASE_URL", "").strip() or None
    webhook_hostname = (
        os.getenv("WEBHOOK_HOSTNAME", "").strip()
        or os.getenv("RENDER_EXTERNAL_HOSTNAME", "").strip()
    )
    if webhook_base_url is None and webhook_hostname:
        webhook_base_url = f"https://{webhook_hostname}"

    try:
        web_port = int(os.getenv("PORT", "8080"))
    except ValueError as exc:
        raise ValueError("PORT должен быть числом.") from exc

    return Settings(
        bot_token=bot_token,
        admin_ids=_parse_admin_ids(os.getenv("ADMIN_IDS", "")),
        data_dir=data_dir,
        telegram_proxy_url=telegram_proxy_url,
        bot_mode=bot_mode,
        webhook_base_url=webhook_base_url,
        webhook_path=webhook_path,
        webhook_secret=webhook_secret,
        web_host=web_host,
        web_port=web_port,
    )
