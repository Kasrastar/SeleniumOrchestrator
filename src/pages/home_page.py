"""
Example Page Object: Home Page

This is a sample implementation of a Page Object for a home/dashboard page.
It demonstrates how to handle common page elements like navigation, search, and content sections.

Usage:
    from src.pages.home_page import HomePage
    
    home_page = HomePage(session)
    home_page.navigate()
    home_page.search("query")
    items = home_page.get_featured_items()
"""

from typing import List, Optional
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from .base_page import BasePage
from ..core.ports import Locator


class HomePage(BasePage):
    """
    Page Object for a typical home/dashboard page.
    
    This class demonstrates handling of:
    - Navigation menus
    - Search functionality
    - Dynamic content lists
    - User profile sections
    """
    
    def __init__(self, session, base_url: str = "https://example.com"):
        """
        Initialize the HomePage.
        
        Args:
            session (SeleniumSession): The Selenium session
            base_url (str): The base URL of the application
        """
        super().__init__(session)
        self.url = f"{base_url}/home"
    
    # ==================== Header Locators ====================
    
    HEADER = Locator(By.CSS_SELECTOR, "header")
    LOGO = Locator(By.CSS_SELECTOR, "header .logo")
    SEARCH_INPUT = Locator(By.ID, "search")
    SEARCH_BUTTON = Locator(By.CSS_SELECTOR, "button[type='search']")
    USER_PROFILE_ICON = Locator(By.CSS_SELECTOR, ".user-profile-icon")
    USER_DROPDOWN = Locator(By.CSS_SELECTOR, ".user-dropdown")
    
    # ==================== Navigation Menu Locators ====================
    
    NAV_MENU = Locator(By.CSS_SELECTOR, "nav.main-menu")
    NAV_HOME = Locator(By.LINK_TEXT, "Home")
    NAV_PRODUCTS = Locator(By.LINK_TEXT, "Products")
    NAV_ABOUT = Locator(By.LINK_TEXT, "About")
    NAV_CONTACT = Locator(By.LINK_TEXT, "Contact")
    NAV_LOGOUT = Locator(By.LINK_TEXT, "Logout")
    
    # ==================== Content Section Locators ====================
    
    MAIN_CONTENT = Locator(By.CSS_SELECTOR, "main.content")
    WELCOME_MESSAGE = Locator(By.CSS_SELECTOR, ".welcome-message")
    FEATURED_ITEMS = Locator(By.CSS_SELECTOR, ".featured-item")
    ITEM_TITLE = Locator(By.CSS_SELECTOR, ".item-title")
    ITEM_DESCRIPTION = Locator(By.CSS_SELECTOR, ".item-description")
    ITEM_PRICE = Locator(By.CSS_SELECTOR, ".item-price")
    ADD_TO_CART_BUTTON = Locator(By.CSS_SELECTOR, ".add-to-cart")
    
    # ==================== Footer Locators ====================
    
    FOOTER = Locator(By.CSS_SELECTOR, "footer")
    FOOTER_COPYRIGHT = Locator(By.CSS_SELECTOR, "footer .copyright")
    
    # ==================== Header Actions ====================
    
    def search(self, query: str) -> None:
        """
        Perform a search using the search bar.
        
        Args:
            query (str): The search query
        """
        self.clear_and_type(self.SEARCH_INPUT, query)
        self.click(self.SEARCH_BUTTON)
    
    def click_logo(self) -> None:
        """Click the logo to return to home page."""
        self.click(self.LOGO)
    
    def open_user_dropdown(self) -> None:
        """Open the user profile dropdown menu."""
        self.click(self.USER_PROFILE_ICON)
    
    # ==================== Navigation Actions ====================
    
    def navigate_to_home(self) -> None:
        """Navigate to the Home page using the navigation menu."""
        self.click(self.NAV_HOME)
    
    def navigate_to_products(self) -> None:
        """Navigate to the Products page using the navigation menu."""
        self.click(self.NAV_PRODUCTS)
    
    def navigate_to_about(self) -> None:
        """Navigate to the About page using the navigation menu."""
        self.click(self.NAV_ABOUT)
    
    def navigate_to_contact(self) -> None:
        """Navigate to the Contact page using the navigation menu."""
        self.click(self.NAV_CONTACT)
    
    def logout(self) -> None:
        """Logout using the navigation menu."""
        self.click(self.NAV_LOGOUT)
    
    # ==================== Content Interaction Methods ====================
    
    def get_welcome_message(self) -> str:
        """
        Get the welcome message text.
        
        Returns:
            str: The welcome message text
        """
        return self.get_text(self.WELCOME_MESSAGE)
    
    def get_featured_items(self) -> List[WebElement]:
        """
        Get all featured items on the page.
        
        Returns:
            List[WebElement]: List of featured item elements
        """
        return self.find_elements(self.FEATURED_ITEMS)
    
    def get_featured_item_count(self) -> int:
        """
        Get the count of featured items.
        
        Returns:
            int: Number of featured items
        """
        return len(self.get_featured_items())
    
    def get_item_details(self, item_element: WebElement) -> dict:
        """
        Extract details from a featured item element.
        
        Args:
            item_element (WebElement): The item element to extract details from
            
        Returns:
            dict: Dictionary containing item details (title, description, price)
        """
        title_element = self.find_element(self.ITEM_TITLE, root_element=item_element)
        desc_element = self.find_element(self.ITEM_DESCRIPTION, root_element=item_element)
        price_element = self.find_element(self.ITEM_PRICE, root_element=item_element)
        
        return {
            "title": title_element.text if title_element else "",
            "description": desc_element.text if desc_element else "",
            "price": price_element.text if price_element else ""
        }
    
    def get_all_item_details(self) -> List[dict]:
        """
        Get details for all featured items.
        
        Returns:
            List[dict]: List of dictionaries containing item details
        """
        items = self.get_featured_items()
        return [self.get_item_details(item) for item in items]
    
    def add_item_to_cart(self, item_index: int = 0) -> None:
        """
        Add a featured item to cart by index.
        
        Args:
            item_index (int): The index of the item to add (0-based)
        """
        items = self.get_featured_items()
        if item_index < len(items):
            add_button = self.find_element(
                self.ADD_TO_CART_BUTTON,
                root_element=items[item_index]
            )
            if add_button:
                add_button.click()
    
    def add_item_to_cart_by_title(self, title: str) -> bool:
        """
        Add an item to cart by its title.
        
        Args:
            title (str): The title of the item to add
            
        Returns:
            bool: True if item was found and added, False otherwise
        """
        items = self.get_featured_items()
        for item in items:
            item_title_element = self.find_element(self.ITEM_TITLE, root_element=item)
            if item_title_element and title.lower() in item_title_element.text.lower():
                add_button = self.find_element(self.ADD_TO_CART_BUTTON, root_element=item)
                if add_button:
                    add_button.click()
                    return True
        return False
    
    # ==================== Verification Methods ====================
    
    def is_welcome_message_displayed(self) -> bool:
        """
        Check if welcome message is displayed.
        
        Returns:
            bool: True if welcome message is visible, False otherwise
        """
        return self.is_visible(self.WELCOME_MESSAGE)
    
    def is_user_logged_in(self) -> bool:
        """
        Check if a user is logged in.
        
        Returns:
            bool: True if user profile icon is visible, False otherwise
        """
        return self.is_visible(self.USER_PROFILE_ICON)
    
    def has_featured_items(self) -> bool:
        """
        Check if the page has any featured items.
        
        Returns:
            bool: True if featured items exist, False otherwise
        """
        return self.get_featured_item_count() > 0
    
    def is_search_available(self) -> bool:
        """
        Check if search functionality is available.
        
        Returns:
            bool: True if search input is present, False otherwise
        """
        return self.is_present(self.SEARCH_INPUT)
    
    # ==================== Page State Methods ====================
    
    def wait_for_page_load(self, timeout: int = 10) -> bool:
        """
        Wait for the home page to fully load.
        
        Args:
            timeout (int): Maximum wait time in seconds
            
        Returns:
            bool: True if page loaded successfully, False otherwise
        """
        return self.is_visible(self.MAIN_CONTENT, timeout=timeout)
    
    def is_page_loaded(self) -> bool:
        """
        Check if the home page is fully loaded.
        
        Returns:
            bool: True if all critical elements are present, False otherwise
        """
        return (
            self.is_present(self.HEADER) and
            self.is_present(self.NAV_MENU) and
            self.is_present(self.MAIN_CONTENT)
        )
    
    # ==================== Advanced Methods ====================
    
    def scroll_to_footer(self) -> None:
        """Scroll to the footer of the page."""
        footer = self.find_element(self.FOOTER)
        if footer:
            self.execute_script("arguments[0].scrollIntoView({block: 'end'});", footer)
    
    def get_copyright_text(self) -> str:
        """
        Get the copyright text from footer.
        
        Returns:
            str: The copyright text
        """
        return self.get_text(self.FOOTER_COPYRIGHT)
    
    def take_full_page_screenshot(self, filepath: str) -> bool:
        """
        Take a screenshot of the entire home page.
        
        Args:
            filepath (str): Path where to save the screenshot
            
        Returns:
            bool: True if screenshot was saved successfully, False otherwise
        """
        self.scroll_to_top()
        return self.take_screenshot(filepath)
