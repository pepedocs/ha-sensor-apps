import aiohttp
import requests
import json

import selenium_async

from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary


from common.app import App


class HttpBelongGateway(App):
    def __init__(self,
            logger_name: str = __name__,
            envvars: list = None,
            poll_interval_seconds: int = 60,
            *args,
            **kwargs):
        super().__init__(logger_name=logger_name,
                         envvars=envvars,
                         run_now=False)
        self.firefox_options = Options()
        self.firefox_options.add_argument("--headless")
        self.firefox_options.binary = FirefoxBinary(self.envvars["FIREFOX_EXEC_PATH"])
        self.webdriver = webdriver.Firefox(
            executable_path=self.envvars["FIREFOX_GECKODRIVER_PATH"],
            options=self.firefox_options
        )
        self._has_logged_in = False
        self.start()

    def process(self, driver):
        if not self._has_logged_in:
            self.webdriver.get(
                f"http://{self.envvars['BELONG_GATEWAY_IPADDR']}/0.1/gui/#/login/")

            self.logger.info("Waiting for password field.")

            input = WebDriverWait(self.webdriver, 60).until(
                EC.element_to_be_clickable(
                    (By.ID, "password")
                    )
                )
            input.send_keys(self.envvars["BELONG_GATEWAY_PASSWORD"])
            input.send_keys(Keys.RETURN)
            self._has_logged_in = True

            self.logger.info("Waiting for span'.")

        span = WebDriverWait(self.webdriver, 60).until(
            EC.element_to_be_clickable(
                (By.XPATH, '//*[@id="page-content"]/div/div[3]/div[1]/div[1]/span')
                )
            )

        state = "offline"
        online_str = ("your broadband service is working normally. "
                      "you are connected and online.")
        if online_str in span.text.lower():
            state = "online"

        payload = {
            "state": state,
            "attributes": {
                    "friendly_name": "Belong Gateway",
                },
            }
        headers = {
            "Authorization": f"Bearer {self.envvars['HA_API_KEY']}",
            "Content-Type": "application/json",
        }
        resp = requests.post(
            f"{self.envvars['HA_API_URL']}/states/sensor.belonggatewayfast4353",
            data=json.dumps(payload),
            headers=headers
        )
        text = resp.text

        self.logger.info(f"HA API response: status={resp.status_code}\n{text}")

        resp.raise_for_status()

    async def run(self):
        await selenium_async.run_sync(self.process)

    def exit(self):
        self.webdriver.quit()

if __name__ == "__main__":
    sensor = HttpBelongGateway.create(
        "HttpBelongGateway",
        envvars = [
            "BELONG_GATEWAY_USERNAME",
            "BELONG_GATEWAY_PASSWORD",
            "BELONG_GATEWAY_IPADDR",
            "FIREFOX_EXEC_PATH",
            "FIREFOX_GECKODRIVER_PATH",
            "HA_API_KEY",
            "HA_API_URL",
        ]
    )
