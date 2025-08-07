from typing import Any

from .driver_creator import DriverCreator
from ..utils.exceptions import BrowserInitializationError
from ..utils.logger import logger


class BrowserFactory:
    def __init__(self):
        self.driver_map = {
            "chrome": DriverCreator.create_chrome_driver,
            "firefox": DriverCreator.create_firefox_driver,
            "remote": DriverCreator.create_remote_driver,
        }

    def create_browser(self, browser_type: str, options: Any, connection: dict):
        browser_type = browser_type.lower()
        creator = self.driver_map.get(browser_type)
        if not creator:
            raise BrowserInitializationError(browser_type)
        
        logger.info(f'request to create driver with type=({browser_type}), connection=({connection})')
        return creator(options, connection)