import uvicorn
from alembic import command
from alembic.config import Config

from src.core import get_logger, settings

logger = get_logger(__name__)

if __name__ == "__main__":
    try:
        alembic_cfg = Config("alembic.ini")
        command.upgrade(alembic_cfg, "heads")
    except Exception as error:
        logger.error(f"Failing to apply migrations: {error}", exc_info=True)

    uvicorn.run(
        "src.app:create_app",
        host=settings.app.host,
        port=settings.app.port,
        reload=settings.app.reload,
        factory=True,
    )
