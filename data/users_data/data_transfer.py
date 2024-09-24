# import asyncio
# import datetime
# import json
#
# from bot import design_bot
# from db.repository import design_level_repository, users_repository, earnings_level_repository, mentor_repository, \
#     send_link_repository, ai_recommendations_repository
#
#
# class DataTransfer:
#     def __init__(self, filename: str | None = ""):
#         self.filename = filename
#
#     # async def transfer_users(self):
#     #     with open(f"ai_recommendations.json", "r", encoding="utf-8") as ai_recommendations:
#     #         self.ai_recommendations = list(json.load(ai_recommendations).get("users").keys())
#     #     with open(f"design_level.json", "r", encoding="utf-8") as design_level:
#     #         self.design_level = list(json.load(design_level).get("users").keys())
#     #     with open(f"earnings_level.json", "r", encoding="utf-8") as earnings_level:
#     #         self.earnings_level = list(json.load(earnings_level).get("users").keys())
#     #     with open(f"mentor_stat.json", "r", encoding="utf-8") as mentor_stat:
#     #         self.mentor_stat = list(json.load(mentor_stat).get("users").keys())
#     #     with open(f"send_link_data.json", "r", encoding="utf-8") as send_link_data:
#     #         self.send_link_data = list(json.load(send_link_data).get("users").keys())
#     #     users = list(set(self.design_level + self.ai_recommendations + self.earnings_level + self.mentor_stat + self.send_link_data))
#     #     for user in users:
#     #         print(user)
#     #         try:
#     #             link = '<a href="https://t.me/slashstudy">канале</a>'
#     #             message_to_user = await design_bot.send_message(chat_id=user, text="Здравствуй!\n\nСейчас наш бот"
#     #                                                                                " находится на сервисном обслуживании,"
#     #                                                                                " чтобы в скором времени обрадовать тебя"
#     #                                                                                " новыми фичами🚀\nОбязательно следи за"
#     #                                                                                f" новостями в нашем {link}")
#     #             user_base = await users_repository.get_user_by_user_id(user_id=int(user))
#     #             if not user_base:
#     #                 await users_repository.add_user(user_id=int(user), username=message_to_user.chat.username,
#     #                                                 donate=False, attempts=3)
#     #         except:
#     #             continue
#
#
#     async def transfer_design_level(self):
#         with open(f"{self.filename}.json", "r", encoding="utf-8") as items:
#             self.items = json.load(items).get("users")
#         for user in self.items.keys():
#             if (await users_repository.get_user_by_user_id(user_id=int(user)) and
#                     (await design_level_repository.get_user_by_user_id(user_id=int(user))) is None):
#                 user_id = int(user)
#                 last_start_date = datetime.datetime.utcfromtimestamp(self.items.get(user).get("start_time"))
#                 finish_service = self.items.get(user).get("complete_questions")
#                 await design_level_repository.add_design_level(user_id=user_id, last_date_start=last_start_date,
#                                                                finish_service=finish_service)
#
#     async def transfer_earnings_level(self):
#         with open(f"{self.filename}.json", "r", encoding="utf-8") as items:
#             self.items = json.load(items).get("users")
#         for user in self.items.keys():
#             if (await users_repository.get_user_by_user_id(user_id=int(user)) and
#                     (await earnings_level_repository.get_user_by_user_id(user_id=int(user))) is None):
#                 user_id = int(user)
#                 last_start_date = datetime.datetime.utcfromtimestamp(self.items.get(user).get("start_time"))
#                 finish_service = self.items.get(user).get("complete_questions")
#                 await earnings_level_repository.add_earnings_level(user_id=user_id, last_date_start=last_start_date,
#                                                                  finish_service=finish_service)
#
#     async def transfer_mentor(self):
#         with open(f"{self.filename}.json", "r", encoding="utf-8") as items:
#             self.items = json.load(items).get("users")
#         for user in self.items.keys():
#             if (await users_repository.get_user_by_user_id(user_id=int(user)) and
#                     (await mentor_repository.get_user_by_user_id(user_id=int(user))) is None):
#                 user_id = int(user)
#                 last_start_date = datetime.datetime.utcfromtimestamp(self.items.get(user).get("start_time"))
#                 await mentor_repository.add_mentor(user_id=user_id, last_date_start=last_start_date)
#
#     async def transfer_send_link(self):
#         with open(f"{self.filename}.json", "r", encoding="utf-8") as items:
#             self.items = json.load(items).get("users")
#         for user in self.items.keys():
#             if (await users_repository.get_user_by_user_id(user_id=int(user)) and
#                     (await send_link_repository.get_user_by_user_id(user_id=int(user))) is None):
#                 user_id = int(user)
#                 last_start_date = datetime.datetime.utcfromtimestamp(self.items.get(user).get("start_time"))
#                 await send_link_repository.add_send_link(user_id=user_id, last_date_start=last_start_date)
#
#     async def transfer_ai_recommendations(self):
#         with open(f"{self.filename}.json", "r", encoding="utf-8") as items:
#             self.items = json.load(items).get("users")
#         for user in self.items.keys():
#             if (await users_repository.get_user_by_user_id(user_id=int(user)) and
#                     (await ai_recommendations_repository.get_user_by_user_id(user_id=int(user))) is None):
#                 user_id = int(user)
#                 last_start_date = datetime.datetime.utcfromtimestamp(self.items.get(user).get("start_time"))
#                 await ai_recommendations_repository.add_ai_recommendation(user_id=user_id, last_date_start=last_start_date)
#
#
# async def main():
#     await DataTransfer("design_level").transfer_design_level()
#     await asyncio.sleep(10)
#     await DataTransfer("earnings_level").transfer_earnings_level()
#     await asyncio.sleep(10)
#     await DataTransfer("mentor_stat").transfer_mentor()
#     await asyncio.sleep(10)
#     await DataTransfer("send_link_data").transfer_send_link()
#     await asyncio.sleep(10)
#     await DataTransfer("ai_recommendations").transfer_ai_recommendations()
#
# if __name__ == "__main__":
#     asyncio.run(main())
#
