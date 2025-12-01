"""
Example Page Object: Login Page

This is a sample implementation of a Page Object for a login page.
It demonstrates best practices for creating page objects using the BasePage class.

Usage:
    from src.pages.login_page import LoginPage
    
    login_page = LoginPage(session)
    login_page.navigate()
    login_page.login("username", "password")
    assert login_page.is_logged_in()
"""

from selenium.webdriver.common.by import By
from .base_page import BasePage
from ..core.ports import Locator


class LoginPage(BasePage):
    """
    Page Object for a typical login page.
    
    This class encapsulates all interactions with the login page,
    including locators, actions, and verification methods.
    """
    
    def __init__(self, session, base_url: str = "https://example.com"):
        """
        Initialize the LoginPage.
        
        Args:
            session (SeleniumSession): The Selenium session
            base_url (str): The base URL of the application
        """
        super().__init__(session)
        self.url = f"{base_url}/login"
    
    # ==================== Locators ====================
    # Define all page element locators as class-level constants
    
    USERNAME_INPUT = Locator(By.ID, "username")
    PASSWORD_INPUT = Locator(By.ID, "password")
    LOGIN_BUTTON = Locator(By.CSS_SELECTOR, "button[type='submit']")
    ERROR_MESSAGE = Locator(By.CSS_SELECTOR, ".error-message")
    FORGOT_PASSWORD_LINK = Locator(By.LINK_TEXT, "Forgot Password?")
    REMEMBER_ME_CHECKBOX = Locator(By.ID, "remember-me")
    SUCCESS_MESSAGE = Locator(By.CSS_SELECTOR, ".success-message")
    LOGOUT_BUTTON = Locator(By.ID, "logout")
    
    # Alternative locators (if page has multiple login forms)
    ALTERNATIVE_USERNAME = Locator(By.NAME, "user")
    ALTERNATIVE_PASSWORD = Locator(By.NAME, "pass")
    
    # ==================== Page Actions ====================
    
    def enter_username(self, username: str) -> None:
        """
        Enter username into the username field.
        
        Args:
            username (str): The username to enter
        """
        self.clear_and_type(self.USERNAME_INPUT, username)
    
    def enter_password(self, password: str) -> None:
        """
        Enter password into the password field.
        
        Args:
            password (str): The password to enter
        """
        self.clear_and_type(self.PASSWORD_INPUT, password)
    
    def click_login_button(self) -> None:
        """Click the login button."""
        self.click(self.LOGIN_BUTTON)
    
    def click_forgot_password(self) -> None:
        """Click the 'Forgot Password?' link."""
        self.click(self.FORGOT_PASSWORD_LINK)
    
    def check_remember_me(self) -> None:
        """Check the 'Remember Me' checkbox if not already checked."""
        checkbox = self.find_element(self.REMEMBER_ME_CHECKBOX)
        if checkbox and not checkbox.is_selected():
            self.click(self.REMEMBER_ME_CHECKBOX)
    
    def uncheck_remember_me(self) -> None:
        """Uncheck the 'Remember Me' checkbox if checked."""
        checkbox = self.find_element(self.REMEMBER_ME_CHECKBOX)
        if checkbox and checkbox.is_selected():
            self.click(self.REMEMBER_ME_CHECKBOX)
    
    # ==================== Composite Actions ====================
    
    def login(self, username: str, password: str, remember_me: bool = False) -> None:
        """
        Perform a complete login action.
        
        This is a composite action that combines multiple steps:
        1. Enter username
        2. Enter password
        3. Optionally check 'Remember Me'
        4. Click login button
        
        Args:
            username (str): The username to login with
            password (str): The password to login with
            remember_me (bool): Whether to check 'Remember Me' checkbox
        """
        self.enter_username(username)
        self.enter_password(password)
        
        if remember_me:
            self.check_remember_me()
        
        self.click_login_button()
    
    def logout(self) -> None:
        """Perform logout action."""
        if self.is_logged_in():
            self.click(self.LOGOUT_BUTTON)
    
    # ==================== Verification Methods ====================
    
    def is_login_button_visible(self) -> bool:
        """
        Check if the login button is visible.
        
        Returns:
            bool: True if login button is visible, False otherwise
        """
        return self.is_visible(self.LOGIN_BUTTON)
    
    def is_error_displayed(self) -> bool:
        """
        Check if an error message is displayed.
        
        Returns:
            bool: True if error message is displayed, False otherwise
        """
        return self.is_visible(self.ERROR_MESSAGE, timeout=5)
    
    def get_error_message(self) -> str:
        """
        Get the error message text.
        
        Returns:
            str: The error message text, or empty string if not found
        """
        return self.get_text(self.ERROR_MESSAGE)
    
    def is_logged_in(self) -> bool:
        """
        Check if user is successfully logged in.
        
        This method checks for the presence of elements that only appear
        when logged in (e.g., logout button, success message).
        
        Returns:
            bool: True if user is logged in, False otherwise
        """
        # Option 1: Check for logout button
        # return self.is_present(self.LOGOUT_BUTTON, timeout=5)
        
        # Option 2: Check for success message
        # return self.is_visible(self.SUCCESS_MESSAGE, timeout=5)
        
        # Option 3: Check URL contains specific text
        return self.wait_for_url_to_contain("dashboard", timeout=10)
    
    def is_remember_me_checked(self) -> bool:
        """
        Check if 'Remember Me' checkbox is checked.
        
        Returns:
            bool: True if checkbox is checked, False otherwise
        """
        checkbox = self.find_element(self.REMEMBER_ME_CHECKBOX)
        return checkbox.is_selected() if checkbox else False
    
    # ==================== Page State Methods ====================
    
    def wait_for_page_load(self, timeout: int = 10) -> bool:
        """
        Wait for the login page to fully load.
        
        Args:
            timeout (int): Maximum wait time in seconds
            
        Returns:
            bool: True if page loaded successfully, False otherwise
        """
        return self.is_visible(self.LOGIN_BUTTON, timeout=timeout)
    
    def is_page_loaded(self) -> bool:
        """
        Check if the login page is fully loaded.
        
        Returns:
            bool: True if page is loaded, False otherwise
        """
        return (
            self.is_present(self.USERNAME_INPUT) and
            self.is_present(self.PASSWORD_INPUT) and
            self.is_present(self.LOGIN_BUTTON)
        )
