from abc import (
    ABC,
    abstractmethod,
)
from dataclasses import (
    dataclass,
    field,
)

from app.logic.queries.base import (
    BaseQuery,
    QR,
    QT,
    QueryHandler,
)


@dataclass(frozen=True)
class QueryMediator(ABC):
    queries_map: dict[QT, QueryHandler] = field(
        default_factory=dict,
        kw_only=True,
    )

    @abstractmethod
    def register_query(self, query: QT, query_handler: QueryHandler[QT, QR]):
        ...

    @abstractmethod
    async def handle_query(self, query: BaseQuery) -> QR:
        ...
