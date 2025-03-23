__all__ = ("engine",)

from src.core import settings
from src.database.engine import DatabaseHelper

engine = DatabaseHelper(
    url=settings.database.url,
    echo=settings.database.echo,
)
