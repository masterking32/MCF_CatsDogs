# Developed by: MasterkinG32
# Date: 2024
# Github: https://github.com/masterking32
# Telegram: https://t.me/MasterCryptoFarmBot


import json


class Game:
    def __init__(self, log, httpRequest, account_name):
        self.log = log
        self.http = httpRequest
        self.account_name = account_name

    def claim(self):
        try:
            response = self.http.post(
                url="/game/claim",
            )

            if response is None:
                self.log.error(f"<r>⭕ <c>{self.account_name}</c> failed to claim!</r>")
                return None

            return response
        except Exception as e:
            self.log.error(f"<r>⭕ <c>{self.account_name}</c> failed to claim!</r>")
            # self.log.error(f"<r>{e}</r>")
            return

    def current(self):
        try:
            response = self.http.get(
                url="/game/current",
            )

            if response is None:
                self.log.error(
                    f"<r>⭕ <c>{self.account_name}</c> failed to get user info!</r>"
                )
                return None

            return response
        except Exception as e:
            self.log.error(
                f"<r>⭕ <c>{self.account_name}</c> failed to get user info!</r>"
            )
            # self.log.error(f"<r>{e}</r>")
            return None

    def register(self, race):
        try:
            response = self.http.post(
                url="/auth/register",
                data=json.dumps({"race": race}),
            )

            if response is None:
                self.log.error(
                    f"<r>⭕ <c>{self.account_name}</c> failed to register!</r>"
                )
                return None

            return response
        except Exception as e:
            self.log.error(f"<r>⭕ <c>{self.account_name}</c> failed to register!</r>")
            # self.log.error(f"<r>{e}</r>")
            return None
