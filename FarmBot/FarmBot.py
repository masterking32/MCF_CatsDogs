# Developed by: MasterkinG32
# Date: 2024
# Github: https://github.com/masterking32
# Telegram: https://t.me/MasterCryptoFarmBot
import random
import sys
import os
import time

from utilities.utilities import getConfig
from .core.HttpRequest import HttpRequest
from .core.User import User
from .core.Auth import Auth
from .core.Game import Game
from .core.Tasks import Tasks


from dateutil import parser

MasterCryptoFarmBot_Dir = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__ + "/../../"))
)
sys.path.append(MasterCryptoFarmBot_Dir)


class FarmBot:
    def __init__(
        self,
        log,
        bot_globals,
        account_name,
        web_app_query,
        proxy=None,
        user_agent=None,
        isPyrogram=False,
        tgAccount=None,
    ):
        self.log = log
        self.bot_globals = bot_globals
        self.account_name = account_name
        self.web_app_query = web_app_query
        self.proxy = proxy
        self.user_agent = user_agent
        self.isPyrogram = isPyrogram
        self.tgAccount = tgAccount

    async def run(self):
        try:
            self.log.info(
                f"<cyan>{self.account_name}</cyan><g> | 🤖 Start farming Cats&Dogs ...</g>"
            )

            self.log.info(
                "Module Required update. Please wait for new version to be released."
            )
            return
            self.http = HttpRequest(
                log=self.log,
                proxy=self.proxy,
                user_agent=self.user_agent,
                tgWebData=self.web_app_query,
                account_name=self.account_name,
            )

            self.http.authToken = self.web_app_query

            user = User(
                log=self.log,
                httpRequest=self.http,
                account_name=self.account_name,
                tgWebData=self.web_app_query,
            )

            user_info = user.info()

            if user_info is None:
                self.log.error(
                    f"<r>⭕ <c>{self.account_name}</c> failed to get user info!</r>"
                )
                return

            user_id = user_info.get("id")
            race = user_info.get("race", 0)

            auth = Auth(
                log=self.log,
                httpRequest=self.http,
                account_name=self.account_name,
            )

            auth_info = auth.days()
            self.log.info(
                f"<g>📅 The age of account <c>{self.account_name}</c> is <c>{auth_info.get('days')}</c> days</g>"
            )

            if race == 0:
                race = (
                    random.choice([1, 2])
                    if int(getConfig("select_race", "3")) == 3
                    else int(getConfig("select_race", "1"))
                )

                register = auth.register(race)
                if register is None:
                    self.log.error(
                        f"<r>⭕ <c>{self.account_name}</c> failed to register!</r>"
                    )
                    return

                r_name = "Cats" if race == 1 else "Dogs"
                self.log.info(
                    f"<g>🔥 Account <c>{self.account_name}</c> was successfully registered as <c>{r_name}</c>!</g>"
                )

                user_info = register

            game = Game(
                log=self.log,
                httpRequest=self.http,
                account_name=self.account_name,
            )

            game_info = game.current()
            if game_info is None:
                self.log.error(
                    f"<r>⭕ <c>{self.account_name}</c> failed to get game info!</r>"
                )
                return

            cats = game_info.get("cats", 0)
            dogs = game_info.get("dogs", 0)
            rewards_cats = game_info.get("rewards", {}).get("cats", 0)
            rewards_dogs = game_info.get("rewards", {}).get("dogs", 0)

            if race == 1:
                self.log.info(
                    f"<g>🐱 Account <c>{self.account_name}</c> has <c>{cats}</c> Cats and <c>{rewards_cats}</c> rewards</g>"
                )
            else:
                self.log.info(
                    f"<g>🐶 Account <c>{self.account_name}</c> has <c>{dogs}</c> Dogs and <c>{rewards_dogs}</c> rewards</g>"
                )

            balance = user.balance()
            if balance is None:
                self.log.error(
                    f"<r>⭕ <c>{self.account_name}</c> failed to get user balance!</r>"
                )
                return

            account_balance = 0
            for coin in balance:
                account_balance += balance[coin]

            self.log.info(
                f"<g>💰 Account <c>{self.account_name}</c> has a balance of <c>{account_balance}</c> coins</g>"
            )

            license_key = self.bot_globals.get("license", None)
            tasks = Tasks(
                log=self.log,
                httpRequest=self.http,
                account_name=self.account_name,
                license_key=license_key,
                tgAccount=self.tgAccount,
                bot_globals=self.bot_globals,
            )

            self.log.info(
                f"<g>📋 Account <c>{self.account_name}</c> is fetching tasks list...</g>"
            )
            tasks_list = tasks.list()

            claimed_at = user_info.get("claimed_at", None)
            if claimed_at is None:
                claimed_at = "2020-10-15T20:40:25.780995Z"

            claim_timestamp = int(parser.isoparse(claimed_at).timestamp())
            current_time = int(time.time())

            if current_time - claim_timestamp > 28805:
                self.log.info(
                    f"<g>🎁 Account <c>{self.account_name}</c> can claim a reward!</g>"
                )
                time.sleep(random.randint(5, 8))
                claim = game.claim()
                if claim is not None:
                    self.log.info(
                        f"<g>🎁 Account <c>{self.account_name}</c> has successfully claimed a reward!</g>"
                    )

                    balance = user.balance()
                    current = game.current()

                    if balance is not None and current is not None:
                        account_balance = 0
                        for coin in balance:
                            account_balance += balance[coin]

                        self.log.info(
                            f"<g>💰 Account <c>{self.account_name}</c> has a balance of <c>{account_balance}</c> coins</g>"
                        )

                        cats = current.get("cats", 0)
                        dogs = current.get("dogs", 0)
                        rewards_cats = current.get("rewards", {}).get("cats", 0)
                        rewards_dogs = current.get("rewards", {}).get("dogs", 0)

            if getConfig("auto_finish_tasks", True):
                self.log.info(
                    f"<g>📋 Account <c>{self.account_name}</c> is starting to check tasks...</g>"
                )

                await tasks.check_tasks()

                balance = user.balance()
                current = game.current()

                if balance is not None and current is not None:
                    account_balance = 0
                    for coin in balance:
                        account_balance += balance[coin]

                    self.log.info(
                        f"<g>💰 Account <c>{self.account_name}</c> has a balance of <c>{account_balance}</c> coins</g>"
                    )

                    cats = current.get("cats", 0)
                    dogs = current.get("dogs", 0)
                    rewards_cats = current.get("rewards", {}).get("cats", 0)
                    rewards_dogs = current.get("rewards", {}).get("dogs", 0)

            self.log.info(
                f"<g>🔚 Account <c>{self.account_name}</c> has finished farming Cats&Dogs!</g>"
            )

        except Exception as e:
            self.log.error(f"<r>⭕ <c>{self.account_name}</c> failed to farm!</r>")
            self.log.error(f"<r>{str(e)}</r>")
            return
        finally:
            delay_between_accounts = getConfig("delay_between_accounts", 60)
            random_sleep = random.randint(0, 20) + delay_between_accounts
            self.log.info(
                f"<g>⌛ Farming for <c>{self.account_name}</c> completed. Waiting for <c>{random_sleep}</c> seconds before running the next account...</g>"
            )
            time.sleep(random_sleep)
