import os
import asyncio
import signal

import aiohttp

from common.logger import Logger
from common.exceptions import MissingEnvironmentVariables


class App:
    def __init__(self,
            logger_name: str = __name__,
            logger_level: str = "info",
            envvars: list = None,
            poll_interval_seconds: int = 60,
            run_now=True,
            *args,
            **kwargs):

        self._run_now = run_now
        Logger(name=logger_name, level=logger_level)
        self.logger = Logger.get_logger(logger_name)
        self._envvars = dict()
        self.poll_interval_seconds = poll_interval_seconds

        if envvars is not None:
            missing = self.check_environment_variables(envvars)
            if len(missing) > 0:
                raise MissingEnvironmentVariables(
                    f"Missing environment variables: {missing}"
                )

        if self._run_now:
            self.start()

    def start(self):
        loop = asyncio.get_event_loop()
        try:
            loop.run_until_complete(self._run())
        except:
            self.logger.exception("Something went wrong.")
            self.exit()
            loop.close()

    async def run(self):
        raise NotImplementedError

    @classmethod
    def create(cls,
            logger_name: str = __name__,
            envvars: list = None,
            poll_interval_seconds: int = 60,
            *args,
            **kwargs):
        self = cls(
            logger_name,
            envvars=envvars,
            poll_interval_seconds=poll_interval_seconds,
            *args,
            **kwargs
        )
        return self

    async def _run(self):
        while True:
            await self.run()
            await asyncio.sleep(self.poll_interval_seconds)

    def check_environment_variables(self, envvars: list) -> list:
        missing = []
        for key in envvars:
            try:
                value = os.environ[key]
                self.envvars[key] = value
            except KeyError:
                missing.append(key)
        return missing

    @property
    def envvars(self):
        return self._envvars

    async def exit(self):
        raise NotImplementedError

