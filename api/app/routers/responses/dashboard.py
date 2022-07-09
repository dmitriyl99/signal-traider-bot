from pydantic import BaseModel


class UsersStatisticsResponse(BaseModel):
    all_users_count: int
    new_users_count: int
    growth_users_count: int
