from pydantic import BaseModel


class UsersStatisticsResponse(BaseModel):
    all_users_count: int
    new_users_count: int
    growth_users_count: int


class SubscriptionStatisticsResponse(BaseModel):
    all_active_subscriptions_count: int
    new_subscriptions_count: int
    subscriptions_growth_count: int
    users_without_subscriptions_count: int
