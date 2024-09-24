import asyncio
import json
import time
from datetime import datetime, timedelta
from typing import List

from db.models import DesignLevel, EarningsLevel, Mentor, SendLink, AiRecommendations, AiRequests, Operations
from db.repository import design_level_repository, earnings_level_repository, mentor_repository, send_link_repository, \
    ai_recommendations_repository, ai_requests_repository, operation_repository

manager = asyncio.Lock()


class Statistic:
    def __init__(self,
                 service_name: str):
        self.service_name = service_name
        self.users = []
        if self.service_name == "design_level":
            self.items: List[DesignLevel]
        elif self.service_name == "earnings_level":
            self.items: List[EarningsLevel]
        elif self.service_name == "mentor_stat":
            self.items: List[Mentor]
        elif self.service_name == "send_link_data":
            self.items: List[SendLink]
        elif self.service_name == "ai_requests":
            self.items: List[AiRequests]
        elif self.service_name == "operations_data":
            self.items: List[Operations]
        else:
            self.items = List[AiRecommendations]
        self.services_with_finished = ["design_level", "earnings_level"]

    async def get_users(self):
        if self.service_name == "design_level":
            self.users: List[DesignLevel] = await design_level_repository.select_all_users()
        elif self.service_name == "earnings_level":
            self.users: List[EarningsLevel] = await earnings_level_repository.select_all_users()
        elif self.service_name == "mentor_stat":
            self.users: List[Mentor] = await mentor_repository.select_all_users()
        elif self.service_name == "send_link_data":
            self.users: List[SendLink] = await send_link_repository.select_all_users()
        elif self.service_name == "ai_requests":
            self.users: List[AiRequests] = await ai_requests_repository.select_all_requests()
        elif self.service_name == "operations_data":
            self.users: List[Operations] = await operation_repository.select_all_operations()
        else:
            self.users: List[AiRecommendations] = await ai_recommendations_repository.select_all_users()

    async def get_statistic_by_timedelta(self, time_delta: int):
        number_start = 0
        number_finish = 0
        current_datetime = datetime.now()
        if self.service_name != "operations_data" and self.service_name != "ai_requests":
            for user in self.users:
                if (current_datetime - user.last_start_date) <= timedelta(days=time_delta):
                    number_start += 1
                    if self.service_name in self.services_with_finished and user.finish_service:
                        number_finish += 1
            return [number_start, number_finish]
        elif self.service_name == "operations_data":
            for user in self.users:
                if (current_datetime - user.creation_date) <= timedelta(days=time_delta):
                    number_start += 1
                    if user.is_paid:
                        number_finish += 1
            return [number_start, number_finish]
        else:
            for user in self.users:
                if (current_datetime - user.creation_date) <= timedelta(days=time_delta):
                    number_start += 1
            return [number_start, number_finish]

    async def get_all_statistic(self):
        number_start = 0
        number_finish = 0
        current_datetime = datetime.now()
        if self.service_name == "operations_data":
            for user in self.users:
                number_start += 1
                if user.is_paid:
                    number_finish += 1
            return [number_start, number_finish]
        for user in self.users:
            number_start += 1
            if self.service_name in self.services_with_finished and user.finish_service:
                number_finish += 1
        return [number_start, number_finish]