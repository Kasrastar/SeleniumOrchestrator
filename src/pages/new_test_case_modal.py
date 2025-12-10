"""
New Test Case Modal Component Module

This module provides the NewTestCaseModal class for interacting with the
"Create Test Case" modal that appears when clicking the "New Test Case" button.

Design Pattern: Modal Component Pattern
- Modal is overlaid on the TestCasesPage
- Can be instantiated from TestCasesPage
- Provides methods to interact with modal elements and close it
"""

from typing import Optional, List
from time import sleep
import logging
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement

from ..core.ports import Locator, WaitCondition
from .base_page import BasePage
from ..infra.selenium_session import SeleniumSession


class NewTestCaseModal(BasePage):
    """
    Modal component for creating a new test case.
    
    This modal provides functionality for:
    - Entering test case name (required)
    - Adding objective and precondition (rich text)
    - Setting status, priority, component
    - Setting owner and estimated run time
    - Selecting folder location
    - Adding labels
    - Creating and optionally creating another
    
    The modal overlays the main page and can be closed or submitted.
    """
    
    # ==================== Modal Container Locators ====================
    
    MODAL_CONTAINER = Locator(By.CSS_SELECTOR, "[data-testid='create-entity-modal']")
    MODAL_HEADER = Locator(By.CSS_SELECTOR, "[data-testid='create-entity-modal--header']")
    MODAL_TITLE = Locator(By.CSS_SELECTOR, "[data-testid='create-entity-modal--header'] h2")
    MODAL_BODY = Locator(By.CSS_SELECTOR, "[data-testid='create-entity-modal--body']")
    MODAL_FOOTER = Locator(By.CSS_SELECTOR, "[data-testid='create-entity-modal--footer']")
    MODAL_FORM = Locator(By.CSS_SELECTOR, "#create-entity-modal-form")
    
    # Close button
    CLOSE_BUTTON = Locator(By.CSS_SELECTOR, "[data-testid='close-icon']")
    
    # ==================== Form Field Locators ====================
    
    # Name field (Required)
    NAME_LABEL = Locator(By.CSS_SELECTOR, "label#name-label")
    NAME_INPUT = Locator(By.CSS_SELECTOR, "input#name[data-testid='name-field']")
    NAME_FIELD_CONTAINER = Locator(By.CSS_SELECTOR, "[data-testid='name-field-container']")
    
    # Objective field (Rich Text Editor)
    OBJECTIVE_LABEL = Locator(By.CSS_SELECTOR, "label#objective-label")
    OBJECTIVE_EDITOR = Locator(By.CSS_SELECTOR, "[data-testid='richTextEditor-objective']")
    OBJECTIVE_EDITOR_CONTENT = Locator(By.CSS_SELECTOR, "[data-testid='richTextEditor-objective'] .fr-element")
    
    # Precondition field (Rich Text Editor)
    PRECONDITION_LABEL = Locator(By.CSS_SELECTOR, "label#precondition-label")
    PRECONDITION_EDITOR = Locator(By.CSS_SELECTOR, "[data-testid='richTextEditor-precondition']")
    PRECONDITION_EDITOR_CONTENT = Locator(By.CSS_SELECTOR, "[data-testid='richTextEditor-precondition'] .fr-element")
    
    # ==================== Details Section Locators ====================
    
    DETAILS_SECTION_HEADER = Locator(By.CSS_SELECTOR, ".css-bvt3e8 span")
    
    # Status dropdown
    STATUS_LABEL = Locator(By.CSS_SELECTOR, "label#statusId-label")
    STATUS_DROPDOWN = Locator(By.CSS_SELECTOR, "input#statusId")
    STATUS_SELECTED_VALUE = Locator(By.CSS_SELECTOR, "#react-select-12-live-region + span + div .zscale-select__single-value")
    
    # Component dropdown
    COMPONENT_LABEL = Locator(By.CSS_SELECTOR, "label#componentId-label")
    COMPONENT_DROPDOWN = Locator(By.CSS_SELECTOR, "input#componentId")
    COMPONENT_PLACEHOLDER = Locator(By.CSS_SELECTOR, "#react-select-13-placeholder")
    
    # Estimated run time
    ESTIMATED_TIME_LABEL = Locator(By.CSS_SELECTOR, "label#estimatedTime-label")
    ESTIMATED_TIME_INPUT = Locator(By.CSS_SELECTOR, "input#estimatedTime[data-testid='creation-modal-estimatedTime-field']")
    
    # Priority dropdown
    PRIORITY_LABEL = Locator(By.CSS_SELECTOR, "label#priorityId-label")
    PRIORITY_DROPDOWN = Locator(By.CSS_SELECTOR, "input#priorityId")
    PRIORITY_SELECTED_VALUE = Locator(By.CSS_SELECTOR, "#react-select-14-live-region + span + div .zscale-select__single-value")
    
    # Owner dropdown
    OWNER_LABEL = Locator(By.CSS_SELECTOR, "label#owner-label")
    OWNER_DROPDOWN = Locator(By.CSS_SELECTOR, "input#owner")
    OWNER_SELECTED_VALUE = Locator(By.CSS_SELECTOR, "#react-select-16-live-region + span + div .zscale-select__single-value")
    OWNER_CLEAR_BUTTON = Locator(By.CSS_SELECTOR, ".zscale-select__clear-indicator button")
    
    # Folder field
    FOLDER_LABEL = Locator(By.CSS_SELECTOR, "label#folderId-label")
    FOLDER_DISPLAY = Locator(By.CSS_SELECTOR, ".css-tq6cp8")
    FOLDER_CLEAR_BUTTON = Locator(By.CSS_SELECTOR, ".clear-text-field-icon")
    FOLDER_SELECT_BUTTON = Locator(By.CSS_SELECTOR, "button.eqkfmpc2")
    
    # Labels field
    LABELS_LABEL = Locator(By.CSS_SELECTOR, "label#labels-label")
    LABELS_INPUT = Locator(By.CSS_SELECTOR, "input#react-select-15-input")
    LABELS_PLACEHOLDER = Locator(By.CSS_SELECTOR, "#react-select-15-placeholder")
    
    # ==================== Rich Text Editor Toolbar Locators ====================
    
    # Objective editor toolbar
    OBJECTIVE_BOLD_BUTTON = Locator(By.CSS_SELECTOR, "[data-testid='richTextEditor-objective'] button[data-cmd='bold']")
    OBJECTIVE_ITALIC_BUTTON = Locator(By.CSS_SELECTOR, "[data-testid='richTextEditor-objective'] button[data-cmd='italic']")
    OBJECTIVE_UNDERLINE_BUTTON = Locator(By.CSS_SELECTOR, "[data-testid='richTextEditor-objective'] button[data-cmd='underline']")
    OBJECTIVE_INSERT_LINK_BUTTON = Locator(By.CSS_SELECTOR, "[data-testid='richTextEditor-objective'] button[data-cmd='insertLink']")
    
    # Precondition editor toolbar
    PRECONDITION_BOLD_BUTTON = Locator(By.CSS_SELECTOR, "[data-testid='richTextEditor-precondition'] button[data-cmd='bold']")
    PRECONDITION_ITALIC_BUTTON = Locator(By.CSS_SELECTOR, "[data-testid='richTextEditor-precondition'] button[data-cmd='italic']")
    
    # ==================== Footer Locators ====================
    
    CREATE_ANOTHER_CHECKBOX = Locator(By.CSS_SELECTOR, "input#createAnotherEntity-uid381")
    CREATE_ANOTHER_LABEL = Locator(By.CSS_SELECTOR, "label[id*='createAnotherEntity']")
    
    CANCEL_BUTTON = Locator(By.CSS_SELECTOR, "button[data-testid='creation-modal-cancel-button']")
    CREATE_BUTTON = Locator(By.CSS_SELECTOR, "button[data-testid='creation-modal-create-button']")
    CREATE_DROPDOWN_BUTTON = Locator(By.CSS_SELECTOR, "button[data-testid='creation-modal-footer-dropdown']")
    
    # Dropdown menu options (appears when clicking dropdown arrow)
    CREATE_AND_EDIT_OPTION = Locator(By.XPATH, "//a[contains(text(), 'Create and Edit')]")
    
    def __init__(self, session: SeleniumSession):
        """
        Initialize the NewTestCaseModal.
        
        Args:
            session (SeleniumSession): The Selenium session to use
        """
        super().__init__(session)
        self.url = ""  # Modal doesn't have its own URL
        self.logger = logging.getLogger(f"{__name__}.{self.__class__.__name__}")
    
    # ==================== Modal State Methods ====================
    
    def is_modal_visible(self) -> bool:
        """
        Check if the modal is visible.
        
        Returns:
            bool: True if modal is displayed, False otherwise
        """
        return self.is_visible(self.MODAL_CONTAINER)
    
    def wait_for_modal_visible(self, timeout: int = 10) -> bool:
        """
        Wait for the modal to become visible.
        
        Args:
            timeout (int): Maximum time to wait in seconds
            
        Returns:
            bool: True if modal is visible within timeout
        """
        try:
            self.find_element(
                self.MODAL_CONTAINER,
                timeout=timeout,
                condition=WaitCondition.VISIBILITY_OF_ELEMENT_LOCATED
            )
            return True
        except Exception:
            return False
    
    def wait_for_modal_closed(self, timeout: int = 10) -> bool:
        """
        Wait for the modal to close.
        
        Args:
            timeout (int): Maximum time to wait in seconds
            
        Returns:
            bool: True if modal is closed within timeout
        """
        try:
            # Wait for modal to become invisible by checking if it's no longer present
            from selenium.webdriver.support.ui import WebDriverWait
            from selenium.webdriver.support import expected_conditions as EC
            
            WebDriverWait(self.session.driver, timeout).until_not(
                EC.presence_of_element_located((self.MODAL_CONTAINER.by, self.MODAL_CONTAINER.value))
            )
            return True
        except Exception:
            return False
    
    def get_modal_title(self) -> str:
        """
        Get the modal title text.
        
        Returns:
            str: The modal title (e.g., "Create Test Case")
        """
        element = self.find_element(self.MODAL_TITLE, condition=WaitCondition.VISIBILITY_OF_ELEMENT_LOCATED)
        return element.text if element else ""
    
    # ==================== Close Modal Methods ====================
    
    def click_close_button(self) -> None:
        """Close the modal using the X button."""
        self.click(self.CLOSE_BUTTON)
    
    def click_cancel(self) -> None:
        """Cancel and close the modal."""
        self.click(self.CANCEL_BUTTON)
    
    # ==================== Name Field Methods ====================
    
    def enter_name(self, name: str) -> None:
        """
        Enter the test case name (required field).
        
        Args:
            name (str): The test case name
        """
        self.clear_and_type(self.NAME_INPUT, name)
    
    def clear_name(self) -> None:
        """Clear the name field."""
        self.clear(self.NAME_INPUT)
    
    def get_name(self) -> str:
        """
        Get the current value of the name field.
        
        Returns:
            str: The name field value
        """
        return self.get_text(self.NAME_INPUT)
    
    # ==================== Objective Field Methods ====================
    
    def enter_objective(self, text: str) -> None:
        """
        Enter text in the objective rich text editor.
        
        Args:
            text (str): The objective text to enter
        """
        self.clear_and_type(self.OBJECTIVE_EDITOR_CONTENT, text)
    
    def clear_objective(self) -> None:
        """Clear the objective field."""
        self.clear(self.OBJECTIVE_EDITOR_CONTENT)
    
    def click_objective_bold(self) -> None:
        """Click the Bold button in objective editor."""
        self.click(self.OBJECTIVE_BOLD_BUTTON)
    
    def click_objective_italic(self) -> None:
        """Click the Italic button in objective editor."""
        self.click(self.OBJECTIVE_ITALIC_BUTTON)
    
    # ==================== Precondition Field Methods ====================
    
    def enter_precondition(self, text: str) -> None:
        """
        Enter text in the precondition rich text editor.
        
        Args:
            text (str): The precondition text to enter
        """
        self.clear_and_type(self.PRECONDITION_EDITOR_CONTENT, text)
    
    def clear_precondition(self) -> None:
        """Clear the precondition field."""
        self.clear(self.PRECONDITION_EDITOR_CONTENT)
    
    # ==================== Status Field Methods ====================
    
    def click_status_dropdown(self) -> None:
        """Click to open the status dropdown."""
        self.click(self.STATUS_DROPDOWN)
    
    def get_selected_status(self) -> str:
        """
        Get the currently selected status.
        
        Returns:
            str: The selected status (e.g., "Draft")
        """
        element = self.find_element(self.STATUS_SELECTED_VALUE, condition=WaitCondition.VISIBILITY_OF_ELEMENT_LOCATED)
        return element.text if element else ""
    
    def select_status(self, status: str) -> None:
        """
        Select a status from the dropdown.
        
        Args:
            status (str): The status to select (e.g., "Draft", "Approved")
        """
        self.click_status_dropdown()
        sleep(0.5)  # Wait for dropdown to open
        status_option = Locator("xpath", f"//div[text()='{status}']")
        self.click(status_option)
    
    # ==================== Component Field Methods ====================
    
    def click_component_dropdown(self) -> None:
        """Click to open the component dropdown."""
        self.click(self.COMPONENT_DROPDOWN)
    
    def select_component(self, component: str) -> None:
        """
        Select a component from the dropdown.
        
        Args:
            component (str): The component to select
        """
        self.click_component_dropdown()
        sleep(0.5)
        component_option = Locator("xpath", f"//div[text()='{component}']")
        self.click(component_option)
    
    # ==================== Estimated Time Field Methods ====================
    
    def enter_estimated_time(self, time: str) -> None:
        """
        Enter estimated run time in hh:mm format.
        
        Args:
            time (str): Time in hh:mm format (e.g., "01:30")
        """
        self.clear_and_type(self.ESTIMATED_TIME_INPUT, time)
    
    def clear_estimated_time(self) -> None:
        """Clear the estimated time field."""
        self.clear(self.ESTIMATED_TIME_INPUT)
    
    # ==================== Priority Field Methods ====================
    
    def click_priority_dropdown(self) -> None:
        """Click to open the priority dropdown."""
        self.click(self.PRIORITY_DROPDOWN)
    
    def get_selected_priority(self) -> str:
        """
        Get the currently selected priority.
        
        Returns:
            str: The selected priority (e.g., "Normal")
        """
        element = self.find_element(self.PRIORITY_SELECTED_VALUE, condition=WaitCondition.VISIBILITY_OF_ELEMENT_LOCATED)
        return element.text if element else ""
    
    def select_priority(self, priority: str) -> None:
        """
        Select a priority from the dropdown.
        
        Args:
            priority (str): The priority to select (e.g., "High", "Normal", "Low")
        """
        self.click_priority_dropdown()
        sleep(0.5)
        priority_option = Locator("xpath", f"//span[text()='{priority}']")
        self.click(priority_option)
    
    # ==================== Owner Field Methods ====================
    
    def click_owner_dropdown(self) -> None:
        """Click to open the owner dropdown."""
        self.click(self.OWNER_DROPDOWN)
    
    def get_selected_owner(self) -> str:
        """
        Get the currently selected owner.
        
        Returns:
            str: The selected owner name
        """
        element = self.find_element(self.OWNER_SELECTED_VALUE, condition=WaitCondition.VISIBILITY_OF_ELEMENT_LOCATED)
        if element:
            name_span = element.find_element("css selector", ".css-1gz2b5f")
            return name_span.text if name_span else ""
        return ""
    
    def clear_owner(self) -> None:
        """Clear the owner selection."""
        self.click(self.OWNER_CLEAR_BUTTON)
    
    def select_owner(self, owner_name: str) -> None:
        """
        Select an owner from the dropdown.
        
        Args:
            owner_name (str): The owner name to select
        """
        self.click_owner_dropdown()
        sleep(0.5)
        owner_option = Locator("xpath", f"//span[@title='{owner_name}']")
        self.click(owner_option)
    
    # ==================== Folder Field Methods ====================
    
    def get_selected_folder(self) -> str:
        """
        Get the currently selected folder path.
        
        Returns:
            str: The folder path (e.g., "/K45-library/dealer/aaa/login")
        """
        element = self.find_element(self.FOLDER_DISPLAY, condition=WaitCondition.VISIBILITY_OF_ELEMENT_LOCATED)
        return element.text if element else ""
    
    def click_folder_select(self) -> None:
        """Click to open folder selection dialog."""
        self.click(self.FOLDER_SELECT_BUTTON)
    
    def clear_folder(self) -> None:
        """Clear the folder selection."""
        self.click(self.FOLDER_CLEAR_BUTTON)
    
    # ==================== Labels Field Methods ====================
    
    def click_labels_dropdown(self) -> None:
        """Click to open the labels dropdown."""
        self.click(self.LABELS_INPUT)
    
    def add_label(self, label: str) -> None:
        """
        Add a label to the test case.
        
        Args:
            label (str): The label to add
        """
        self.clear_and_type(self.LABELS_INPUT, label)
        self.press_enter(self.LABELS_INPUT)
    
    # ==================== Footer Methods ====================
    
    def check_create_another(self) -> None:
        """Check the 'Create another test case' checkbox."""
        element = self.find_element(self.CREATE_ANOTHER_CHECKBOX, condition=WaitCondition.ELEMENT_TO_BE_CLICKABLE)
        if element and not element.is_selected():
            self.click(self.CREATE_ANOTHER_LABEL)
    
    def uncheck_create_another(self) -> None:
        """Uncheck the 'Create another test case' checkbox."""
        element = self.find_element(self.CREATE_ANOTHER_CHECKBOX, condition=WaitCondition.ELEMENT_TO_BE_CLICKABLE)
        if element and element.is_selected():
            self.click(self.CREATE_ANOTHER_LABEL)
    
    def is_create_another_checked(self) -> bool:
        """
        Check if 'Create another test case' is checked.
        
        Returns:
            bool: True if checked, False otherwise
        """
        element = self.find_element(self.CREATE_ANOTHER_CHECKBOX, condition=WaitCondition.PRESENCE_OF_ELEMENT_LOCATED)
        return element.is_selected() if element else False
    
    def click_create(self) -> None:
        """Click the Create button to submit the form."""
        self.click(self.CREATE_BUTTON)
    
    def click_create_dropdown(self) -> None:
        """Click the dropdown arrow next to Create button."""
        self.click(self.CREATE_DROPDOWN_BUTTON)
    
    def click_create_and_edit(self) -> bool:
        """
        Click the "Create and Edit" option from the dropdown menu.
        This will create the test case and navigate to the test case detail page.
        
        Returns:
            bool: True if option was clicked successfully
        """
        try:
            # First verify modal is still visible
            if not self.is_modal_visible():
                self.logger.error("Modal is not visible before clicking dropdown")
                return False
            
            # Click dropdown button to reveal options
            self.logger.info("Clicking dropdown button to reveal Create options...")
            dropdown_btn = self.find_element(
                self.CREATE_DROPDOWN_BUTTON,
                timeout=5,
                condition=WaitCondition.ELEMENT_TO_BE_CLICKABLE
            )
            if dropdown_btn:
                self.logger.info(f"Found dropdown button: {dropdown_btn.tag_name}, visible: {dropdown_btn.is_displayed()}")
                dropdown_btn.click()
                self.logger.info("Dropdown button clicked")
            else:
                self.logger.error("Could not find dropdown button")
                return False
            
            # Wait for dropdown menu to appear
            self.logger.info("Waiting for dropdown menu to appear...")
            sleep(2.0)  # Give dropdown time to animate and render
            
            # Check for dropdown menu container
            try:
                dropdown_containers = self.session.driver.find_elements(By.XPATH, "//div[contains(@class, 'aui-dropdown2') or contains(@id, 'submit-menu')]")
                self.logger.info(f"Found {len(dropdown_containers)} dropdown containers")
                for container in dropdown_containers:
                    if container.is_displayed():
                        self.logger.info(f"Visible dropdown container: {container.get_attribute('class')}, id: {container.get_attribute('id')}")
                        self.logger.info(f"Container HTML: {container.get_attribute('outerHTML')[:200]}")
            except Exception as e:
                self.logger.error(f"Error checking dropdown containers: {e}")
            
            # Try multiple locator strategies to find "Create and Edit" option
            self.logger.info("Looking for 'Create and Edit' option...")
            
            locators_to_try = [
                Locator(By.XPATH, "//a[contains(text(), 'Create and Edit')]"),
                Locator(By.XPATH, "//a[text()='Create and Edit']"),
                Locator(By.XPATH, "//div[@id='createTestCase-submit-menu']//a[contains(text(), 'Create and Edit')]"),
                Locator(By.XPATH, "//div[contains(@class, 'aui-dropdown2')]//a[contains(text(), 'Create and Edit')]"),
                Locator(By.XPATH, "//li[@class='menu-item']//a[contains(text(), 'Create and Edit')]"),
                Locator(By.LINK_TEXT, "Create and Edit"),
                Locator(By.PARTIAL_LINK_TEXT, "Create and Edit"),
            ]
            
            edit_option = None
            for idx, locator in enumerate(locators_to_try):
                try:
                    self.logger.info(f"Trying locator strategy {idx + 1}: {locator.by}, {locator.value}")
                    edit_option = self.find_element(
                        locator,
                        timeout=2,
                        condition=WaitCondition.PRESENCE_OF_ELEMENT_LOCATED
                    )
                    if edit_option and edit_option.is_displayed():
                        self.logger.info(f"Found visible element with strategy {idx + 1}")
                        break
                    elif edit_option:
                        self.logger.info(f"Found element but not visible with strategy {idx + 1}")
                        edit_option = None
                except Exception as e:
                    self.logger.debug(f"Strategy {idx + 1} failed: {e}")
                    continue
            
            if edit_option:
                self.logger.info("Found 'Create and Edit' option, clicking...")
                # Try clicking with JavaScript as fallback
                try:
                    edit_option.click()
                except Exception as e:
                    self.logger.warning(f"Regular click failed, trying JavaScript click: {e}")
                    self.session.driver.execute_script("arguments[0].click();", edit_option)
                self.logger.info("Successfully clicked Create and Edit option")
                return True
            else:
                self.logger.error("Could not find 'Create and Edit' option with any strategy")
                # Try to get all links in dropdown for debugging
                try:
                    all_dropdown_links = self.session.driver.find_elements(By.XPATH, "//div[contains(@class, 'aui-dropdown2')]//a | //div[contains(@id, 'menu')]//a")
                    self.logger.error(f"Links in dropdown areas: {[link.text for link in all_dropdown_links if link.is_displayed()]}")
                except:
                    pass
                return False
                
        except Exception as e:
            self.logger.error(f"Failed to click Create and Edit: {e}")
            import traceback
            self.logger.error(traceback.format_exc())
            return False
    
    # ==================== Verification Methods ====================
    
    def is_name_field_empty(self) -> bool:
        """
        Check if the name field is empty.
        
        Returns:
            bool: True if empty, False otherwise
        """
        value = self.get_name()
        return value == "" or value is None
    
    def wait_for_modal_ready(self, timeout: int = 10) -> bool:
        """
        Wait for the modal to be fully loaded and ready.
        
        Args:
            timeout (int): Maximum time to wait in seconds
            
        Returns:
            bool: True if modal is ready, False otherwise
        """
        try:
            self.wait_for_modal_visible(timeout)
            self.find_element(
                self.NAME_INPUT,
                timeout=timeout,
                condition=WaitCondition.ELEMENT_TO_BE_CLICKABLE
            )
            self.find_element(
                self.CREATE_BUTTON,
                timeout=timeout,
                condition=WaitCondition.ELEMENT_TO_BE_CLICKABLE
            )
            return True
        except Exception:
            return False
    
    # ==================== Complete Form Methods ====================
    
    def create_test_case(
        self,
        name: str,
        objective: str = None,
        precondition: str = None,
        status: str = None,
        priority: str = None,
        estimated_time: str = None,
        create_another: bool = False
    ) -> None:
        """
        Complete convenience method to create a test case with all common fields.
        
        Args:
            name (str): Test case name (required)
            objective (str, optional): Test objective
            precondition (str, optional): Test precondition
            status (str, optional): Status to select
            priority (str, optional): Priority to select
            estimated_time (str, optional): Estimated time in hh:mm format
            create_another (bool, optional): Whether to check 'Create another'
        """
        # Enter required name
        self.enter_name(name)
        
        # Enter optional fields
        if objective:
            self.enter_objective(objective)
        
        if precondition:
            self.enter_precondition(precondition)
        
        if status:
            self.select_status(status)
        
        if priority:
            self.select_priority(priority)
        
        if estimated_time:
            self.enter_estimated_time(estimated_time)
        
        # Handle create another checkbox
        if create_another:
            self.check_create_another()
        else:
            self.uncheck_create_another()
        
        # Submit form
        self.click_create()
