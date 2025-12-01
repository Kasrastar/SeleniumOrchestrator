"""
Pages Module

This module contains all Page Object Model (POM) classes for the SeleniumOrchestrator.

The Page Object Model is a design pattern that:
- Encapsulates page-specific behavior and locators
- Provides a clear API for page interactions
- Improves test maintainability and reduces code duplication
- Separates test logic from implementation details

Structure:
    base_page.py - Base class with common functionality for all pages
    login_page.py - Example page object for login functionality
    home_page.py - Example page object for home/dashboard functionality
    [Add more page objects here as needed]

Usage:
    from src.pages.login_page import LoginPage
    from src.pages.home_page import HomePage
    
    # Create page objects
    login_page = LoginPage(session, base_url="https://example.com")
    home_page = HomePage(session, base_url="https://example.com")
    
    # Use page objects in tests
    login_page.navigate()
    login_page.login("username", "password")
    assert home_page.is_page_loaded()
"""

from .base_page import BasePage
from .login_page import LoginPage
from .home_page import HomePage

__all__ = [
    'BasePage',
    'LoginPage',
    'HomePage',
]
