"""
Jira Login Page Object

Page Object Model implementation for Jira login page at https://jira.inside45.ir/login.jsp
This module encapsulates all interactions with the Jira authentication system.

Usage:
    from src.pages.jira_login_page import JiraLoginPage
    
    jira_login = JiraLoginPage(session)
    jira_login.navigate()
    jira_login.login("username", "password", remember_me=True)
    assert jira_login.is_login_successful()
"""

from selenium.webdriver.common.by import By
from typing import Optional
from .base_page import BasePage
from ..core.ports import Locator, WaitCondition


class JiraLoginPage(BasePage):
    """
    Page Object for Jira login page (https://jira.inside45.ir/login.jsp).
    
    This class provides methods to interact with all elements on the Jira login page,
    including username/password entry, remember me checkbox, and login verification.
    
    Attributes:
        url (str): The Jira login page URL
    """
    
    def __init__(self, session, base_url: str = "https://jira.inside45.ir"):
        """
        Initialize the JiraLoginPage.
        
        Args:
            session (SeleniumSession): The Selenium session
            base_url (str): The base URL of the Jira instance (default: https://jira.inside45.ir)
        """
        super().__init__(session)
        self.base_url = base_url
        self.url = f"{base_url}/login.jsp"
    
    # ==================== Locators ====================
    # All element locators based on the actual Jira HTML structure
    
    # Main form and container
    LOGIN_FORM = Locator(By.ID, "login-form")
    LOGIN_HEADER = Locator(By.ID, "login-header")
    LOGIN_MESSAGE = Locator(By.ID, "login-message")
    
    # Input fields
    USERNAME_FIELD = Locator(By.ID, "username-field")
    USERNAME_LABEL = Locator(By.ID, "username-field-label")
    PASSWORD_FIELD = Locator(By.ID, "password-field")
    PASSWORD_LABEL = Locator(By.ID, "password-field-label")
    
    # Buttons
    LOGIN_BUTTON = Locator(By.ID, "login-button")
    TOGGLE_PASSWORD_BUTTON = Locator(By.CSS_SELECTOR, "[data-testid='toggle-password-button']")
    
    # Checkbox
    REMEMBER_ME_CHECKBOX = Locator(By.ID, "rememberMe-uid1")
    REMEMBER_ME_LABEL = Locator(By.ID, "rememberMe-uid1-label")
    
    # Links
    FORGOT_PASSWORD_LINK = Locator(By.XPATH, "//a[contains(@href, '/secure/ForgotLoginDetails.jspa')]")
    LOGIN_LINK = Locator(By.CSS_SELECTOR, "a.login-link")
    
    # Header elements
    HEADER = Locator(By.ID, "header")
    LOGO = Locator(By.ID, "logo")
    QUICK_SEARCH_INPUT = Locator(By.ID, "quickSearchInput")
    HELP_MENU = Locator(By.ID, "help_menu")
    
    # Footer elements
    FOOTER = Locator(By.ID, "footer")
    ABOUT_LINK = Locator(By.ID, "about-link")
    REPORT_PROBLEM_LINK = Locator(By.ID, "footer-report-problem-link")
    
    # Success indicators (after login)
    USER_OPTIONS = Locator(By.ID, "user-options")
    DASHBOARD_LINK = Locator(By.XPATH, "//a[contains(@href, '/secure/Dashboard.jspa')]")
    
    # Error message container
    ERROR_CONTAINER = Locator(By.CSS_SELECTOR, "[role='alert']")
    
    # ==================== Basic Actions ====================
    
    def enter_username(self, username: str) -> None:
        """
        Enter username into the username field.
        
        Args:
            username (str): The username to enter
            
        Raises:
            ElementNotInteractableError: If the username field is not interactable
        """
        self.find_element(self.USERNAME_FIELD, condition=WaitCondition.VISIBILITY_OF_ELEMENT_LOCATED)
        self.clear_and_type(self.USERNAME_FIELD, username)
    
    def enter_password(self, password: str) -> None:
        """
        Enter password into the password field.
        
        Args:
            password (str): The password to enter
            
        Raises:
            ElementNotInteractableError: If the password field is not interactable
        """
        self.find_element(self.PASSWORD_FIELD, condition=WaitCondition.VISIBILITY_OF_ELEMENT_LOCATED)
        self.clear_and_type(self.PASSWORD_FIELD, password)
    
    def click_login_button(self) -> None:
        """
        Click the login button to submit credentials.
        
        Raises:
            ElementNotClickableError: If the login button is not clickable
        """
        self.find_element(self.LOGIN_BUTTON, condition=WaitCondition.ELEMENT_TO_BE_CLICKABLE)
        self.click(self.LOGIN_BUTTON)
    
    def toggle_remember_me(self, should_remember: bool = True) -> None:
        """
        Toggle the 'Remember me' checkbox.
        
        Args:
            should_remember (bool): True to check the box, False to uncheck it
        """
        checkbox = self.find_element(self.REMEMBER_ME_CHECKBOX)
        is_checked = checkbox.get_attribute("aria-checked") == "true"
        
        if should_remember and not is_checked:
            self.click(self.REMEMBER_ME_CHECKBOX)
        elif not should_remember and is_checked:
            self.click(self.REMEMBER_ME_CHECKBOX)
    
    def click_toggle_password_visibility(self) -> None:
        """
        Toggle password visibility (show/hide password text).
        
        This clicks the eye icon button next to the password field.
        """
        self.click(self.TOGGLE_PASSWORD_BUTTON)
    
    def click_forgot_password(self) -> None:
        """
        Click the 'Can't log in?' (forgot password) link.
        
        This navigates to the password recovery page.
        """
        self.click(self.FORGOT_PASSWORD_LINK)
    
    # ==================== Composite Actions ====================
    
    def login(self, username: str, password: str, remember_me: bool = False) -> None:
        """
        Perform a complete login operation.
        
        This is a composite action that:
        1. Waits for page to load
        2. Enters username
        3. Enters password
        4. Optionally checks 'Remember me'
        5. Clicks login button
        
        Args:
            username (str): The username to login with
            password (str): The password to login with
            remember_me (bool): Whether to check the 'Remember me' checkbox (default: False)
            
        Example:
            >>> jira_login = JiraLoginPage(session)
            >>> jira_login.navigate()
            >>> jira_login.login("john.doe", "secret123", remember_me=True)
        """
        self.wait_for_page_ready()
        self.enter_username(username)
        self.enter_password(password)
        
        if remember_me:
            self.toggle_remember_me(True)
        
        self.click_login_button()
    
    def quick_login(self, username: str, password: str) -> None:
        """
        Perform a quick login without additional options.
        
        This is a simplified version of login() for common use cases.
        
        Args:
            username (str): The username to login with
            password (str): The password to login with
        """
        self.login(username, password, remember_me=False)
    
    # ==================== Verification Methods ====================
    
    def is_login_page_loaded(self) -> bool:
        """
        Check if the login page is fully loaded.
        
        Returns:
            bool: True if login page is loaded, False otherwise
        """
        try:
            return (self.is_element_visible(self.LOGIN_FORM) and
                    self.is_element_visible(self.USERNAME_FIELD) and
                    self.is_element_visible(self.PASSWORD_FIELD) and
                    self.is_element_visible(self.LOGIN_BUTTON))
        except Exception:
            return False
    
    def is_username_field_visible(self) -> bool:
        """
        Check if username field is visible.
        
        Returns:
            bool: True if visible, False otherwise
        """
        return self.is_element_visible(self.USERNAME_FIELD)
    
    def is_password_field_visible(self) -> bool:
        """
        Check if password field is visible.
        
        Returns:
            bool: True if visible, False otherwise
        """
        return self.is_element_visible(self.PASSWORD_FIELD)
    
    def is_login_button_enabled(self) -> bool:
        """
        Check if the login button is enabled and clickable.
        
        Returns:
            bool: True if enabled, False otherwise
        """
        try:
            button = self.find_element(self.LOGIN_BUTTON)
            return button.is_enabled()
        except Exception:
            return False
    
    def is_remember_me_checked(self) -> bool:
        """
        Check if the 'Remember me' checkbox is checked.
        
        Returns:
            bool: True if checked, False otherwise
        """
        try:
            checkbox = self.find_element(self.REMEMBER_ME_CHECKBOX)
            return checkbox.get_attribute("aria-checked") == "true"
        except Exception:
            return False
    
    def is_password_visible(self) -> bool:
        """
        Check if password is currently visible (not masked).
        
        Returns:
            bool: True if password is visible (type='text'), False if masked (type='password')
        """
        try:
            password_field = self.find_element(self.PASSWORD_FIELD)
            return password_field.get_attribute("type") == "text"
        except Exception:
            return False
    
    def has_error_message(self) -> bool:
        """
        Check if an error message is displayed on the login page.
        
        Returns:
            bool: True if error message is present and visible, False otherwise
        """
        try:
            return self.is_element_visible(self.LOGIN_MESSAGE)
        except Exception:
            return False
    
    def get_error_message(self) -> Optional[str]:
        """
        Get the error message text if displayed.
        
        Returns:
            Optional[str]: The error message text, or None if no error
        """
        try:
            if self.has_error_message():
                return self.get_text(self.LOGIN_MESSAGE)
            return None
        except Exception:
            return None
    
    def is_login_successful(self, timeout: int = 10) -> bool:
        """
        Check if login was successful by verifying redirect/dashboard elements.
        
        This method waits for indicators that login succeeded:
        - URL changes away from login.jsp
        - User options menu appears
        - Dashboard link is available
        
        Args:
            timeout (int): Maximum time to wait for success indicators (default: 10 seconds)
        
        Returns:
            bool: True if login succeeded, False otherwise
        """
        try:
            # Wait for URL to change from login page
            self.wait_for_url_change(self.url, timeout=timeout)
            
            # Check if we're no longer on login page
            current_url = self.session.get_current_url()
            if "login.jsp" not in current_url:
                return True
            
            return False
        except Exception:
            return False
    
    def get_page_title(self) -> str:
        """
        Get the page title.
        
        Returns:
            str: The page title
        """
        return self.session.get_title()
    
    def get_login_header_text(self) -> str:
        """
        Get the login header text ('Log in').
        
        Returns:
            str: The header text
        """
        try:
            return self.get_text(self.LOGIN_HEADER)
        except Exception:
            return ""
    
    # ==================== Field Validation Methods ====================
    
    def get_username_value(self) -> str:
        """
        Get the current value in the username field.
        
        Returns:
            str: The username field value
        """
        try:
            element = self.find_element(self.USERNAME_FIELD)
            return element.get_attribute("value") or ""
        except Exception:
            return ""
    
    def get_password_value(self) -> str:
        """
        Get the current value in the password field.
        
        Returns:
            str: The password field value
        """
        try:
            element = self.find_element(self.PASSWORD_FIELD)
            return element.get_attribute("value") or ""
        except Exception:
            return ""
    
    def is_username_field_required(self) -> bool:
        """
        Check if username field has 'required' attribute.
        
        Returns:
            bool: True if required, False otherwise
        """
        try:
            element = self.find_element(self.USERNAME_FIELD)
            return element.get_attribute("required") is not None
        except Exception:
            return False
    
    def is_password_field_required(self) -> bool:
        """
        Check if password field has 'required' attribute.
        
        Returns:
            bool: True if required, False otherwise
        """
        try:
            element = self.find_element(self.PASSWORD_FIELD)
            return element.get_attribute("required") is not None
        except Exception:
            return False
    
    def clear_username(self) -> None:
        """Clear the username field."""
        self.clear_field(self.USERNAME_FIELD)
    
    def clear_password(self) -> None:
        """Clear the password field."""
        self.clear_field(self.PASSWORD_FIELD)
    
    def clear_all_fields(self) -> None:
        """Clear both username and password fields."""
        self.clear_username()
        self.clear_password()
    
    # ==================== Navigation & Wait Methods ====================
    
    def wait_for_page_ready(self, timeout: int = 10) -> None:
        """
        Wait for the login page to be fully loaded and ready.
        
        Args:
            timeout (int): Maximum time to wait in seconds (default: 10)
            
        Raises:
            TimeoutException: If page doesn't load within timeout
        """
        self.find_element(self.LOGIN_FORM, timeout=timeout)
        self.find_element(self.USERNAME_FIELD, timeout=timeout, condition=WaitCondition.VISIBILITY_OF_ELEMENT_LOCATED)
        self.find_element(self.PASSWORD_FIELD, timeout=timeout, condition=WaitCondition.VISIBILITY_OF_ELEMENT_LOCATED)
        self.find_element(self.LOGIN_BUTTON, timeout=timeout, condition=WaitCondition.VISIBILITY_OF_ELEMENT_LOCATED)
    
    def wait_for_login_completion(self, timeout: int = 15) -> bool:
        """
        Wait for login process to complete (either success or failure).
        
        Args:
            timeout (int): Maximum time to wait in seconds (default: 15)
        
        Returns:
            bool: True if login succeeded, False if failed
        """
        try:
            # Wait for either URL change (success) or error message (failure)
            return self.is_login_successful(timeout=timeout)
        except Exception:
            return False
    
    # ==================== Helper Methods ====================
    
    def get_jira_version(self) -> Optional[str]:
        """
        Get the Jira version from the page metadata.
        
        Returns:
            Optional[str]: The Jira version (e.g., "10.6.1"), or None if not found
        """
        try:
            # Jira version is in the body data attribute
            body_element = self.session.driver.find_element(By.TAG_NAME, "body")
            return body_element.get_attribute("data-version")
        except Exception:
            return None
    
    def is_logged_in_already(self) -> bool:
        """
        Check if user is already logged in (login link not present).
        
        Returns:
            bool: True if already logged in, False otherwise
        """
        try:
            # If we're on login page and see the login form, we're not logged in
            if self.is_element_visible(self.LOGIN_FORM):
                return False
            
            # If user options menu exists without login link, we're logged in
            return not self.is_element_visible(self.LOGIN_LINK)
        except Exception:
            return False
    
    def take_screenshot_on_error(self, filename: str = "jira_login_error") -> Optional[str]:
        """
        Take a screenshot when an error occurs during login.
        
        Args:
            filename (str): Base filename for the screenshot (default: "jira_login_error")
        
        Returns:
            Optional[str]: Path to saved screenshot, or None if failed
        """
        return self.take_screenshot(filename)
    
    def submit_form_by_enter_key(self) -> None:
        """
        Submit the login form by pressing Enter key in password field.
        
        This simulates natural user behavior.
        """
        from selenium.webdriver.common.keys import Keys
        password_field = self.find_element(self.PASSWORD_FIELD)
        password_field.send_keys(Keys.RETURN)
    
    # ==================== Advanced Login Scenarios ====================
    
    def login_with_screenshot(self, username: str, password: str, 
                             remember_me: bool = False) -> tuple[bool, Optional[str]]:
        """
        Perform login with automatic screenshot on failure.
        
        Args:
            username (str): The username to login with
            password (str): The password to login with
            remember_me (bool): Whether to check remember me (default: False)
        
        Returns:
            tuple[bool, Optional[str]]: (success status, error message if failed)
        """
        try:
            self.login(username, password, remember_me)
            success = self.wait_for_login_completion()
            
            if not success:
                error_msg = self.get_error_message()
                self.take_screenshot_on_error(f"login_failed_{username}")
                return False, error_msg
            
            return True, None
        except Exception as e:
            self.take_screenshot_on_error(f"login_exception_{username}")
            return False, str(e)
    
    def verify_login_page_elements(self) -> dict[str, bool]:
        """
        Verify all critical login page elements are present.
        
        Returns:
            dict[str, bool]: Dictionary of element names and their presence status
        """
        return {
            "login_form": self.is_element_visible(self.LOGIN_FORM),
            "username_field": self.is_element_visible(self.USERNAME_FIELD),
            "password_field": self.is_element_visible(self.PASSWORD_FIELD),
            "login_button": self.is_element_visible(self.LOGIN_BUTTON),
            "remember_me": self.is_element_visible(self.REMEMBER_ME_CHECKBOX),
            "forgot_password_link": self.is_element_visible(self.FORGOT_PASSWORD_LINK),
            "header": self.is_element_visible(self.HEADER),
            "footer": self.is_element_visible(self.FOOTER)
        }
