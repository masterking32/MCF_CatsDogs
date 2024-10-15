# Developed by: MasterkinG32
# Date: 2024
# Github: https://github.com/masterking32
# Telegram: https://t.me/MasterCryptoFarmBot


import json
import random
import time

from utilities.utilities import getConfig
from mcf_utils.api import API
from mcf_utils.tgAccount import tgAccount as TG


class Tasks:
    def __init__(
        self,
        log,
        httpRequest,
        account_name,
        license_key=None,
        tgAccount=None,
        bot_globals=None,
    ):
        self.log = log
        self.http = httpRequest
        self.account_name = account_name
        self.tasks = None
        self.license_key = license_key
        self.tgAccount = tgAccount
        self.bot_globals = bot_globals

    async def check_tasks(self, tasks_list=None):
        if self.tasks is None and tasks_list is None:
            return False

        tasks = self.tasks if tasks_list is None else tasks_list
        for task in tasks:
            try:
                if (
                    ("hidden" in task and task["hidden"] == True)
                    or ("transaction_id" in task and task["transaction_id"] is not None)
                    or (
                        "transaction_created_at" in task
                        and task["transaction_created_at"] is not None
                    )
                    or ("is_completed" in task and task["is_completed"] == True)
                    or ("completed_at" in task and task["completed_at"] is not None)
                ):
                    continue

                task_id = task.get("id")
                task_title = task.get("title", "")

                if task["type"] in ["inst", "tik"]:
                    pass
                elif task["type"] in ["tg", "channel"]:
                    if self.tgAccount is None or not getConfig("join_channels", True):
                        continue

                    channel_url = task.get("link")
                    if channel_url is None or channel_url == "":
                        continue

                    if "+" not in channel_url:
                        channel_url = (
                            channel_url.replace("https://t.me/", "")
                            .replace("@", "")
                            .replace("boost/", "")
                        )

                        channel_url = (
                            channel_url.split("/")[0]
                            if "/" in channel_url
                            else channel_url
                        )

                    self.log.info(
                        f"<g>📝 <c>{self.account_name}</c> | Attempting to join the <c>{channel_url}</c> channel to complete the <c>{task_title}</c> task</g>"
                    )

                    try:
                        await self.tgAccount.joinChat(channel_url)
                        time.sleep(random.randint(5, 10))
                    except Exception as e:
                        pass

                elif task["type"] in ["okx", "invite"]:
                    continue
                elif task["type"] == "folder":
                    if self.tgAccount is None or not getConfig("join_channels", True):
                        continue

                    if self.tgAccount is None or not getConfig("start_bots", True):
                        continue

                    sub_tasks = self.get_sub_tasks(task_id)
                    if sub_tasks is None:
                        continue

                    await self.check_tasks(sub_tasks)
                elif task["type"] == "twitter" or "t.me/" in task["link"]:
                    if "t.me/" not in task["link"]:
                        self.log.info(
                            f"<g>📝 <c>{self.account_name}</c> | Trying to complete <c>{task_title}</c> task</g>"
                        )

                        response = None
                        if tasks_list is not None:
                            response = self.claim_sub_task(task_id)
                        else:
                            response = self.claim(task_id)
                        time.sleep(random.randint(5, 10))
                        continue

                    if (
                        self.tgAccount is None
                        or not getConfig("start_bots", True)
                        or "+" in task["link"]
                        or "?" not in task["link"]
                    ):
                        continue

                    data = {
                        "task_type": "invite",
                        "task_data": task["link"],
                    }

                    api_response = self.get_api_data(data, license_key=self.license_key)
                    if (
                        api_response is None
                        or "status" not in api_response
                        or api_response["status"] != "success"
                    ):
                        continue

                    ref_link = api_response.get("referral")
                    bot_id = api_response.get("bot_id")

                    if ref_link is None or bot_id is None:
                        continue

                    self.log.info(
                        f"<g>🚀 Starting bot for task <c>{task_title}</c>...</g>"
                    )

                    try:
                        tg = TG(
                            bot_globals=self.bot_globals,
                            log=self.log,
                            accountName=self.account_name,
                            proxy=self.http.proxy,
                            BotID=bot_id,
                            ReferralToken=ref_link,
                            MuteBot=True,
                        )

                        await tg.getWebViewData()

                        self.log.info(f"<g>✅ Bot <c>{bot_id}</c> started!</g>")

                        time.sleep(random.randint(5, 10))
                    except Exception as e:
                        pass

                else:
                    continue

                self.log.info(
                    f"<g>📝 <c>{self.account_name}</c> | Trying to complete <c>{task_title}</c> task</g>"
                )

                response = None
                if tasks_list is not None:
                    response = self.claim_sub_task(task_id)
                else:
                    response = self.claim(task_id)
                if (
                    response is not None
                    and "status" in response
                    and response["status"] == "success"
                ):
                    self.log.info(
                        f"<g>🎉 <c>{self.account_name}</c> | Task <c>{task_title}</c> completed successfully</g>"
                    )
                else:
                    self.log.info(
                        f"<y>⭕ <c>{self.account_name}</c> | Failed to complete task <c>{task_title}</c></y>"
                    )

                time.sleep(random.randint(5, 10))
            except Exception as e:
                # self.log.error(f"<r>{e}</r>")
                continue
        return True

    def claim_sub_task(self, sub_task_id):
        try:
            response = self.http.post(
                url="/tasks/subtasks/claim",
                data=json.dumps({"subtask_id": sub_task_id}),
                display_errors=False,
            )

            if response is None:
                return None

            return response
        except Exception as e:
            # self.log.error(f"<r>{e}</r>")
            return None

    def get_sub_tasks(self, task_id):
        try:
            response = self.http.get(
                url=f"/tasks/{task_id}/subtasks",
            )

            if response is None:
                self.log.error(
                    f"<r>⭕ <c>{self.account_name}</c> failed to get subtasks!</r>"
                )
                return None

            return response
        except Exception as e:
            self.log.error(
                f"<r>⭕ <c>{self.account_name}</c> failed to get subtasks!</r>"
            )
            # self.log.error(f"<r>{e}</r>")
            return None

    def get_api_data(self, data, license_key):
        if license_key is None:
            return None

        apiObj = API(self.log)
        data["game_name"] = "cats_dogs"
        data["action"] = "get_task"
        response = apiObj.get_task_answer(license_key, data)
        time.sleep(3)
        if "error" in response:
            self.log.error(f"<y>⭕ API Error: {response['error']}</y>")
            return None
        elif "status" in response and response["status"] == "success":
            return response
        elif (
            "status" in response
            and response["status"] == "error"
            and "message" in response
        ):
            self.log.info(f"<y>🟡 {response['message']}</y>")
            return None
        else:
            self.log.error(
                f"<y>🟡 Unable to get task answer, please try again later</y>"
            )
            return None

    def claim(self, task_id):
        try:
            response = self.http.post(
                url="/tasks/claim",
                data=json.dumps({"task_id": task_id}),
                display_errors=False,
            )

            if response is None:
                # self.log.error(
                #     f"<r>⭕ <c>{self.account_name}</c> failed to claim task!</r>"
                # )
                return None

            return response
        except Exception as e:
            # self.log.error(
            #     f"<r>⭕ <c>{self.account_name}</c> failed to claim task!</r>"
            # )
            # self.log.error(f"<r>{e}</r>")
            return None

    def list(self):
        try:
            response = self.http.get(
                url="/tasks/list",
            )

            if response is None:
                self.log.error(
                    f"<r>⭕ <c>{self.account_name}</c> failed to get tasks list!</r>"
                )
                return None

            self.tasks = response
            return response
        except Exception as e:
            self.log.error(
                f"<r>⭕ <c>{self.account_name}</c> failed to get tasks list!</r>"
            )
            # self.log.error(f"<r>{e}</r>")
            return None
