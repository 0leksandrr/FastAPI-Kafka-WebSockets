from pydantic import BaseModel

from app.infra.repositories.filters.messages import GetMessagesFilters as GetMessagesFilterRepository


class GetMessagesFilter(BaseModel):
    limit: int = 10
    offset: int = 0

    def to_infra(self):
        return GetMessagesFilterRepository(limit=self.limit, offset=self.offset)