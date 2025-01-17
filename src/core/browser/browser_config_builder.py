from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.edge.options import Options as EdgeOptions


class BrowserConfigBuilder:
    BROWSER_OPTIONS_MAP = {
        "chrome": ChromeOptions,
        "firefox": FirefoxOptions,
        "edge": EdgeOptions
    }

    def __init__(self, browser_name: str):
        self.browser_name = browser_name.lower()
        self.options = self._initialize_options()

    def _initialize_options(self):
        """
        Initializes browser-specific options based on the chosen browser using a dictionary.
        """
        options_class = self.BROWSER_OPTIONS_MAP.get(self.browser_name)

        if not options_class:
            raise ValueError(f"Unsupported browser: {self.browser_name}")

        return options_class()

    def set_headless(self, headless: bool = True):
        """
        Sets the browser to headless mode or not.
        :param headless: Boolean indicating whether the browser should run in headless mode.
        :return: The builder instance for chaining.
        """
        if headless:
            self.options.add_argument("--headless")
        return self

    def set_window_size(self, width: int, height: int):
        """
        Sets the browser window size.
        :param width: The width of the browser window.
        :param height: The height of the browser window.
        :return: The builder instance for chaining.
        """
        self.options.add_argument(f"--window-size={width},{height}")
        return self

    def disable_gpu(self):
        """
        Disables GPU hardware acceleration.
        :return: The builder instance for chaining.
        """
        self.options.add_argument("--disable-gpu")
        return self

    def set_incognito(self):
        """
        Enables incognito mode.
        :return: The builder instance for chaining.
        """
        self.options.add_argument("--incognito")
        return self

    def set_user_agent(self, user_agent: str):
        """
        Sets a custom user agent.
        :param user_agent: The user-agent string to set.
        :return: The builder instance for chaining.
        """
        self.options.add_argument(f"user-agent={user_agent}")
        return self

    def set_user_data_dir(self, path: str):
        """
        Sets the user data directory for Chrome/Chromium-based browsers (like Chrome, Edge).
        :param path: The path to the user data directory.
        :return: The builder instance for chaining.
        """
        if self.browser_name in ['chrome', 'edge']:
            self.options.add_argument(f'--user-data-dir={path}')
        else:
            raise ValueError(
                f"User data directory is only supported for Chrome or Edge browsers. Current browser: {self.browser_name}"
            )
        return self

    def build(self):
        """
        Returns the configured options.
        :return: The browser-specific options.
        """
        return self.options
