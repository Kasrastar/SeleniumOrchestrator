import os
from typing import Any, Dict
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.common.exceptions import SessionNotCreatedException, WebDriverException
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions


from ..utils.exceptions import BrowserInitializationError, DriverNotFoundError, BrowserConfigError
from ..utils.logger import setup_logger

logger = setup_logger("DriverCreator")

class DriverCreator:
    @staticmethod
    def create_chrome_driver(options: ChromeOptions, connection: dict) -> webdriver.Chrome:
        try:
            binary_path = connection.get('binary_path', '')
            if not binary_path:
                logger.error("Chrome binary path is missing")
                raise BrowserInitializationError("chrome", "Chrome binary path is missing")
            if not os.path.exists(binary_path):
                logger.warning(f"ChromeDriver binary not found at {binary_path}")
                raise DriverNotFoundError("ChromeDriver", f"Binary not found at {binary_path}")
            driver = webdriver.Chrome(
                service=ChromeService(executable_path=binary_path),
                options=options
            )
            logger.info("Chrome driver created")
            return driver
        except SessionNotCreatedException as e:
            logger.error("Session creation failed", exc_info=True)
            raise BrowserInitializationError('chrome', str(e))
        except WebDriverException as e:
            logger.error("WebDriver exception", exc_info=True)
            raise BrowserInitializationError('chrome', f"Unexpected error: {e}")
        except Exception as e:
            logger.critical("Critical error", exc_info=True)
            raise BrowserInitializationError('chrome', f"Critical error: {e}")

    @staticmethod
    def create_firefox_driver(options: FirefoxOptions, connection: dict) -> webdriver.Firefox:
        try:
            binary_path = connection.get('binary_path', '')
            if not binary_path:
                logger.error("Firefox binary path is missing")
                raise BrowserInitializationError("firefox", "Firefox binary path is missing")
            if not os.path.exists(binary_path):
                logger.warning(f"GeckoDriver binary not found at {binary_path}")
                raise DriverNotFoundError("GeckoDriver", f"Binary not found at {binary_path}")

            driver = webdriver.Firefox(
                service=FirefoxService(executable_path=binary_path),
                options=options
            )
            
            if "--start-maximized" in options.arguments:
                driver.maximize_window()
            logger.info("Firefox driver created")
            return driver
        
        except SessionNotCreatedException as e:
            logger.error("Session creation failed", exc_info=True)
            raise BrowserInitializationError('firefox', str(e))
        except WebDriverException as e:
            # logger.error("WebDriver exception", exc_info=True)
            raise BrowserInitializationError('firefox', f"Unexpected error: {e}")
        except Exception as e:
            logger.critical("Critical error", exc_info=True)
            raise BrowserInitializationError('firefox', f"Critical error: {e}")

    @staticmethod
    def create_remote_driver(options: Any, connection: dict) -> webdriver.Remote:
        try:
            remote_url = connection.get('remote_url', '')
            if not remote_url:
                logger.error("Remote URL missing")
                raise BrowserConfigError("Remote URL required")
            driver = webdriver.Remote(command_executor=remote_url, options=options)
            logger.info("Remote driver created")
            return driver
        except WebDriverException as e:
            logger.error("WebDriver exception", exc_info=True)
            raise BrowserInitializationError('remote', f"Unexpected error: {e}")
        except Exception as e:
            logger.critical("Critical error", exc_info=True)
            raise BrowserInitializationError('remote', f"Critical error: {e}")

