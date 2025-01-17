from src.orchestrator.driver_creator import DriverCreator
from src.orchestrator.browser_config_builder import BrowserConfigBuilder


class BrowserFactory:
    def __init__(self):
        # Mapping of browser names to corresponding creation methods in DriverCreator
        self.driver_map = {
            "chrome": DriverCreator.create_chrome_driver,
            # "firefox": DriverCreator.create_firefox_driver,
            # "edge": DriverCreator.create_edge_driver,
            # "remote": DriverCreator.create_remote_driver
        }

    def create_browser(self, browser_name: str, options: BrowserConfigBuilder, connection: dict):
        """
        Factory method to create browser instances.

        :param browser_name: Name of the browser ('chrome', 'firefox', 'edge', 'remote')
        :param options: Dictionary of browser-specific options.
        :return: A WebDriver instance.
        """
        browser_name = browser_name.lower()
        if browser_name in self.driver_map:
            return self.driver_map[browser_name](options, connection)
        else:
            raise ValueError(f"Unsupported browser: {browser_name}")
