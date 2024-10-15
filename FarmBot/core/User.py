# Developed by: MasterkinG32
# Date: 2024
# Github: https://github.com/masterking32
# Telegram: https://t.me/MasterCryptoFarmBot


class User:
    def __init__(self, log, httpRequest, account_name, tgWebData):
        self.log = log
        self.http = httpRequest
        self.account_name = account_name
        self.tgWebData = tgWebData

    def info(self):
        try:
            response = self.http.get(
                url="/user/info",
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

    def balance(self):
        try:
            response = self.http.get(
                url="/user/balance",
            )

            if response is None:
                self.log.error(
                    f"<r>⭕ <c>{self.account_name}</c> failed to get user balance!</r>"
                )
                return None

            return response
        except Exception as e:
            self.log.error(
                f"<r>⭕ <c>{self.account_name}</c> failed to get user balance!</r>"
            )
            # self.log.error(f"<r>{e}</r>")
            return None
