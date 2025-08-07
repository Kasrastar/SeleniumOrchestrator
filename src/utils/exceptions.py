from .logger import logger  

class SeleniumWrapperException(Exception):
    """Base class for all exceptions raised by the Selenium Wrapper."""

    def log_exception(self):
        """Logs the exception details."""
        logger.error(f"Exception occurred: {self}", exc_info=True)

class BrowserInitializationError(SeleniumWrapperException):
    """Raised when there is an error initializing the browser."""

    def __init__(self, browser_name: str, message: str = "Failed to initialize browser"):
        self.browser_name = browser_name
        self.message = f"{message}: {browser_name}"
        super().__init__(self.message)
        self.log_exception() 

class TabManagementError(SeleniumWrapperException):
    """Raised when there is an issue with managing tabs."""

    def __init__(self, tab_name: str, message: str = "Error managing the tab"):
        self.tab_name = tab_name
        self.message = f"{message}: {tab_name}"
        super().__init__(self.message)
        self.log_exception() 

class DriverNotFoundError(SeleniumWrapperException):
    """Raised when a WebDriver binary is not found."""

    def __init__(self, driver_name: str, message: str = "Driver not found"):
        self.driver_name = driver_name
        self.message = f"{message}: {driver_name}"
        super().__init__(self.message)
        self.log_exception() 

class BrowserConfigError(SeleniumWrapperException):
    """Raised when there is an error with the browser configuration."""

    def __init__(self, message: str = "Error in browser configuration"):
        self.message = message
        super().__init__(self.message)
        self.log_exception() 

class InvalidTabOperationError(SeleniumWrapperException):
    """Raised when there is an invalid operation on a tab."""

    def __init__(self, operation: str, message: str = "Invalid tab operation"):
        self.operation = operation
        self.message = f"{message}: {operation}"
        super().__init__(self.message)
        self.log_exception()  
