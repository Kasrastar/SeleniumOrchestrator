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
    jira_login_page.py - Jira-specific login page implementation
    test_cases_page.py - Jira Zephyr Scale Test Cases Library page
    new_test_case_modal.py - Modal component for creating new test cases
    [Add more page objects here as needed]

Usage:
    from src.pages.login_page import LoginPage
    from src.pages.home_page import HomePage
    from src.pages.jira_login_page import JiraLoginPage
    from src.pages.test_cases_page import TestCasesPage
    from src.pages.new_test_case_modal import NewTestCaseModal
    
    # Create page objects
    login_page = LoginPage(session, base_url="https://example.com")
    home_page = HomePage(session, base_url="https://example.com")
    jira_login = JiraLoginPage(session, base_url="https://jira.inside45.ir")
    test_cases = TestCasesPage(session, project_id="10200")
    
    # Use page objects in tests
    login_page.navigate()
    login_page.login("username", "password")
    assert home_page.is_page_loaded()
    
    # Use page + modal pattern
    test_cases.navigate()
    modal = test_cases.click_new_test_case()
    modal.create_test_case(name="My Test", priority="High")
"""

from .base_page import BasePage
from .login_page import LoginPage
from .home_page import HomePage
from .jira_login_page import JiraLoginPage
from .test_cases_page import TestCasesPage
from .new_test_case_modal import NewTestCaseModal
from .test_case_detail_page import TestCaseDetailPage

__all__ = [
    'BasePage',
    'LoginPage',
    'HomePage',
    'JiraLoginPage',
    'TestCasesPage',
    'NewTestCaseModal',
]

