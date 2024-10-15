# Developed by: MasterkinG32
# Date: 2024
# Github: https://github.com/masterking32
# Telegram: https://t.me/MasterCryptoFarmBot
import random
import sys
import os

from utilities.utilities import getConfig
from .core.HttpRequest import HttpRequest
from .core.User import User
from .core.Auth import Auth
from .core.Game import Game

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
                    if getConfig("select_race", 3) == 3
                    else getConfig("select_race", 1)
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

        except Exception as e:
            self.log.error(f"<r>⭕ <c>{self.account_name}</c> failed to farm!</r>")
            self.log.error(f"<r>{str(e)}</r>")
            return
