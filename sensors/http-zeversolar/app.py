import aiohttp

from common.app import App

from zevercloud import ZeverCloud


class HttpZeversolar(App):
    async def run(self):
        async with aiohttp.ClientSession() as client:
            zc = ZeverCloud(
                self.envvars["API_KEY"],
                self.envvars["APP_KEY"],
                self.envvars["APP_SECRET"],
            )
            overview = zc.overview

            self.logger.info(f"Overview: {overview}")

            payload = {
                "state": overview["yield"]["today"],
                "attributes": {
                    "unit_of_measurement": "kWh",
                    "friendly_name": "Solar Yield Today",
                    "power": f'{overview["power"]} kW',
                },
            }
            headers = {
                "Authorization": f"Bearer {self.envvars['HA_API_KEY']}",
                "Content-Type": "application/json",
            }
            resp = await client.post(
                f"{self.envvars['HA_API_URL']}/states/sensor.zevercloud",
                json=payload,
                headers=headers
            )
            text = await resp.text()

            self.logger.info(f"HA API response: status={resp.status}\n{text}")

            resp.raise_for_status()


if __name__ == "__main__":
    sensor = HttpZeversolar.create(
        logger_name="HttpZeversolar",
        envvars=[
            "API_KEY",
            "APP_KEY",
            "APP_SECRET",
            "HA_API_KEY",
            "HA_API_URL",
        ]
    )