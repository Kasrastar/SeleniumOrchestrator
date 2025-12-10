"""
Test Case Detail Page Object Module

This module provides the TestCaseDetailPage class for interacting with the Jira Zephyr
Test Case detail/edit page. Handles test case details, test script steps, and tab navigation.

Page URL: https://jira.inside45.ir/secure/Tests.jspa#/testCase/{TEST_KEY}

Design Pattern: Page Object Model with Tab Components
"""

from typing import Optional, List, Dict
from time import sleep
import logging
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webelement import WebElement

from ..core.ports import Locator, WaitCondition
from .base_page import BasePage
from ..infra.selenium_session import SeleniumSession


class TestCaseDetailPage(BasePage):
    """Page object for Test Case Detail/Edit Page in Jira Zephyr.
    
    This page appears after creating a test case or navigating to an existing test case.
    Provides functionality for editing test details, adding test scripts (steps), and
    managing test case information.
    """

    def __init__(self, session: SeleniumSession, test_case_key: Optional[str] = None):
        super().__init__(session)
        self.test_case_key = test_case_key
        self.logger = logging.getLogger(f"{__name__}.{self.__class__.__name__}")
        if test_case_key:
            self.url = f"{self.base_url}/secure/Tests.jspa#/testCase/{test_case_key}"

    # ==================== Header and Navigation Locators ====================
    
    PAGE_HEADER = Locator(By.CSS_SELECTOR, "header.aui-page-header")
    PAGE_TITLE = Locator(By.CSS_SELECTOR, "h1.ktm-header-title")
    BREADCRUMB_CONTAINER = Locator(By.CSS_SELECTOR, ".ktm-breadcrumb-container")
    
    # Action buttons in header
    BACK_BUTTON = Locator(By.CSS_SELECTOR, "button.aui-button-link[ng-click='goBack()']")
    SAVE_BUTTON = Locator(By.CSS_SELECTOR, "button.ktm-save-button")
    NEW_VERSION_BUTTON = Locator(By.CSS_SELECTOR, "a.aui-button-split-main")
    VERSION_DROPDOWN = Locator(By.CSS_SELECTOR, "button.ktm-version-picker-new-ui")
    
    # Tab navigation
    TAB_CONTAINER = Locator(By.CSS_SELECTOR, "nav.aui-navgroup-horizontal")
    DETAILS_TAB = Locator(By.XPATH, "//li//a[contains(., 'Details')]")
    TEST_SCRIPT_TAB = Locator(By.XPATH, "//li//a[contains(., 'Test Script')]")
    EXECUTION_TAB = Locator(By.XPATH, "//li//a[contains(., 'Execution')]")
    TRACEABILITY_TAB = Locator(By.XPATH, "//li//a[contains(., 'Traceability')]")
    ATTACHMENTS_TAB = Locator(By.XPATH, "//li//a[contains(., 'Attachments')]")
    COMMENTS_TAB = Locator(By.XPATH, "//li//a[contains(., 'Comments')]")
    HISTORY_TAB = Locator(By.XPATH, "//li//a[contains(., 'History')]")
    ACTIVE_TAB = Locator(By.CSS_SELECTOR, "li.aui-nav-selected")
    
    # ==================== Details Tab Locators ====================
    
    # Name section
    NAME_INPUT = Locator(By.CSS_SELECTOR, "input[ng-model='testCase.name']")
    
    # Objective section
    OBJECTIVE_CONTAINER = Locator(By.CSS_SELECTOR, "rich-text[name='objective']")
    OBJECTIVE_CONTENT = Locator(By.CSS_SELECTOR, "rich-text[name='objective'] .ktm-editor-html-viewer")
    
    # Precondition section
    PRECONDITION_CONTAINER = Locator(By.CSS_SELECTOR, "rich-text[name='precondition']")
    PRECONDITION_CONTENT = Locator(By.CSS_SELECTOR, "rich-text[name='precondition'] .ktm-editor-html-viewer")
    
    # Details fields
    STATUS_DROPDOWN = Locator(By.CSS_SELECTOR, "select-box[name='status'] button")
    PRIORITY_DROPDOWN = Locator(By.CSS_SELECTOR, "select-box[name='priority'] button")
    COMPONENT_DROPDOWN = Locator(By.CSS_SELECTOR, "select-box[name='component'] button")
    OWNER_DROPDOWN = Locator(By.CSS_SELECTOR, "user-picker[name='owner'] button")
    ESTIMATED_TIME_INPUT = Locator(By.CSS_SELECTOR, "input[name='estimatedTime']")
    FOLDER_DROPDOWN = Locator(By.CSS_SELECTOR, "select-box[name='folder'] button")
    LABELS_INPUT = Locator(By.CSS_SELECTOR, "tags-input[name='labels'] input.input")
    
    # ==================== Test Script Tab Locators ====================
    
    # Test script type selector
    SCRIPT_TYPE_DROPDOWN = Locator(By.CSS_SELECTOR, "select-box#ktm-test-script-options-selector button")
    SCRIPT_TYPE_DROPDOWN_MENU = Locator(By.CSS_SELECTOR, "#select-box-5")
    
    # Script type options in dropdown
    SCRIPT_TYPE_PLAIN_TEXT = Locator(By.XPATH, "//div[@id='select-box-5']//a[contains(., 'Plain Text')]")
    SCRIPT_TYPE_STEP_BY_STEP = Locator(By.XPATH, "//div[@id='select-box-5']//a[contains(., 'Step-by-Step')]")
    SCRIPT_TYPE_BDD = Locator(By.XPATH, "//div[@id='select-box-5']//a[contains(., 'BDD')]")
    
    # Test parameters button (for step-by-step)
    TEST_PARAMETERS_BUTTON = Locator(By.CSS_SELECTOR, "button#ktm-test-parameters-dropdown")
    
    # Steps container and actions
    STEPS_CONTAINER = Locator(By.CSS_SELECTOR, ".ktm-testscript-steps")
    ADD_STEP_BUTTON = Locator(By.CSS_SELECTOR, "button[ng-click='onAddStep(0)']")
    STEPS_HINT = Locator(By.CSS_SELECTOR, "span.ktm-hint")
    
    # Individual step locators (templates - will be formatted with index)
    STEP_CONTAINER_TEMPLATE = "[ng-repeat='step in currentSteps() | orderBy:\"index\"']:nth-of-type({index})"
    STEP_INDEX_TEMPLATE = ".ktm-testscript-step:nth-of-type({index}) .ktm-index-number"
    STEP_DESCRIPTION_TEMPLATE = ".ktm-testscript-step:nth-of-type({index}) rich-text[name='stepDescription-{index}']"
    STEP_TEST_DATA_TEMPLATE = ".ktm-testscript-step:nth-of-type({index}) rich-text[name='stepTestData-{index}']"
    STEP_EXPECTED_RESULT_TEMPLATE = ".ktm-testscript-step:nth-of-type({index}) rich-text[name='stepExpectedResult-{index}']"
    
    # Step action buttons
    STEP_DELETE_BUTTON_TEMPLATE = ".ktm-testscript-step:nth-of-type({index}) button[ng-click='deleteStep()']"
    STEP_ATTACH_FILES_BUTTON_TEMPLATE = ".ktm-testscript-step:nth-of-type({index}) button[ngf-select]"
    STEP_CLONE_BUTTON_TEMPLATE = ".ktm-testscript-step:nth-of-type({index}) button[ng-click='cloneStep()']"
    STEP_CALL_TO_TEST_BUTTON_TEMPLATE = ".ktm-testscript-step:nth-of-type({index}) button[ng-click='addCallToTest()']"
    STEP_ADD_STEP_BUTTON_TEMPLATE = ".ktm-testscript-step:nth-of-type({index}) button[ng-click='addStep()']"
    
    # Editable content divs for steps
    STEP_DESCRIPTION_EDITOR = Locator(By.CSS_SELECTOR, "rich-text[name^='stepDescription'] .ktm-editor-html-viewer[contenteditable='true']")
    STEP_TEST_DATA_EDITOR = Locator(By.CSS_SELECTOR, "rich-text[name^='stepTestData'] .ktm-editor-html-viewer[contenteditable='true']")
    STEP_EXPECTED_RESULT_EDITOR = Locator(By.CSS_SELECTOR, "rich-text[name^='stepExpectedResult'] .ktm-editor-html-viewer[contenteditable='true']")
    
    # All steps
    ALL_STEPS = Locator(By.CSS_SELECTOR, ".ktm-testscript-step")
    
    # ==================== Navigation Methods ====================
    
    def navigate_to_test_case(self, test_case_key: str) -> None:
        """Navigate to a specific test case detail page."""
        self.test_case_key = test_case_key
        self.url = f"{self.base_url}/secure/Tests.jspa#/testCase/{test_case_key}"
        self.navigate()
        self.logger.info(f"Navigated to test case: {test_case_key}")
    
    def wait_for_page_ready(self, timeout: int = 10) -> bool:
        """Wait for the test case detail page to be fully loaded."""
        try:
            self.find_element(self.PAGE_HEADER, timeout=timeout, 
                            condition=WaitCondition.VISIBILITY_OF_ELEMENT_LOCATED)
            self.find_element(self.PAGE_TITLE, timeout=timeout, 
                            condition=WaitCondition.VISIBILITY_OF_ELEMENT_LOCATED)
            return True
        except Exception as e:
            self.logger.error(f"Page not ready: {e}")
            return False
    
    # ==================== Tab Navigation Methods ====================
    
    def click_tab(self, tab_name: str) -> bool:
        """
        Click on a specific tab.
        
        Args:
            tab_name: One of 'Details', 'Test Script', 'Execution', 'Traceability',
                     'Attachments', 'Comments', 'History'
        
        Returns:
            bool: True if tab was clicked successfully
        """
        tab_locators = {
            'Details': self.DETAILS_TAB,
            'Test Script': self.TEST_SCRIPT_TAB,
            'Execution': self.EXECUTION_TAB,
            'Traceability': self.TRACEABILITY_TAB,
            'Attachments': self.ATTACHMENTS_TAB,
            'Comments': self.COMMENTS_TAB,
            'History': self.HISTORY_TAB
        }
        
        locator = tab_locators.get(tab_name)
        if not locator:
            self.logger.error(f"Invalid tab name: {tab_name}")
            return False
        
        try:
            self.click(locator)
            sleep(1)  # Wait for tab content to load
            self.logger.info(f"Clicked {tab_name} tab")
            return True
        except Exception as e:
            self.logger.error(f"Failed to click tab: {e}")
            return False
    
    def click_test_script_tab(self) -> bool:
        """Click on Test Script tab - convenience method."""
        return self.click_tab('Test Script')
    
    def get_active_tab_name(self) -> str:
        """Get the name of currently active tab."""
        try:
            element = self.find_element(self.ACTIVE_TAB)
            return self.get_text(self.ACTIVE_TAB).strip()
        except Exception:
            return ""
    
    # ==================== Test Script Type Methods ====================
    
    def get_current_script_type(self) -> str:
        """Get the currently selected script type (Plain Text, Step-by-Step, or BDD)."""
        try:
            button_text = self.get_text(self.SCRIPT_TYPE_DROPDOWN)
            # Extract type from "Type: Step-by-Step" format
            if ":" in button_text:
                return button_text.split(":", 1)[1].strip()
            return button_text.strip()
        except Exception:
            return ""
    
    def select_script_type(self, script_type: str) -> bool:
        """
        Select test script type.
        
        Args:
            script_type: One of 'Plain Text', 'Step-by-Step', or 'BDD'
        
        Returns:
            bool: True if type was selected successfully
        """
        type_locators = {
            'Plain Text': self.SCRIPT_TYPE_PLAIN_TEXT,
            'Step-by-Step': self.SCRIPT_TYPE_STEP_BY_STEP,
            'BDD': self.SCRIPT_TYPE_BDD
        }
        
        locator = type_locators.get(script_type)
        if not locator:
            self.logger.error(f"Invalid script type: {script_type}")
            return False
        
        try:
            # Open dropdown
            self.click(self.SCRIPT_TYPE_DROPDOWN)
            sleep(0.5)
            
            # Select type
            self.click(locator)
            sleep(1)
            
            self.logger.info(f"Selected script type: {script_type}")
            return True
        except Exception as e:
            self.logger.error(f"Failed to select script type: {e}")
            return False
    
    # ==================== Test Steps Methods (Step-by-Step Mode) ====================
    
    def get_steps_count(self) -> int:
        """Get the number of test steps currently added."""
        try:
            elements = self.find_elements(self.ALL_STEPS)
            return len(elements)
        except Exception:
            return 0
    
    def wait_for_steps_ready(self, timeout: int = 5) -> bool:
        """Wait for steps container to be ready."""
        try:
            self.find_element(self.STEPS_CONTAINER, timeout=timeout,
                            condition=WaitCondition.VISIBILITY_OF_ELEMENT_LOCATED)
            return True
        except Exception:
            return False
    
    def click_add_step_initial(self) -> bool:
        """Click the initial 'Add step' button (when no steps exist)."""
        try:
            self.click(self.ADD_STEP_BUTTON)
            sleep(1)
            self.logger.info("Clicked initial Add Step button")
            return True
        except Exception as e:
            self.logger.warning(f"Initial add step button not found: {e}")
            return False
    
    def get_step_description_editor(self, step_index: int) -> Optional[WebElement]:
        """Get the description editor element for a specific step."""
        selector = f"rich-text[name='stepDescription-{step_index}'] .ktm-editor-html-viewer[contenteditable='true']"
        locator = Locator(By.CSS_SELECTOR, selector)
        try:
            return self.find_element(locator, timeout=5)
        except Exception:
            return None
    
    def get_step_test_data_editor(self, step_index: int) -> Optional[WebElement]:
        """Get the test data editor element for a specific step."""
        selector = f"rich-text[name='stepTestData-{step_index}'] .ktm-editor-html-viewer[contenteditable='true']"
        locator = Locator(By.CSS_SELECTOR, selector)
        try:
            return self.find_element(locator, timeout=5)
        except Exception:
            return None
    
    def get_step_expected_result_editor(self, step_index: int) -> Optional[WebElement]:
        """Get the expected result editor element for a specific step."""
        selector = f"rich-text[name='stepExpectedResult-{step_index}'] .ktm-editor-html-viewer[contenteditable='true']"
        locator = Locator(By.CSS_SELECTOR, selector)
        try:
            return self.find_element(locator, timeout=5)
        except Exception:
            return None
    
    def enter_step_description(self, step_index: int, description: str, retries: int = 3) -> bool:
        """
        Enter description text for a specific step.
        
        Args:
            step_index: The step number (1-based index)
            description: The description text to enter
            retries: Number of retries for stale element handling
        
        Returns:
            bool: True if successful
        """
        for attempt in range(retries):
            try:
                # Refind element each time to avoid stale reference
                editor = self.get_step_description_editor(step_index)
                if not editor:
                    if attempt < retries - 1:
                        sleep(0.5)
                        continue
                    return False
                
                editor.click()
                sleep(0.3)
                editor.clear()
                editor.send_keys(description)
                self.logger.info(f"Entered description for step {step_index}")
                return True
            except Exception as e:
                if "stale element" in str(e).lower() and attempt < retries - 1:
                    self.logger.warning(f"Stale element, retrying... (attempt {attempt + 1}/{retries})")
                    sleep(0.5)
                    continue
                else:
                    self.logger.error(f"Failed to enter step description: {e}")
                    if attempt == retries - 1:
                        return False
        return False
    
    def enter_step_test_data(self, step_index: int, test_data: str, retries: int = 3) -> bool:
        """
        Enter test data for a specific step.
        
        Args:
            step_index: The step number (1-based index)
            test_data: The test data to enter
            retries: Number of retries for stale element handling
        
        Returns:
            bool: True if successful
        """
        for attempt in range(retries):
            try:
                # Refind element each time to avoid stale reference
                editor = self.get_step_test_data_editor(step_index)
                if not editor:
                    if attempt < retries - 1:
                        sleep(0.5)
                        continue
                    return False
                
                editor.click()
                sleep(0.3)
                editor.clear()
                editor.send_keys(test_data)
                self.logger.info(f"Entered test data for step {step_index}")
                return True
            except Exception as e:
                if "stale element" in str(e).lower() and attempt < retries - 1:
                    self.logger.warning(f"Stale element, retrying... (attempt {attempt + 1}/{retries})")
                    sleep(0.5)
                    continue
                else:
                    self.logger.error(f"Failed to enter test data: {e}")
                    if attempt == retries - 1:
                        return False
        return False
    
    def enter_step_expected_result(self, step_index: int, expected_result: str, 
                                   press_tab: bool = True, retries: int = 3) -> bool:
        """
        Enter expected result for a specific step.
        
        Args:
            step_index: The step number (1-based index)
            expected_result: The expected result text
            press_tab: If True, press TAB after entering to auto-generate next step
            retries: Number of retries for stale element handling
        
        Returns:
            bool: True if successful
        """
        for attempt in range(retries):
            try:
                # Refind element each time to avoid stale reference
                editor = self.get_step_expected_result_editor(step_index)
                if not editor:
                    if attempt < retries - 1:
                        sleep(0.5)
                        continue
                    return False
                
                editor.click()
                sleep(0.3)
                editor.clear()
                editor.send_keys(expected_result)
                
                if press_tab:
                    editor.send_keys(Keys.TAB)
                    sleep(1)  # Wait for new step to generate
                    self.logger.info(f"Entered expected result for step {step_index} and pressed TAB")
                else:
                    self.logger.info(f"Entered expected result for step {step_index}")
                
                return True
            except Exception as e:
                if "stale element" in str(e).lower() and attempt < retries - 1:
                    self.logger.warning(f"Stale element, retrying... (attempt {attempt + 1}/{retries})")
                    sleep(0.5)
                    continue
                else:
                    self.logger.error(f"Failed to enter expected result: {e}")
                    if attempt == retries - 1:
                        return False
        return False
    
    def add_test_step(self, description: str, test_data: str, expected_result: str,
                     auto_create_next: bool = True) -> bool:
        """
        Add a complete test step with all three fields.
        
        Args:
            description: Step description
            test_data: Test data for the step
            expected_result: Expected result
            auto_create_next: If True, press TAB to auto-generate next step row
        
        Returns:
            bool: True if successful
        """
        current_count = self.get_steps_count()
        step_index = current_count if current_count > 0 else 1
        
        # If no steps exist, click initial add button
        if current_count == 0:
            if not self.click_add_step_initial():
                self.logger.error("Failed to initialize first step")
                return False
            sleep(1)
            step_index = 1
        
        # Enter step data
        success = (
            self.enter_step_description(step_index, description) and
            self.enter_step_test_data(step_index, test_data) and
            self.enter_step_expected_result(step_index, expected_result, press_tab=auto_create_next)
        )
        
        if success:
            self.logger.info(f"Successfully added step {step_index}")
        
        return success
    
    def add_multiple_test_steps(self, steps: List[Dict[str, str]]) -> bool:
        """
        Add multiple test steps.
        
        Args:
            steps: List of step dictionaries with keys: 'description', 'test_data', 'expected_result'
        
        Returns:
            bool: True if all steps were added successfully
        """
        if not steps:
            return False
        
        for i, step_data in enumerate(steps):
            is_last_step = (i == len(steps) - 1)
            success = self.add_test_step(
                description=step_data.get('description', ''),
                test_data=step_data.get('test_data', ''),
                expected_result=step_data.get('expected_result', ''),
                auto_create_next=not is_last_step  # Don't create next for last step
            )
            
            if not success:
                self.logger.error(f"Failed to add step {i + 1}")
                return False
            
            sleep(0.5)  # Small delay between steps
        
        self.logger.info(f"Successfully added {len(steps)} steps")
        return True
    
    # ==================== Save and Action Methods ====================
    
    def click_save(self) -> bool:
        """Click the Save button."""
        try:
            self.click(self.SAVE_BUTTON)
            sleep(2)
            self.logger.info("Clicked Save button")
            return True
        except Exception as e:
            self.logger.error(f"Failed to click Save: {e}")
            return False
    
    def click_back(self) -> bool:
        """Click the Back button."""
        try:
            self.click(self.BACK_BUTTON)
            sleep(1)
            self.logger.info("Clicked Back button")
            return True
        except Exception as e:
            self.logger.error(f"Failed to click Back: {e}")
            return False
    
    def get_test_case_key(self) -> str:
        """Get the test case key from the page."""
        try:
            # Extract from breadcrumb or title
            breadcrumb_text = self.get_text(self.BREADCRUMB_CONTAINER)
            # Pattern: SDLC-T180 (1.0)
            import re
            match = re.search(r'([A-Z]+-T\d+)', breadcrumb_text)
            if match:
                return match.group(1)
            return ""
        except Exception:
            return ""
    
    def get_page_title(self) -> str:
        """Get the test case title from the page."""
        try:
            return self.get_text(self.PAGE_TITLE)
        except Exception:
            return ""
