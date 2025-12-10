"""
Example: Create Test Case with "Create and Edit" and Add Test Script

This example demonstrates:
1. Login to Jira
2. Navigate to Test Cases page
3. Create a new test case using "Create and Edit" option
4. Navigate to Test Script tab
5. Select "Step-by-Step" script type
6. Add multiple test steps with automatic row generation using TAB key
7. Save the test case

The "Create and Edit" button allows you to immediately edit the test case after creation,
which is useful for adding test scripts.
"""

from time import sleep
from chromedriver_py import binary_path

from src.application.profile_service import ProfileService
from src.infra.browser_config_builder import BrowserConfigBuilder
from src.infra.selenium_session import SeleniumSession
from src.utils.logger import logger
from src.pages.jira_login_page import JiraLoginPage
from src.pages.test_cases_page import TestCasesPage
from src.pages.new_test_case_modal import NewTestCaseModal
from src.pages.test_case_detail_page import TestCaseDetailPage


# Setup Chrome driver
chrome_connections = {
    'browser_type': 'chrome',
    'binary_path': binary_path
}

options = BrowserConfigBuilder('chrome')\
    .set_no_sandbox()\
    .disable_dev_shm_usage()\
    .set_browser_profile('./profiles/test_profile')\
    .build()

session = SeleniumSession()
profile_service = ProfileService()

new_profile = profile_service.new_profile(
    driver_name='test_driver',
    tab_name='initial_tab',
    session=session,
    profile_options=options,
    connection=chrome_connections
)

url = 'https://jira.inside45.ir'

try:
    # ==================== Step 1: Login ====================
    logger.info('=== Step 1: Login to Jira ===')
    jira_login_page = JiraLoginPage(new_profile.session, base_url=url)
    jira_login_page.navigate()
    logger.info('Navigated to login page')
    
    jira_login_page.wait_for_page_ready()
    jira_login_page.login(username='your_username', password='your_password')
    logger.info('Login submitted')
    sleep(3)
    
    # ==================== Step 2: Navigate to Test Cases ====================
    logger.info('=== Step 2: Navigate to Test Cases Page ===')
    test_cases_page = TestCasesPage(new_profile.session, project_id="10200")
    test_cases_page.navigate()
    logger.info('Navigated to Test Cases page')
    sleep(5)
    
    # Select target folder
    logger.info('=== Step 3: Select Target Folder ===')
    if test_cases_page.wait_for_folder_tree_loaded(timeout=10):
        logger.info('Folder tree loaded')
    
    test_cases_page.click_folder_by_name("Login")
    logger.info('Selected "Login" folder')
    sleep(2)
    
    # ==================== Step 4: Create Test Case ====================
    logger.info('=== Step 4: Create New Test Case ===')
    modal = test_cases_page.click_new_test_case()
    logger.info('Opened New Test Case modal')
    
    if modal.wait_for_modal_visible(timeout=10):
        logger.info('Modal is visible')
    
    if modal.wait_for_modal_ready(timeout=10):
        logger.info('Modal is ready')
    
    # Fill test case details
    logger.info('=== Step 5: Fill Test Case Details ===')
    test_name = "Verify User Login with Valid Credentials"
    test_objective = "Ensure that users can successfully login with valid username and password"
    test_precondition = "1. User is on login page\n2. Valid credentials are available\n3. System is accessible"
    
    modal.enter_name(test_name)
    logger.info(f'Entered name: {test_name}')
    
    modal.enter_objective(test_objective)
    logger.info('Entered objective')
    
    modal.enter_precondition(test_precondition)
    logger.info('Entered precondition')
    
    modal.select_priority("High")
    logger.info('Selected priority: High')
    
    modal.enter_estimated_time("00:10")
    logger.info('Set estimated time: 10 minutes')
    
    # ==================== Step 6: Create and Edit ====================
    logger.info('=== Step 6: Click Create and Edit ===')
    if modal.click_create_and_edit():
        logger.info('Clicked "Create and Edit" - navigating to detail page')
        sleep(3)  # Wait for navigation
    else:
        logger.error('Failed to click Create and Edit')
        raise Exception('Could not click Create and Edit')
    
    # ==================== Step 7: Open Test Script Tab ====================
    logger.info('=== Step 7: Navigate to Test Script Tab ===')
    detail_page = TestCaseDetailPage(new_profile.session)
    
    if detail_page.wait_for_page_ready(timeout=10):
        logger.info('Detail page is ready')
    
    # Get test case key
    test_key = detail_page.get_test_case_key()
    logger.info(f'Test case created: {test_key}')
    
    # Click Test Script tab
    if detail_page.click_test_script_tab():
        logger.info('Navigated to Test Script tab')
        sleep(2)
    
    # ==================== Step 8: Select Script Type ====================
    logger.info('=== Step 8: Select Script Type ===')
    current_type = detail_page.get_current_script_type()
    logger.info(f'Current script type: {current_type}')
    
    if current_type != "Step-by-Step":
        if detail_page.select_script_type("Step-by-Step"):
            logger.info('Selected Step-by-Step script type')
            sleep(1)
    else:
        logger.info('Already in Step-by-Step mode')
    
    # ==================== Step 9: Add Test Steps ====================
    logger.info('=== Step 9: Add Test Steps ===')
    
    # Define test steps
    test_steps = [
        {
            'description': 'Navigate to login page',
            'test_data': 'URL: https://example.com/login',
            'expected_result': 'Login page is displayed with username and password fields'
        },
        {
            'description': 'Enter valid username',
            'test_data': 'Username: testuser@example.com',
            'expected_result': 'Username is entered in the username field'
        },
        {
            'description': 'Enter valid password',
            'test_data': 'Password: ValidPass123!',
            'expected_result': 'Password is masked and entered in the password field'
        },
        {
            'description': 'Click Login button',
            'test_data': 'N/A',
            'expected_result': 'User is logged in and redirected to dashboard'
        },
        {
            'description': 'Verify user is logged in',
            'test_data': 'N/A',
            'expected_result': 'Username is displayed in header and logout option is available'
        }
    ]
    
    if detail_page.add_multiple_test_steps(test_steps):
        logger.info(f'Successfully added {len(test_steps)} test steps')
    else:
        logger.error('Failed to add test steps')
    
    # ==================== Step 10: Save ====================
    logger.info('=== Step 10: Save Test Case ===')
    sleep(2)
    
    if detail_page.click_save():
        logger.info('✓ Test case saved successfully!')
        sleep(2)
    else:
        logger.warning('Save button click may have failed')
    
    # ==================== Step 11: Verification ====================
    logger.info('=== Step 11: Verification ===')
    steps_count = detail_page.get_steps_count()
    logger.info(f'Total steps added: {steps_count}')
    
    page_title = detail_page.get_page_title()
    logger.info(f'Test case title: {page_title}')
    
    logger.info('=' * 60)
    logger.info('✓ WORKFLOW COMPLETED SUCCESSFULLY!')
    logger.info(f'Test Case: {test_key}')
    logger.info(f'Title: {test_name}')
    logger.info(f'Steps: {steps_count}')
    logger.info('=' * 60)
    
    # Keep browser open for manual inspection
    logger.info('Browser will remain open for 10 seconds for inspection...')
    sleep(10)

except Exception as e:
    logger.error(f'Error occurred: {e}')
    import traceback
    traceback.print_exc()
    sleep(5)

finally:
    logger.info('=== Script execution completed ===')
