from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.common.exceptions import SessionNotCreatedException

from .browser_config_builder import BrowserConfigBuilder


class DriverCreator:
    @staticmethod
    def create_chrome_driver(options: BrowserConfigBuilder, connection: dict) -> webdriver.Chrome:
        try:
            binary_path = connection.get('binary_path', '')
            if not binary_path:
                ...  # raise error
            driver = webdriver.Chrome(
                service=ChromeService(
                    executable_path=binary_path
                ),
                options=options  # noqa
            )

            return driver
        except SessionNotCreatedException:
            raise

    #
    # @staticmethod
    # def create_firefox_driver(options: dict) -> webdriver.Firefox:
    #     firefox_options = FirefoxOptions()
    #     DriverCreator._set_browser_options(firefox_options, options)
    #     firefox_service = FirefoxService(GeckoDriverManager().install())
    #     return webdriver.Firefox(service=firefox_service, options=firefox_options)
    #
    # @staticmethod
    # def create_edge_driver(options: dict) -> webdriver.Edge:
    #     edge_options = EdgeOptions()
    #     DriverCreator._set_browser_options(edge_options, options)
    #     edge_service = EdgeService(EdgeDriverManager().install())
    #     return webdriver.Edge(service=edge_service, options=edge_options)

    @staticmethod
    def create_remote_driver(options, connection) -> webdriver.Remote:
        remote_url = connection.get('remote_url')
        return webdriver.Remote(command_executor=remote_url, options=options)
    

