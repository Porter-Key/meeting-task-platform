from __future__ import annotations

import strawberry

from web.graphql.mutations import Mutation
from web.graphql.queries import Query

schema = strawberry.Schema(query=Query, mutation=Mutation)
