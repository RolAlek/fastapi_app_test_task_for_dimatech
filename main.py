import uvicorn
from alembic import command
from alembic.config import Config

from src.core import get_logger
from src.core.settings import AppSettings, get_settings

logger = get_logger(__name__)

if __name__ == "__main__":
    try:
        alembic_cfg = Config("alembic.ini")
        command.upgrade(alembic_cfg, "heads")
    except Exception as error:
        logger.error(f"Failing to apply migrations: {error}", exc_info=True)

    settings: AppSettings = get_settings(AppSettings)

    uvicorn.run(
        "src.app:create_app",
        host=settings.host,
        port=settings.port,
        reload=settings.reload,
        factory=True,
    )
