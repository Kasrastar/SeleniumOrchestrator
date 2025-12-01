"""
Base Page Object Module

This module provides the BasePage class that all page objects should inherit from.
It encapsulates common functionality and provides a clean interface for page interactions.

Design Pattern: Page Object Model (POM)
- Separates test logic from page-specific code
- Improves maintainability and reduces code duplication
- Provides reusable methods for common page interactions
"""

from typing import Optional, List, Any
from selenium.webdriver.remote.webelement import WebElement

from ..core.ports import Locator, WaitCondition
from ..application.element_service import ElementService
from ..infra.selenium_session import SeleniumSession


class BasePage:
    """
    Base class for all Page Objects.
    
    Provides common functionality for page interactions including:
    - Element location and interaction
    - Navigation
    - Wait conditions
    - Page state verification
    
    Attributes:
        session (SeleniumSession): The Selenium session instance
        element_service (ElementService): Service for element interactions
        url (str): The base URL of the page (override in subclasses)
    """
    
    def __init__(self, session: SeleniumSession):
        """
        Initialize the BasePage.
        
        Args:
            session (SeleniumSession): The Selenium session to use for interactions
        """
        self.session = session
        self.element_service = ElementService(session)
        self.url = ""  # Override in subclass
    
    # ==================== Navigation Methods ====================
    
    def navigate(self) -> None:
        """Navigate to the page's URL."""
        if not self.url:
            raise ValueError(f"URL not defined for {self.__class__.__name__}")
        self.session.get(self.url)
    
    def get_current_url(self) -> str:
        """
        Get the current page URL.
        
        Returns:
            str: The current URL
        """
        if self.session.driver:
            return self.session.driver.current_url
        return ""
    
    def get_title(self) -> str:
        """
        Get the current page title.
        
        Returns:
            str: The page title
        """
        if self.session.driver:
            return self.session.driver.title
        return ""
    
    def refresh(self) -> None:
        """Refresh the current page."""
        if self.session.driver:
            self.session.driver.refresh()
    
    def go_back(self) -> None:
        """Navigate back to the previous page."""
        if self.session.driver:
            self.session.driver.back()
    
    def go_forward(self) -> None:
        """Navigate forward to the next page."""
        if self.session.driver:
            self.session.driver.forward()
    
    # ==================== Element Interaction Methods ====================
    
    def click(self, locator: Locator, root_element: Optional[WebElement] = None) -> None:
        """
        Click an element.
        
        Args:
            locator (Locator): The locator to find the element
            root_element (Optional[WebElement]): Parent element to search within
        """
        self.element_service.click(locator, root_element=root_element)
    
    def type(self, locator: Locator, text: str, root_element: Optional[WebElement] = None) -> None:
        """
        Type text into an input field.
        
        Args:
            locator (Locator): The locator to find the element
            text (str): The text to type
            root_element (Optional[WebElement]): Parent element to search within
        """
        self.element_service.send_keys(locator, text, root_element=root_element)
    
    def clear(self, locator: Locator, root_element: Optional[WebElement] = None) -> None:
        """
        Clear an input field.
        
        Args:
            locator (Locator): The locator to find the element
            root_element (Optional[WebElement]): Parent element to search within
        """
        self.element_service.clear(locator, root_element=root_element)
    
    def clear_and_type(self, locator: Locator, text: str, root_element: Optional[WebElement] = None) -> None:
        """
        Clear an input field and type new text.
        
        Args:
            locator (Locator): The locator to find the element
            text (str): The text to type
            root_element (Optional[WebElement]): Parent element to search within
        """
        self.clear(locator, root_element)
        self.type(locator, text, root_element)
    
    # ==================== Element Query Methods ====================
    
    def find_element(
        self,
        locator: Locator,
        timeout: int = 10,
        condition: str = WaitCondition.PRESENCE_OF_ELEMENT_LOCATED,
        root_element: Optional[WebElement] = None
    ) -> Optional[WebElement]:
        """
        Find a single element.
        
        Args:
            locator (Locator): The locator to find the element
            timeout (int): Maximum wait time in seconds
            condition (str): Wait condition to use
            root_element (Optional[WebElement]): Parent element to search within
            
        Returns:
            Optional[WebElement]: The found element or None
        """
        return self.session.find_element(locator, timeout, condition, root_element)
    
    def find_elements(
        self,
        locator: Locator,
        timeout: int = 10,
        scroll_into_view: bool = False,
        root_element: Optional[WebElement] = None
    ) -> List[WebElement]:
        """
        Find multiple elements.
        
        Args:
            locator (Locator): The locator to find elements
            timeout (int): Maximum wait time in seconds
            scroll_into_view (bool): Whether to scroll elements into view
            root_element (Optional[WebElement]): Parent element to search within
            
        Returns:
            List[WebElement]: List of found elements
        """
        return self.element_service.find_all(locator, timeout, scroll_into_view, root_element)
    
    def get_text(self, locator: Locator, root_element: Optional[WebElement] = None) -> str:
        """
        Get text content of an element.
        
        Args:
            locator (Locator): The locator to find the element
            root_element (Optional[WebElement]): Parent element to search within
            
        Returns:
            str: The text content
        """
        element = self.find_element(locator, root_element=root_element)
        return element.text if element else ""
    
    def get_attribute(
        self,
        locator: Locator,
        attribute: str,
        root_element: Optional[WebElement] = None
    ) -> Optional[str]:
        """
        Get an attribute value from an element.
        
        Args:
            locator (Locator): The locator to find the element
            attribute (str): The attribute name
            root_element (Optional[WebElement]): Parent element to search within
            
        Returns:
            Optional[str]: The attribute value or None
        """
        element = self.find_element(locator, root_element=root_element)
        return element.get_attribute(attribute) if element else None
    
    # ==================== Element State Methods ====================
    
    def is_visible(self, locator: Locator, timeout: int = 10) -> bool:
        """
        Check if an element is visible.
        
        Args:
            locator (Locator): The locator to find the element
            timeout (int): Maximum wait time in seconds
            
        Returns:
            bool: True if element is visible, False otherwise
        """
        element = self.find_element(
            locator,
            timeout=timeout,
            condition=WaitCondition.VISIBILITY_OF_ELEMENT_LOCATED
        )
        return element is not None
    
    def is_clickable(self, locator: Locator, timeout: int = 10) -> bool:
        """
        Check if an element is clickable.
        
        Args:
            locator (Locator): The locator to find the element
            timeout (int): Maximum wait time in seconds
            
        Returns:
            bool: True if element is clickable, False otherwise
        """
        element = self.find_element(
            locator,
            timeout=timeout,
            condition=WaitCondition.ELEMENT_TO_BE_CLICKABLE
        )
        return element is not None
    
    def is_present(self, locator: Locator, timeout: int = 10) -> bool:
        """
        Check if an element is present in the DOM.
        
        Args:
            locator (Locator): The locator to find the element
            timeout (int): Maximum wait time in seconds
            
        Returns:
            bool: True if element is present, False otherwise
        """
        element = self.find_element(locator, timeout=timeout)
        return element is not None
    
    # ==================== JavaScript Execution Methods ====================
    
    def execute_script(self, script: str, *args: Any) -> Any:
        """
        Execute JavaScript code.
        
        Args:
            script (str): The JavaScript code to execute
            *args: Arguments to pass to the script
            
        Returns:
            Any: The return value from the script
        """
        if self.session.driver:
            return self.session.driver.execute_script(script, *args)
        return None
    
    def scroll_to_element(self, locator: Locator) -> None:
        """
        Scroll to make an element visible.
        
        Args:
            locator (Locator): The locator to find the element
        """
        element = self.find_element(locator)
        if element:
            self.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
    
    def scroll_to_top(self) -> None:
        """Scroll to the top of the page."""
        self.execute_script("window.scrollTo(0, 0);")
    
    def scroll_to_bottom(self) -> None:
        """Scroll to the bottom of the page."""
        self.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    
    # ==================== Wait Methods ====================
    
    def wait_for_url_to_contain(self, text: str, timeout: int = 10) -> bool:
        """
        Wait for URL to contain specific text.
        
        Args:
            text (str): Text to wait for in URL
            timeout (int): Maximum wait time in seconds
            
        Returns:
            bool: True if URL contains text within timeout, False otherwise
        """
        from selenium.webdriver.support.ui import WebDriverWait
        from selenium.webdriver.support import expected_conditions as EC
        from selenium.common.exceptions import TimeoutException
        
        try:
            if self.session.driver:
                WebDriverWait(self.session.driver, timeout).until(
                    EC.url_contains(text)
                )
                return True
        except TimeoutException:
            pass
        return False
    
    def wait_for_title_to_contain(self, text: str, timeout: int = 10) -> bool:
        """
        Wait for page title to contain specific text.
        
        Args:
            text (str): Text to wait for in title
            timeout (int): Maximum wait time in seconds
            
        Returns:
            bool: True if title contains text within timeout, False otherwise
        """
        from selenium.webdriver.support.ui import WebDriverWait
        from selenium.webdriver.support import expected_conditions as EC
        from selenium.common.exceptions import TimeoutException
        
        try:
            if self.session.driver:
                WebDriverWait(self.session.driver, timeout).until(
                    EC.title_contains(text)
                )
                return True
        except TimeoutException:
            pass
        return False
    
    # ==================== Screenshot Methods ====================
    
    def take_screenshot(self, filepath: str) -> bool:
        """
        Take a screenshot and save to file.
        
        Args:
            filepath (str): Path where to save the screenshot
            
        Returns:
            bool: True if screenshot was saved successfully, False otherwise
        """
        if self.session.driver:
            return self.session.driver.save_screenshot(filepath)
        return False
    
    def take_element_screenshot(self, locator: Locator, filepath: str) -> bool:
        """
        Take a screenshot of a specific element.
        
        Args:
            locator (Locator): The locator to find the element
            filepath (str): Path where to save the screenshot
            
        Returns:
            bool: True if screenshot was saved successfully, False otherwise
        """
        element = self.find_element(locator)
        if element:
            return element.screenshot(filepath)
        return False
