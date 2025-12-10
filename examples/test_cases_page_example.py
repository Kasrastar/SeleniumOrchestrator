"""
Test Cases Page Usage Examples

This script demonstrates how to use the TestCasesPage and NewTestCaseModal
page objects to interact with the Jira Zephyr Scale Test Cases Library.

Examples include:
1. Basic navigation and page verification
2. Folder tree navigation
3. Creating new test cases using the modal
4. Searching and filtering test cases
5. Advanced folder operations
"""

from src.infra.selenium_session import SeleniumSession
from src.infra.browser_factory import BrowserFactory
from src.infra.browser_config_builder import BrowserConfigBuilder
from src.pages.test_cases_page import TestCasesPage
from src.pages.new_test_case_modal import NewTestCaseModal


def example_1_basic_navigation():
    """
    Example 1: Navigate to Test Cases page and verify page load.
    """
    print("\n=== Example 1: Basic Navigation ===")
    
    # Create browser configuration
    config = BrowserConfigBuilder().set_browser_type("chrome").set_headless(False).build()
    
    # Create session
    session = SeleniumSession(BrowserFactory())
    session.start(config)
    
    try:
        # Initialize page object with project ID
        test_cases_page = TestCasesPage(session, project_id="10200")
        
        # Navigate to test cases page
        test_cases_page.navigate()
        print("✓ Navigated to Test Cases page")
        
        # Wait for page to be ready
        if test_cases_page.wait_for_page_ready(timeout=15):
            print("✓ Test Cases page is ready")
        
        # Verify Test Cases tab is active
        if test_cases_page.is_test_cases_tab_active():
            print("✓ Test Cases tab is active")
        
        # Get project name
        project_name = test_cases_page.get_current_project_name()
        print(f"✓ Current project: {project_name}")
        
        # Get all test cases count
        count = test_cases_page.get_all_test_cases_count()
        print(f"✓ Total test cases: {count}")
        
    finally:
        session.quit()


def example_2_folder_navigation():
    """
    Example 2: Navigate through folder tree and view folder contents.
    """
    print("\n=== Example 2: Folder Navigation ===")
    
    config = BrowserConfigBuilder().set_browser_type("chrome").set_headless(False).build()
    session = SeleniumSession(BrowserFactory())
    session.start(config)
    
    try:
        test_cases_page = TestCasesPage(session, project_id="10200")
        test_cases_page.navigate()
        test_cases_page.wait_for_page_ready()
        
        # Wait for folder tree to load
        if test_cases_page.wait_for_folder_tree_loaded():
            print("✓ Folder tree loaded")
        
        # Click on root folder
        test_cases_page.click_all_test_cases_folder()
        print("✓ Clicked 'All test cases' folder")
        
        # Click on specific folder by name
        test_cases_page.click_folder_by_name("Login")
        print("✓ Clicked 'Login' folder")
        
        # Get folder count
        login_count = test_cases_page.get_folder_count("2")  # ID 2 is Login folder
        print(f"✓ Login folder test cases: {login_count}")
        
        # Navigate to nested folder path
        test_cases_page.navigate_to_folder_path("/K45-library/dealer/aaa/login")
        print("✓ Navigated to nested folder path")
        
        # Get selected folder name
        selected_folder = test_cases_page.get_selected_folder_name()
        print(f"✓ Currently selected folder: {selected_folder}")
        
        # Get all visible folders
        folders = test_cases_page.get_all_visible_folders()
        print(f"✓ Found {len(folders)} visible folders")
        for folder in folders[:5]:  # Show first 5
            print(f"  - {folder['name']} {folder['count'] or ''}")
        
    finally:
        session.quit()


def example_3_create_test_case_simple():
    """
    Example 3: Create a simple test case with required fields only.
    """
    print("\n=== Example 3: Create Simple Test Case ===")
    
    config = BrowserConfigBuilder().set_browser_type("chrome").set_headless(False).build()
    session = SeleniumSession(BrowserFactory())
    session.start(config)
    
    try:
        test_cases_page = TestCasesPage(session, project_id="10200")
        test_cases_page.navigate()
        test_cases_page.wait_for_page_ready()
        
        # Click New Test Case button to open modal
        modal = test_cases_page.click_new_test_case()
        print("✓ Clicked 'New Test Case' button")
        
        # Wait for modal to be visible
        if modal.wait_for_modal_visible(timeout=10):
            print("✓ Modal is visible")
        
        # Verify modal title
        title = modal.get_modal_title()
        print(f"✓ Modal title: {title}")
        
        # Enter test case name (required)
        modal.enter_name("Verify Login with Valid Credentials")
        print("✓ Entered test case name")
        
        # Click Create button
        modal.click_create()
        print("✓ Clicked Create button")
        
        # Wait for modal to close
        if modal.wait_for_modal_closed(timeout=10):
            print("✓ Modal closed - Test case created successfully")
        
    finally:
        session.quit()


def example_4_create_test_case_complete():
    """
    Example 4: Create a complete test case with all fields populated.
    """
    print("\n=== Example 4: Create Complete Test Case ===")
    
    config = BrowserConfigBuilder().set_browser_type("chrome").set_headless(False).build()
    session = SeleniumSession(BrowserFactory())
    session.start(config)
    
    try:
        test_cases_page = TestCasesPage(session, project_id="10200")
        test_cases_page.navigate()
        test_cases_page.wait_for_page_ready()
        
        # Navigate to specific folder first
        test_cases_page.click_folder_by_name("Login")
        print("✓ Selected 'Login' folder")
        
        # Open modal
        modal = test_cases_page.click_new_test_case()
        modal.wait_for_modal_ready()
        print("✓ Modal is ready")
        
        # Use the convenience method to fill all fields
        modal.create_test_case(
            name="Verify Password Reset Functionality",
            objective="Verify that users can successfully reset their password using email verification",
            precondition="User account exists with registered email address",
            status="Draft",
            priority="High",
            estimated_time="00:15",
            create_another=False
        )
        print("✓ Filled all test case fields")
        print("✓ Submitted test case creation")
        
        # Wait for modal to close
        if modal.wait_for_modal_closed(timeout=10):
            print("✓ Test case created successfully")
        
    finally:
        session.quit()


def example_5_create_multiple_test_cases():
    """
    Example 5: Create multiple test cases using 'Create another' checkbox.
    """
    print("\n=== Example 5: Create Multiple Test Cases ===")
    
    config = BrowserConfigBuilder().set_browser_type("chrome").set_headless(False).build()
    session = SeleniumSession(BrowserFactory())
    session.start(config)
    
    try:
        test_cases_page = TestCasesPage(session, project_id="10200")
        test_cases_page.navigate()
        test_cases_page.wait_for_page_ready()
        
        # Select folder
        test_cases_page.click_folder_by_name("Registration")
        print("✓ Selected 'Registration' folder")
        
        # Define test cases to create
        test_cases = [
            {
                "name": "Verify Registration with Valid Data",
                "objective": "Ensure user can register with all valid information",
                "priority": "High"
            },
            {
                "name": "Verify Email Validation on Registration",
                "objective": "Test email format validation during registration",
                "priority": "Normal"
            },
            {
                "name": "Verify Password Strength Requirements",
                "objective": "Test password complexity validation",
                "priority": "High"
            }
        ]
        
        for idx, test_case in enumerate(test_cases):
            is_last = (idx == len(test_cases) - 1)
            
            # Open modal (first time only)
            if idx == 0:
                modal = test_cases_page.click_new_test_case()
                modal.wait_for_modal_ready()
            
            # Fill fields
            modal.enter_name(test_case["name"])
            modal.enter_objective(test_case["objective"])
            modal.select_priority(test_case["priority"])
            
            # Check 'Create another' for all except last
            if not is_last:
                modal.check_create_another()
                print(f"✓ Creating test case {idx + 1}/{len(test_cases)}: {test_case['name']}")
            else:
                modal.uncheck_create_another()
                print(f"✓ Creating final test case: {test_case['name']}")
            
            # Submit
            modal.click_create()
            
            # If not last, modal should reopen
            if not is_last:
                modal.wait_for_modal_ready()
                # Clear fields for next iteration
                modal.clear_name()
                modal.clear_objective()
        
        # Wait for final modal close
        if modal.wait_for_modal_closed(timeout=10):
            print(f"✓ Successfully created {len(test_cases)} test cases")
        
    finally:
        session.quit()


def example_6_search_and_filter():
    """
    Example 6: Search for test cases and use filters.
    """
    print("\n=== Example 6: Search and Filter ===")
    
    config = BrowserConfigBuilder().set_browser_type("chrome").set_headless(False).build()
    session = SeleniumSession(BrowserFactory())
    session.start(config)
    
    try:
        test_cases_page = TestCasesPage(session, project_id="10200")
        test_cases_page.navigate()
        test_cases_page.wait_for_page_ready()
        
        # Perform search
        test_cases_page.enter_search_text("login")
        print("✓ Entered search text: 'login'")
        
        # Wait for search results
        test_cases_page.wait(2)
        
        # Clear search
        test_cases_page.clear_search()
        print("✓ Cleared search")
        
        # Click filters button
        test_cases_page.click_filters()
        print("✓ Opened filters panel")
        
    finally:
        session.quit()


def example_7_modal_field_operations():
    """
    Example 7: Demonstrate various modal field operations.
    """
    print("\n=== Example 7: Modal Field Operations ===")
    
    config = BrowserConfigBuilder().set_browser_type("chrome").set_headless(False).build()
    session = SeleniumSession(BrowserFactory())
    session.start(config)
    
    try:
        test_cases_page = TestCasesPage(session, project_id="10200")
        test_cases_page.navigate()
        test_cases_page.wait_for_page_ready()
        
        # Open modal
        modal = test_cases_page.click_new_test_case()
        modal.wait_for_modal_ready()
        print("✓ Modal opened")
        
        # Get current folder
        folder = modal.get_selected_folder()
        print(f"✓ Current folder: {folder}")
        
        # Get default status
        status = modal.get_selected_status()
        print(f"✓ Default status: {status}")
        
        # Get default priority
        priority = modal.get_selected_priority()
        print(f"✓ Default priority: {priority}")
        
        # Get default owner
        owner = modal.get_selected_owner()
        print(f"✓ Default owner: {owner}")
        
        # Modify fields
        modal.enter_name("Test Case with All Details")
        modal.enter_objective("Comprehensive test objective")
        modal.enter_precondition("Required preconditions")
        
        # Use rich text editor formatting
        modal.click_objective_bold()
        print("✓ Applied bold formatting to objective")
        
        # Set estimated time
        modal.enter_estimated_time("01:30")
        print("✓ Set estimated time to 1 hour 30 minutes")
        
        # Change status
        modal.select_status("Approved")
        print("✓ Changed status to 'Approved'")
        
        # Verify name is not empty
        if not modal.is_name_field_empty():
            print("✓ Name field is populated")
        
        # Cancel without creating
        modal.click_cancel()
        print("✓ Cancelled modal")
        
        if modal.wait_for_modal_closed():
            print("✓ Modal closed successfully")
        
    finally:
        session.quit()


def example_8_archived_test_cases():
    """
    Example 8: View archived test cases.
    """
    print("\n=== Example 8: Archived Test Cases ===")
    
    config = BrowserConfigBuilder().set_browser_type("chrome").set_headless(False).build()
    session = SeleniumSession(BrowserFactory())
    session.start(config)
    
    try:
        test_cases_page = TestCasesPage(session, project_id="10200")
        test_cases_page.navigate()
        test_cases_page.wait_for_page_ready()
        
        # Click archived test cases
        test_cases_page.click_archived_test_cases()
        print("✓ Viewing archived test cases")
        
        # Wait for content to update
        test_cases_page.wait(2)
        
    finally:
        session.quit()


def example_9_empty_state_handling():
    """
    Example 9: Handle empty state when no test cases exist in a folder.
    """
    print("\n=== Example 9: Empty State Handling ===")
    
    config = BrowserConfigBuilder().set_browser_type("chrome").set_headless(False).build()
    session = SeleniumSession(BrowserFactory())
    session.start(config)
    
    try:
        test_cases_page = TestCasesPage(session, project_id="10200")
        test_cases_page.navigate()
        test_cases_page.wait_for_page_ready()
        
        # Check if empty state is displayed
        if test_cases_page.is_empty_state_displayed():
            print("✓ Empty state detected")
            
            # Get empty state message
            message = test_cases_page.get_empty_state_message()
            print(f"✓ Empty state message: {message}")
            
            # Create test case via empty state link
            modal = test_cases_page.click_empty_state_create_link()
            print("✓ Opened modal from empty state")
            
            # Close modal
            modal.click_close_button()
            modal.wait_for_modal_closed()
        else:
            print("✓ Folder contains test cases")
        
    finally:
        session.quit()


def example_10_complete_workflow():
    """
    Example 10: Complete workflow - Navigate, create test case, verify.
    """
    print("\n=== Example 10: Complete Workflow ===")
    
    config = BrowserConfigBuilder().set_browser_type("chrome").set_headless(False).build()
    session = SeleniumSession(BrowserFactory())
    session.start(config)
    
    try:
        # Step 1: Navigate to page
        test_cases_page = TestCasesPage(session, project_id="10200")
        test_cases_page.navigate()
        test_cases_page.wait_for_page_ready()
        print("✓ Step 1: Navigated to Test Cases page")
        
        # Step 2: Select target folder
        test_cases_page.click_folder_by_name("Login")
        test_cases_page.wait(1)
        initial_count = test_cases_page.get_folder_count("2")
        print(f"✓ Step 2: Selected Login folder (current count: {initial_count})")
        
        # Step 3: Open new test case modal
        modal = test_cases_page.click_new_test_case()
        modal.wait_for_modal_ready()
        print("✓ Step 3: Opened New Test Case modal")
        
        # Step 4: Fill test case details
        test_case_name = "Verify Login Error Messages"
        modal.create_test_case(
            name=test_case_name,
            objective="Verify that appropriate error messages are displayed for invalid login attempts",
            precondition="Application is accessible and login page is displayed",
            status="Draft",
            priority="Normal",
            estimated_time="00:20"
        )
        print(f"✓ Step 4: Created test case '{test_case_name}'")
        
        # Step 5: Wait for creation to complete
        if modal.wait_for_modal_closed(timeout=10):
            print("✓ Step 5: Test case created successfully")
        
        # Step 6: Verify test case appears in folder (optional - refresh if needed)
        test_cases_page.wait(2)
        print("✓ Step 6: Workflow completed successfully")
        
    finally:
        session.quit()


if __name__ == "__main__":
    """
    Run examples.
    
    Uncomment the example you want to run.
    Note: These examples require actual login to Jira system.
    """
    
    print("Test Cases Page - Usage Examples")
    print("=" * 50)
    
    # Uncomment the example you want to run:
    
    # example_1_basic_navigation()
    # example_2_folder_navigation()
    # example_3_create_test_case_simple()
    # example_4_create_test_case_complete()
    # example_5_create_multiple_test_cases()
    # example_6_search_and_filter()
    # example_7_modal_field_operations()
    # example_8_archived_test_cases()
    # example_9_empty_state_handling()
    example_10_complete_workflow()
    
    print("\n" + "=" * 50)
    print("Example execution completed!")
