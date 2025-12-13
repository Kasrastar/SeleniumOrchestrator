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

    def __init__(self, session: SeleniumSession, base_url: Optional[str] = "https://jira.inside45.ir", test_case_key: Optional[str] = None):
        super().__init__(session)
        self.base_url = base_url    
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
    
    def wait_for_step_count(self, expected_count: int, timeout: int = 5) -> bool:
        """Wait for the steps count to reach the expected number.
        
        Args:
            expected_count: Expected number of steps
            timeout: Maximum time to wait in seconds
        
        Returns:
            bool: True if count reached, False if timeout
        """
        from time import time
        start_time = time()
        while time() - start_time < timeout:
            current_count = self.get_steps_count()
            if current_count >= expected_count:
                self.logger.info(f"Step count reached {current_count}")
                return True
            sleep(0.3)
        
        self.logger.warning(f"Timeout waiting for step count to reach {expected_count}")
        return False
    
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
            element = self.find_element(locator, timeout=5, condition=WaitCondition.VISIBILITY_OF_ELEMENT_LOCATED)
            return element
        except Exception as e:
            self.logger.warning(f"Could not find step {step_index} description editor: {e}")
            return None
    
    def get_step_test_data_editor(self, step_index: int) -> Optional[WebElement]:
        """Get the test data editor element for a specific step."""
        selector = f"rich-text[name='stepTestData-{step_index}'] .ktm-editor-html-viewer[contenteditable='true']"
        locator = Locator(By.CSS_SELECTOR, selector)
        try:
            element = self.find_element(locator, timeout=5, condition=WaitCondition.VISIBILITY_OF_ELEMENT_LOCATED)
            return element
        except Exception as e:
            self.logger.warning(f"Could not find step {step_index} test data editor: {e}")
            return None
    
    def get_step_expected_result_editor(self, step_index: int) -> Optional[WebElement]:
        """Get the expected result editor element for a specific step."""
        selector = f"rich-text[name='stepExpectedResult-{step_index}'] .ktm-editor-html-viewer[contenteditable='true']"
        locator = Locator(By.CSS_SELECTOR, selector)
        try:
            element = self.find_element(locator, timeout=5, condition=WaitCondition.VISIBILITY_OF_ELEMENT_LOCATED)
            return element
        except Exception as e:
            self.logger.warning(f"Could not find step {step_index} expected result editor: {e}")
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

        # sleep(2)

        for attempt in range(retries):
            try:
                self.logger.info(f"Attempt {attempt + 1}/{retries} to enter description for step {step_index}")
                
                # Get and click placeholder to activate the editor
                placeholder = self.get_step_description_editor(step_index)
                if not placeholder:
                    if attempt < retries - 1:
                        self.logger.warning(f"Placeholder not found, retrying...")
                        sleep(1)
                        continue
                    self.logger.error(f"Could not find placeholder editor for step {step_index}")
                    return False
                
                self.logger.info(f"Clicking placeholder for step {step_index}")
                placeholder.click()
                sleep(2)  # Wait for Angular/Froala to activate
                
                # Find the activated Froala editor - try multiple selectors
                selectors = [
                    f"rich-text[name='stepDescription-{step_index}'] .fr-wrapper .fr-element.fr-view[contenteditable='true']",
                    f"rich-text[name='stepDescription-{step_index}'] .fr-element.fr-view[contenteditable='true']",
                    f"rich-text[name='stepDescription-{step_index}'] div[contenteditable='true'].fr-element"
                ]
                
                activated_editor = None
                for selector in selectors:
                    try:
                        activated_locator = Locator(By.CSS_SELECTOR, selector)
                        activated_editor = self.find_element(activated_locator, timeout=2)
                        if activated_editor:
                            self.logger.info(f"Found activated editor with selector: {selector}")
                            break
                    except Exception:
                        continue
                
                if not activated_editor:
                    raise Exception("Could not find activated editor with any selector")
                
                # Click on the activated editor to ensure it has focus
                self.logger.info(f"Clicking activated editor to ensure focus")
                activated_editor.click()
                sleep(0.3)
                
                # Send keys to activated editor
                self.logger.info(f"Sending keys to step {step_index} description: {description[:30]}...")
                activated_editor.send_keys(description)
                sleep(0.3)  # Give time for keys to register
                
                self.logger.info(f"Successfully entered description for step {step_index}")
                return True
                
            except Exception as e:
                self.logger.error(f"Error on attempt {attempt + 1}: {str(e)}")
                if attempt < retries - 1:
                    self.logger.warning(f"Retrying in 1 second...")
                    sleep(1)
                    continue
                else:
                    self.logger.error(f"Failed to enter step description after {retries} attempts")
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
                self.logger.info(f"Attempt {attempt + 1}/{retries} to enter test data for step {step_index}")
                
                # Get and click placeholder to activate the editor
                placeholder = self.get_step_test_data_editor(step_index)
                if not placeholder:
                    if attempt < retries - 1:
                        self.logger.warning(f"Placeholder not found, retrying...")
                        sleep(1)
                        continue
                    self.logger.error(f"Could not find placeholder editor for step {step_index}")
                    return False
                
                self.logger.info(f"Clicking placeholder for step {step_index}")
                placeholder.click()
                sleep(0.7)  # Wait for Angular/Froala to activate
                
                # Find the activated Froala editor - try multiple selectors
                selectors = [
                    f"rich-text[name='stepTestData-{step_index}'] .fr-wrapper .fr-element.fr-view[contenteditable='true']",
                    f"rich-text[name='stepTestData-{step_index}'] .fr-element.fr-view[contenteditable='true']",
                    f"rich-text[name='stepTestData-{step_index}'] div[contenteditable='true'].fr-element"
                ]
                
                activated_editor = None
                for selector in selectors:
                    try:
                        activated_locator = Locator(By.CSS_SELECTOR, selector)
                        activated_editor = self.find_element(activated_locator, timeout=2)
                        if activated_editor:
                            self.logger.info(f"Found activated editor with selector: {selector}")
                            break
                    except Exception:
                        continue
                
                if not activated_editor:
                    raise Exception("Could not find activated editor with any selector")
                
                # Click on the activated editor to ensure it has focus
                self.logger.info(f"Clicking activated editor to ensure focus")
                activated_editor.click()
                sleep(0.3)
                
                # Send keys to activated editor
                self.logger.info(f"Sending keys to step {step_index} test data: {test_data[:30]}...")
                activated_editor.send_keys(test_data)
                sleep(0.3)  # Give time for keys to register
                
                self.logger.info(f"Successfully entered test data for step {step_index}")
                return True
                
            except Exception as e:
                self.logger.error(f"Error on attempt {attempt + 1}: {str(e)}")
                if attempt < retries - 1:
                    self.logger.warning(f"Retrying in 1 second...")
                    sleep(1)
                    continue
                else:
                    self.logger.error(f"Failed to enter test data after {retries} attempts")
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
                self.logger.info(f"Attempt {attempt + 1}/{retries} to enter expected result for step {step_index}")
                
                # Get and click placeholder to activate the editor
                placeholder = self.get_step_expected_result_editor(step_index)
                if not placeholder:
                    if attempt < retries - 1:
                        self.logger.warning(f"Placeholder not found, retrying...")
                        sleep(1)
                        continue
                    self.logger.error(f"Could not find placeholder editor for step {step_index}")
                    return False
                
                self.logger.info(f"Clicking placeholder for step {step_index}")
                placeholder.click()
                sleep(0.7)  # Wait for Angular/Froala to activate
                
                # Find the activated Froala editor - try multiple selectors
                selectors = [
                    f"rich-text[name='stepExpectedResult-{step_index}'] .fr-wrapper .fr-element.fr-view[contenteditable='true']",
                    f"rich-text[name='stepExpectedResult-{step_index}'] .fr-element.fr-view[contenteditable='true']",
                    f"rich-text[name='stepExpectedResult-{step_index}'] div[contenteditable='true'].fr-element"
                ]
                
                activated_editor = None
                for selector in selectors:
                    try:
                        activated_locator = Locator(By.CSS_SELECTOR, selector)
                        activated_editor = self.find_element(activated_locator, timeout=2)
                        if activated_editor:
                            self.logger.info(f"Found activated editor with selector: {selector}")
                            break
                    except Exception:
                        continue
                
                if not activated_editor:
                    raise Exception("Could not find activated editor with any selector")
                
                # Click on the activated editor to ensure it has focus
                self.logger.info(f"Clicking activated editor to ensure focus")
                activated_editor.click()
                sleep(0.3)
                
                # Send keys to activated editor
                self.logger.info(f"Sending keys to step {step_index} expected result: {expected_result[:30]}...")
                activated_editor.send_keys(expected_result)
                sleep(0.3)  # Give time for keys to register
                
                if press_tab:
                    self.logger.info(f"Pressing TAB to create next step")
                    activated_editor.send_keys(Keys.TAB)
                    sleep(1.5)  # Wait longer for new step to generate
                    self.logger.info(f"Successfully entered expected result for step {step_index} and pressed TAB")
                else:
                    self.logger.info(f"Successfully entered expected result for step {step_index}")
                
                return True
                
            except Exception as e:
                self.logger.error(f"Error on attempt {attempt + 1}: {str(e)}")
                if attempt < retries - 1:
                    self.logger.warning(f"Retrying in 1 second...")
                    sleep(1)
                    continue
                else:
                    self.logger.error(f"Failed to enter expected result after {retries} attempts")
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
        
        # If no steps exist, click initial add button to create first step
        if current_count == 0:
            if not self.click_add_step_initial():
                self.logger.error("Failed to initialize first step")
                return False
            sleep(1)
            step_index = 1
        else:
            # Fill the last (newest) step - when TAB creates a new step, it becomes the last one
            step_index = current_count
        
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
            
            # For steps after the first, wait for the new step to be created by the previous TAB press
            if i > 0:
                expected_count = i + 1  # After filling step i, we expect i+1 steps to exist
                if not self.wait_for_step_count(expected_count, timeout=3):
                    self.logger.error(f"Step {expected_count} was not created after TAB")
                    return False
                sleep(0.5)  # Additional stabilization time
                
                # Fix: After TAB creates a new row, the description field is auto-focused.
                # Click on the expected_result field (without entering data) to deactivate 
                # the description field, allowing the code to work properly.
                current_count = self.get_steps_count()
                self.logger.info(f"Deactivating auto-focused description field by clicking expected result")
                try:
                    expected_result_placeholder = self.get_step_expected_result_editor(current_count)
                    if expected_result_placeholder:
                        expected_result_placeholder.click()
                        sleep(0.3)  # Brief pause to let the focus change
                        self.logger.info(f"Successfully deactivated description field for step {current_count}")
                except Exception as e:
                    self.logger.warning(f"Could not click expected result to deactivate description: {e}")
            
            # Get current count to determine which step index to fill
            current_count = self.get_steps_count()
            self.logger.info(f"Processing step {i+1}/{len(steps)}, current step count: {current_count}")
            
            success = self.add_test_step(
                description=step_data.get('description', ''),
                test_data=step_data.get('test_data', ''),
                expected_result=step_data.get('expected_result', ''),
                auto_create_next=not is_last_step  # Don't create next for last step
            )
            
            if not success:
                self.logger.error(f"Failed to add step {i + 1}")
                return False
        
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
