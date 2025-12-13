# --- infra/browser_config_builder.py ---
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.edge.options import Options as EdgeOptions
import os
import platform

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
        """Set browser profile with Windows-specific handling.
        
        On Windows:
        - Uses absolute paths to avoid path resolution issues
        - Adds additional stability flags to prevent crashes
        - Creates separate profile directory to avoid conflicts
        
        Args:
            path: Profile directory path (relative or absolute)
        
        Returns:
            Self for method chaining
        """
        if self.browser_name in ['chrome', 'edge']:
            # Convert to absolute path for better reliability
            abs_path = os.path.abspath(path)
            
            # Create the profile directory
            os.makedirs(abs_path, exist_ok=True)
            
            # Windows-specific: Create a separate profile subdirectory
            # This prevents conflicts with existing Chrome profiles
            if platform.system() == 'Windows':
                profile_dir = os.path.join(abs_path, 'Profile')
                os.makedirs(profile_dir, exist_ok=True)
            
            self.options.add_argument(f'--user-data-dir={abs_path}')
            
            # Windows-specific stability flags
            if platform.system() == 'Windows':
                # Prevent crashes on Windows
                self.options.add_argument('--disable-dev-shm-usage')
                # Avoid GPU process crashes
                self.options.add_argument('--disable-software-rasterizer')
                # Prevent renderer crashes
                self.options.add_argument('--disable-features=VizDisplayCompositor')
                
        elif self.browser_name == 'firefox':
            abs_path = os.path.abspath(path)
            os.makedirs(abs_path, exist_ok=True)
            self.options.add_argument("-profile")
            self.options.add_argument(abs_path)
        else:
            raise ValueError(
                f"Profile configuration is only supported for Chrome, Edge, or Firefox browsers. "
                f"Current browser: {self.browser_name}"
            )
        return self

    def disable_blink_features(self, feature: str = "AutomationControlled"):
        """
        Disable specific Blink features (Chromium-based browsers only).
        
        Args:
            feature: The Blink feature to disable (default: "AutomationControlled")
        
        Returns:
            Self for method chaining
        
        Note:
            - Chrome/Edge: Disables the specified Blink feature
            - Firefox: No-op (not applicable)
        """
        if self.browser_name in ['chrome', 'edge']:
            self.options.add_argument(f'--disable-blink-features={feature}')
        # Firefox doesn't have Blink features, silently ignore
        return self

    def add_experimental_option(self, name: str, value):
        """
        Add experimental options (Chromium-based browsers only).
        
        Args:
            name: The experimental option name
            value: The option value
        
        Returns:
            Self for method chaining
        
        Note:
            - Chrome/Edge: Adds the experimental option
            - Firefox: No-op (not applicable)
        """
        if self.browser_name in ['chrome', 'edge']:
            if isinstance(self.options, (ChromeOptions, EdgeOptions)):
                self.options.add_experimental_option(name, value)
        # Firefox doesn't support experimental options, silently ignore
        return self

    def exclude_switches(self, switches: list):
        """
        Exclude Chrome switches from being used (Chromium-based browsers only).
        
        Args:
            switches: List of switches to exclude (e.g., ['enable-logging'])
        
        Returns:
            Self for method chaining
        
        Note:
            - Chrome/Edge: Excludes the specified switches
            - Firefox: No-op (not applicable)
        """
        if self.browser_name in ['chrome', 'edge']:
            if isinstance(self.options, (ChromeOptions, EdgeOptions)):
                self.options.add_experimental_option('excludeSwitches', switches)
        # Firefox doesn't support excludeSwitches, silently ignore
        return self

    def disable_automation_extension(self):
        """
        Disable the use of the automation extension (Chromium-based browsers only).
        
        Returns:
            Self for method chaining
        
        Note:
            - Chrome/Edge: Disables the automation extension
            - Firefox: No-op (not applicable)
        """
        if self.browser_name in ['chrome', 'edge']:
            if isinstance(self.options, (ChromeOptions, EdgeOptions)):
                self.options.add_experimental_option('useAutomationExtension', False)
        # Firefox doesn't support useAutomationExtension, silently ignore
        return self

    def build(self):
        return self.options