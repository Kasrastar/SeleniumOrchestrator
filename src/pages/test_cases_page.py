"""
Test Cases Page Object Module

This module provides the TestCasesPage class for interacting with the Jira Zephyr Scale
Test Cases Library page. It handles folder navigation, test case management, and
interaction with the New Test Case modal.

Page URL: https://jira.inside45.ir/secure/Tests.jspa#/v2/testCases?projectId={projectId}

Design Pattern: Page Object Model (POM) with Modal Component
"""

from typing import Optional, List
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement

from ..core.ports import Locator, WaitCondition
from .base_page import BasePage
from .new_test_case_modal import NewTestCaseModal
from ..infra.selenium_session import SeleniumSession


class TestCasesPage(BasePage):
    """
    Page Object for Jira Zephyr Scale Test Cases Library.
    
    This page provides functionality for:
    - Navigating the test case folder tree
    - Creating new test cases and folders
    - Searching and filtering test cases
    - Managing test case archives
    - Accessing various test case operations
    
    Attributes:
        PAGE_URL (str): Base URL pattern for the test cases page
        PROJECT_ID (str): Current project ID (must be set before use)
    """
    
    # ==================== Page URL ====================
    
    PAGE_URL = "https://jira.inside45.ir/secure/Tests.jspa#/v2/testCases?projectId={project_id}"
    PROJECT_ID = "10200"  # Default project ID
    
    # ==================== Header Locators ====================
    
    PROJECT_SELECTOR = Locator(By.CSS_SELECTOR, "[data-testid='zephyr-scale-v2'] .css-1uadcpv")
    PROJECT_NAME = Locator(By.CSS_SELECTOR, "[data-testid='zephyr-scale-v2'] .css-1uadcpv")
    CONFIGURATION_BUTTON = Locator(By.CSS_SELECTOR, "button[data-testid='zscale-configuration']")
    
    # ==================== Tab Navigation Locators ====================
    
    TEST_CASES_TAB = Locator(By.CSS_SELECTOR, "div[data-testid='zscale-testcase-library'][role='tab']")
    TEST_CYCLES_TAB = Locator(By.CSS_SELECTOR, "div[data-testid='zscale-testcycle-library'][role='tab']")
    TEST_PLANS_TAB = Locator(By.CSS_SELECTOR, "div[data-testid='zscale-testplan-library'][role='tab']")
    REPORTS_TAB = Locator(By.CSS_SELECTOR, "div[data-testid='zscale-reports'][role='tab']")
    
    # ==================== Folder Tree Locators ====================
    
    FOLDER_TREE_CONTAINER = Locator(By.CSS_SELECTOR, "[data-testid='folder-tree-container']")
    NEW_FOLDER_BUTTON = Locator(By.CSS_SELECTOR, "button[data-testid='ktm-create-new-folder']")
    FOLDER_SEARCH_TRIGGER = Locator(By.CSS_SELECTOR, "[data-testid='ktm-search-trigger'] button")
    FOLDER_OPTIONS_BUTTON = Locator(By.CSS_SELECTOR, "button.folder-tree-options")
    
    # All test cases folder
    ALL_TEST_CASES_FOLDER = Locator(By.CSS_SELECTOR, "[data-testid='folder-item-root']")
    ALL_TEST_CASES_COUNT = Locator(By.CSS_SELECTOR, "[data-testid='folder-name-with-count-root'] .css-175qx7m")
    
    # Folder items (dynamic)
    FOLDER_ITEM_TEMPLATE = "div[data-testid='folder-item-{folder_id}']"
    FOLDER_NAME_TEMPLATE = "[data-testid='folder-name-with-count-{folder_id}'] .css-15xv5ui"
    FOLDER_COUNT_TEMPLATE = "[data-testid='folder-name-with-count-{folder_id}'] .css-175qx7m"
    FOLDER_OPTIONS_TEMPLATE = "[data-testid='folder-item-{folder_id}'] button.folder-item-dropdown"
    
    # Selected folder
    SELECTED_FOLDER = Locator(By.CSS_SELECTOR, ".ktm-folder-tree-item.isSelected")
    
    # Archived test cases button
    ARCHIVED_TEST_CASES_BUTTON = Locator(By.CSS_SELECTOR, "button.css-e406dc[aria-pressed='false']")
    
    # ==================== Action Bar Locators ====================
    
    NEW_TEST_CASE_BUTTON = Locator(By.CSS_SELECTOR, "button.css-1jk3zmn")
    ARCHIVE_BUTTON = Locator(By.CSS_SELECTOR, "button.css-1izmkx6[disabled]")
    CLONE_BUTTON = Locator("xpath", "//button[.//span[text()='Clone']]")
    MORE_BUTTON = Locator(By.CSS_SELECTOR, "button.css-xbpjo7")
    
    # ==================== Search and Filter Locators ====================
    
    SEARCH_INPUT = Locator(By.CSS_SELECTOR, "input#zephyr-scale-grid-search")
    FILTERS_BUTTON = Locator(By.CSS_SELECTOR, "button.expand-filters-button")
    
    # ==================== Content Area Locators ====================
    
    EMPTY_STATE_MESSAGE = Locator(By.CSS_SELECTOR, ".css-mlhl9a h4")
    EMPTY_STATE_CREATE_LINK = Locator(By.CSS_SELECTOR, ".css-mlhl9a button.css-eqzzma")
    TEST_CASES_GRID = Locator(By.CSS_SELECTOR, ".css-mlhl9a")
    
    # ==================== Specific Folder Locators ====================
    
    # Predefined folders by name
    LOGIN_FOLDER = Locator(By.CSS_SELECTOR, "[data-folder-name='Login']")
    REGISTRATION_FOLDER = Locator(By.CSS_SELECTOR, "[data-folder-name='Registration']")
    AUCTION_LIST_FOLDER = Locator(By.CSS_SELECTOR, "[data-folder-name='Auction List']")
    K45_LIBRARY_FOLDER = Locator(By.CSS_SELECTOR, "[data-folder-name='K45-library']")
    
    def __init__(self, session: SeleniumSession, project_id: str = None):
        """
        Initialize the TestCasesPage.
        
        Args:
            session (SeleniumSession): The Selenium session to use
            project_id (str, optional): Project ID to use. Defaults to class PROJECT_ID
        """
        super().__init__(session)
        if project_id:
            self.PROJECT_ID = project_id
        self.url = self.PAGE_URL.format(project_id=self.PROJECT_ID)
    
    # ==================== Navigation Methods ====================
    
    def navigate_to_project(self, project_id: str) -> None:
        """
        Navigate to a specific project's test cases page.
        
        Args:
            project_id (str): The project ID to navigate to
        """
        self.PROJECT_ID = project_id
        self.url = self.PAGE_URL.format(project_id=project_id)
        self.navigate()
    
    def switch_to_test_cycles(self) -> None:
        """Switch to the Test Cycles tab."""
        self.click(self.TEST_CYCLES_TAB)
    
    def switch_to_test_plans(self) -> None:
        """Switch to the Test Plans tab."""
        self.click(self.TEST_PLANS_TAB)
    
    def switch_to_reports(self) -> None:
        """Switch to the Reports tab."""
        self.click(self.REPORTS_TAB)
    
    def click_configuration(self) -> None:
        """Click the Configuration button."""
        self.click(self.CONFIGURATION_BUTTON)
    
    # ==================== Folder Tree Methods ====================
    
    def click_new_folder(self) -> None:
        """Click the New Folder button to create a new folder."""
        self.click(self.NEW_FOLDER_BUTTON)
    
    def click_folder_search(self) -> None:
        """Click the folder search trigger button."""
        self.click(self.FOLDER_SEARCH_TRIGGER)
    
    def click_folder_options(self) -> None:
        """Click the folder tree options (three dots) button."""
        self.click(self.FOLDER_OPTIONS_BUTTON)
    
    def click_all_test_cases_folder(self) -> None:
        """Click on the 'All test cases' root folder."""
        self.click(self.ALL_TEST_CASES_FOLDER)
    
    def get_all_test_cases_count(self) -> str:
        """
        Get the count of all test cases.
        
        Returns:
            str: The test case count (e.g., "(171)")
        """
        element = self.find_element(self.ALL_TEST_CASES_COUNT, condition=WaitCondition.VISIBILITY_OF_ELEMENT_LOCATED)
        return element.text if element else "0"
    
    def click_folder_by_id(self, folder_id: str) -> None:
        """
        Click a folder by its ID.
        
        Args:
            folder_id (str): The folder ID (e.g., "2" for Login folder)
        """
        locator = Locator(By.CSS_SELECTOR, self.FOLDER_ITEM_TEMPLATE.format(folder_id=folder_id))
        self.click(locator)
    
    def click_folder_by_name(self, folder_name: str) -> None:
        """
        Click a folder by its name.
        
        Args:
            folder_name (str): The folder name (e.g., "Login")
        """
        locator = Locator(By.CSS_SELECTOR, f"[data-folder-name='{folder_name}']")
        self.click(locator)
    
    def get_folder_count(self, folder_id: str) -> str:
        """
        Get the test case count for a specific folder.
        
        Args:
            folder_id (str): The folder ID
            
        Returns:
            str: The test case count (e.g., "(14)")
        """
        locator = Locator(By.CSS_SELECTOR, self.FOLDER_COUNT_TEMPLATE.format(folder_id=folder_id))
        element = self.find_element(locator, condition=WaitCondition.VISIBILITY_OF_ELEMENT_LOCATED)
        return element.text if element else "0"
    
    def click_folder_options_by_id(self, folder_id: str) -> None:
        """
        Click the options button (three dots) for a specific folder.
        
        Args:
            folder_id (str): The folder ID
        """
        locator = Locator(By.CSS_SELECTOR, self.FOLDER_OPTIONS_TEMPLATE.format(folder_id=folder_id))
        self.click(locator)
    
    def is_folder_selected(self, folder_id: str) -> bool:
        """
        Check if a folder is currently selected.
        
        Args:
            folder_id (str): The folder ID to check
            
        Returns:
            bool: True if the folder is selected, False otherwise
        """
        locator = Locator(By.CSS_SELECTOR, f"[data-folder-id='{folder_id}'].isSelected")
        return self.is_element_visible(locator)
    
    def expand_folder(self, folder_id: str) -> None:
        """
        Expand a folder to show its subfolders.
        
        Args:
            folder_id (str): The folder ID to expand
        """
        chevron_locator = Locator(By.CSS_SELECTOR, f"[data-testid='folder-item-{folder_id}'] [data-testid='rotating-chevron']")
        self.click(chevron_locator)
    
    def click_archived_test_cases(self) -> None:
        """Click the Archived test cases button."""
        self.click(self.ARCHIVED_TEST_CASES_BUTTON)
    
    # ==================== Action Bar Methods ====================
    
    def click_new_test_case(self) -> NewTestCaseModal:
        """
        Click the 'New Test Case' button to open the modal.
        
        Returns:
            NewTestCaseModal: Instance of the modal page object
        """
        self.click(self.NEW_TEST_CASE_BUTTON)
        return NewTestCaseModal(self.session)
    
    def click_archive(self) -> None:
        """Click the Archive button (if enabled)."""
        self.click(self.ARCHIVE_BUTTON)
    
    def click_clone(self) -> None:
        """Click the Clone button (if enabled)."""
        self.click(self.CLONE_BUTTON)
    
    def click_more(self) -> None:
        """Click the More dropdown button."""
        self.click(self.MORE_BUTTON)
    
    # ==================== Search and Filter Methods ====================
    
    def enter_search_text(self, text: str) -> None:
        """
        Enter text in the search field.
        
        Args:
            text (str): The search text to enter
        """
        self.type_text(self.SEARCH_INPUT, text)
    
    def clear_search(self) -> None:
        """Clear the search field."""
        self.clear(self.SEARCH_INPUT)
    
    def click_filters(self) -> None:
        """Click the Filters button to expand filter options."""
        self.click(self.FILTERS_BUTTON)
    
    # ==================== Content Area Methods ====================
    
    def is_empty_state_displayed(self) -> bool:
        """
        Check if the empty state message is displayed.
        
        Returns:
            bool: True if empty state is shown, False otherwise
        """
        return self.is_element_visible(self.EMPTY_STATE_MESSAGE)
    
    def get_empty_state_message(self) -> str:
        """
        Get the empty state message text.
        
        Returns:
            str: The empty state message (e.g., "No test cases")
        """
        element = self.find_element(self.EMPTY_STATE_MESSAGE, condition=WaitCondition.VISIBILITY_OF_ELEMENT_LOCATED)
        return element.text if element else ""
    
    def click_empty_state_create_link(self) -> NewTestCaseModal:
        """
        Click the 'Create a test case' link in the empty state.
        
        Returns:
            NewTestCaseModal: Instance of the modal page object
        """
        self.click(self.EMPTY_STATE_CREATE_LINK)
        return NewTestCaseModal(self.session)
    
    # ==================== Verification Methods ====================
    
    def is_test_cases_tab_active(self) -> bool:
        """
        Verify that the Test Cases tab is active.
        
        Returns:
            bool: True if Test Cases tab is active
        """
        element = self.find_element(self.TEST_CASES_TAB, condition=WaitCondition.VISIBILITY_OF_ELEMENT_LOCATED)
        return element and "css-190fm5y" in element.get_attribute("class")
    
    def wait_for_page_ready(self, timeout: int = 10) -> bool:
        """
        Wait for the test cases page to be fully loaded.
        
        Args:
            timeout (int): Maximum time to wait in seconds
            
        Returns:
            bool: True if page is ready, False otherwise
        """
        try:
            self.find_element(
                self.FOLDER_TREE_CONTAINER,
                timeout=timeout,
                condition=WaitCondition.VISIBILITY_OF_ELEMENT_LOCATED
            )
            self.find_element(
                self.TEST_CASES_TAB,
                timeout=timeout,
                condition=WaitCondition.VISIBILITY_OF_ELEMENT_LOCATED
            )
            self.find_element(
                self.NEW_TEST_CASE_BUTTON,
                timeout=timeout,
                condition=WaitCondition.VISIBILITY_OF_ELEMENT_LOCATED
            )
            return True
        except Exception:
            return False
    
    def get_current_project_name(self) -> str:
        """
        Get the current project name.
        
        Returns:
            str: The project name (e.g., "Software Development Life Cycle")
        """
        element = self.find_element(self.PROJECT_NAME, condition=WaitCondition.VISIBILITY_OF_ELEMENT_LOCATED)
        return element.text if element else ""
    
    def get_selected_folder_name(self) -> str:
        """
        Get the name of the currently selected folder.
        
        Returns:
            str: The selected folder name
        """
        element = self.find_element(self.SELECTED_FOLDER, condition=WaitCondition.VISIBILITY_OF_ELEMENT_LOCATED)
        if element:
            name_element = element.find_element("css selector", ".css-15xv5ui")
            return name_element.text if name_element else ""
        return ""
    
    # ==================== Advanced Folder Methods ====================
    
    def get_all_visible_folders(self) -> List[dict]:
        """
        Get all visible folders in the tree.
        
        Returns:
            List[dict]: List of folder dictionaries with 'id', 'name', and 'count'
        """
        folders = []
        folder_elements = self.find_elements(Locator(By.CSS_SELECTOR, "[data-folder-id]"))
        
        for folder_elem in folder_elements:
            folder_id = folder_elem.get_attribute("data-folder-id")
            folder_name = folder_elem.get_attribute("data-folder-name")
            
            # Get count if available
            try:
                count_elem = folder_elem.find_element("css selector", ".css-175qx7m")
                count = count_elem.text
            except:
                count = None
            
            folders.append({
                "id": folder_id,
                "name": folder_name,
                "count": count
            })
        
        return folders
    
    def navigate_to_folder_path(self, folder_path: str) -> None:
        """
        Navigate to a folder using its path.
        
        Args:
            folder_path (str): The folder path (e.g., "/K45-library/dealer/aaa/login")
        """
        # Split path and navigate through each level
        path_parts = [p for p in folder_path.split("/") if p]
        
        for folder_name in path_parts:
            self.click_folder_by_name(folder_name)
            self.wait(1)  # Wait for folder to expand
    
    # ==================== Helper Methods ====================
    
    def wait_for_folder_tree_loaded(self, timeout: int = 10) -> bool:
        """
        Wait for the folder tree to be fully loaded.
        
        Args:
            timeout (int): Maximum time to wait in seconds
            
        Returns:
            bool: True if loaded, False otherwise
        """
        try:
            container = self.find_element(
                self.FOLDER_TREE_CONTAINER,
                timeout=timeout,
                condition=WaitCondition.VISIBILITY_OF_ELEMENT_LOCATED
            )
            if container:
                is_loaded = container.get_attribute("data-is-folder-tree-loaded")
                return is_loaded == "true"
            return False
        except Exception:
            return False
