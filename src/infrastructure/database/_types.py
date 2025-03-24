from datetime import datetime
from typing import Annotated

from sqlalchemy import func
from sqlalchemy.orm import mapped_column

_updated_at = Annotated[
    datetime, mapped_column(server_default=func.now(), onupdate=func.now())
]
