from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.common.exceptions import (
    SessionNotCreatedException,
    WebDriverException,
)
import os

from .browser_config_builder import BrowserConfigBuilder
from ...utils.exceptions import (
    BrowserInitializationError,
    DriverNotFoundError,
    BrowserConfigError,
)
from ...utils.logger import setup_logger

logger = setup_logger("DriverCreator")

class DriverCreator:
    @staticmethod
    def create_chrome_driver(options: BrowserConfigBuilder, connection: dict) -> webdriver.Chrome:
        try:
            binary_path = connection.get('binary_path', '')
            if not binary_path:
                logger.error("Chrome binary path is missing")
                raise BrowserInitializationError("chrome", "Chrome binary path is missing")

            if not os.path.exists(binary_path):
                logger.warning(f"ChromeDriver binary not found at {binary_path}. Attempting to download...")
                # Placeholder for auto-downloading ChromeDriver logic
                raise DriverNotFoundError("ChromeDriver", f"Binary not found at {binary_path}")

            driver = webdriver.Chrome(
                service=ChromeService(executable_path=binary_path),
                options=options  # noqa
            )
            logger.info("Chrome driver successfully created")
            return driver

        except SessionNotCreatedException as e:
            logger.error("Chrome driver session could not be created. Check version compatibility", exc_info=True)
            raise BrowserInitializationError('chrome', str(e))
        except WebDriverException as e:
            logger.error("Unexpected WebDriver exception occurred during Chrome driver initialization", exc_info=True)
            raise BrowserInitializationError('chrome', f"Unexpected error: {str(e)}")
        except Exception as e:
            logger.critical("Critical error during Chrome driver initialization", exc_info=True)
            raise BrowserInitializationError('chrome', f"Critical error: {str(e)}")

    @staticmethod
    def create_firefox_driver(options: BrowserConfigBuilder, connection: dict) -> webdriver.Firefox:
        try:
            binary_path = connection.get('binary_path', '')
            if not binary_path:
                logger.error("Firefox binary path is missing")
                raise BrowserInitializationError("firefox", "Firefox binary path is missing")

            if not os.path.exists(binary_path):
                logger.warning(f"GeckoDriver binary not found at {binary_path}. Attempting to download...")
                # Placeholder for auto-downloading GeckoDriver logic
                raise DriverNotFoundError("GeckoDriver", f"Binary not found at {binary_path}")

            driver = webdriver.Firefox(
                service=FirefoxService(executable_path=binary_path),
                options=options
            )
            
            def is_arg_exists(options: BrowserConfigBuilder, arg: str):
                arg_list = options.arguments
                if arg in arg_list:
                    return True
                else:
                    return False

            
            if is_arg_exists(options, "--start-maximized"):
                driver.maximize_window()

            logger.info("Firefox driver successfully created")
            return driver

        except SessionNotCreatedException as e:
            logger.error("Firefox driver session could not be created. Check version compatibility", exc_info=True)
            raise BrowserInitializationError('firefox', str(e))
        except WebDriverException as e:
            logger.error("Unexpected WebDriver exception occurred during Firefox driver initialization", exc_info=True)
            raise BrowserInitializationError('firefox', f"Unexpected error: {str(e)}")
        except Exception as e:
            logger.critical("Critical error during Firefox driver initialization", exc_info=True)
            raise BrowserInitializationError('firefox', f"Critical error: {str(e)}")

    @staticmethod
    def create_remote_driver(options: BrowserConfigBuilder, connection: dict) -> webdriver.Remote:
        try:
            remote_url = connection.get('remote_url', '')
            if not remote_url:
                logger.error("Remote WebDriver URL is missing")
                raise BrowserConfigError("Remote WebDriver URL is required but not provided")

            driver = webdriver.Remote(command_executor=remote_url, options=options)
            logger.info("Remote driver successfully created")
            return driver

        except WebDriverException as e:
            logger.error("Unexpected WebDriver exception occurred during Remote driver initialization", exc_info=True)
            raise BrowserInitializationError('remote', f"Unexpected error: {str(e)}")
        except Exception as e:
            logger.critical("Critical error during Remote driver initialization", exc_info=True)
            raise BrowserInitializationError('remote', f"Critical error: {str(e)}")
