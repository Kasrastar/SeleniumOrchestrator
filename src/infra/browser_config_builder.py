# --- infra/browser_config_builder.py ---
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.edge.options import Options as EdgeOptions
import os

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
        options_class = self.BROWSER_OPTIONS_MAP.get(self.browser_name)
        if not options_class:
            raise ValueError(f"Unsupported browser: {self.browser_name}")
        return options_class()

    def set_headless(self):
        self.options.add_argument("--headless")
        return self

    def set_fullscreen(self):
        self.options.add_argument("--start-maximized")
        return self

    def set_window_size(self, width: int, height: int):
        self.options.add_argument(f"--window-size={width},{height}")
        return self

    def disable_gpu(self):
        self.options.add_argument("--disable-gpu")
        return self

    def set_no_sandbox(self):
        self.options.add_argument("--no-sandbox")
        return self

    def disable_dev_shm_usage(self):
        self.options.add_argument("--disable-dev-shm-usage")
        return self

    def set_incognito(self):
        self.options.add_argument("--incognito")
        return self

    def set_user_agent(self, user_agent: str):
        self.options.add_argument(f"--user-agent={user_agent}")
        return self

    def set_browser_profile(self, path: str):
        if self.browser_name in ['chrome', 'edge']:
            self.options.add_argument(f'--user-data-dir={path}')
            os.makedirs(path, exist_ok=True)
        elif self.browser_name == 'firefox':
            os.makedirs(path, exist_ok=True)
            self.options.add_argument("-profile")
            self.options.add_argument(path)
        else:
            raise ValueError(
                f"Profile configuration is only supported for Chrome, Edge, or Firefox browsers. "
                f"Current browser: {self.browser_name}"
            )
        return self

    def build(self):
        return self.options