"""
Example: Using JiraLoginPage with Jira Inside45

This example demonstrates how to use the JiraLoginPage class to automate
login to the Jira instance at https://jira.inside45.ir

Features demonstrated:
1. Initialize Jira login page
2. Navigate to login page
3. Perform login with credentials
4. Verify login page elements
5. Handle login errors with screenshots
6. Toggle password visibility
7. Use remember me functionality
"""

from src.infra.browser_factory import BrowserFactory
from src.infra.browser_config_builder import BrowserConfigBuilder
from src.infra.selenium_session import SeleniumSession
from src.pages.jira_login_page import JiraLoginPage
from src.utils.logger import get_logger

logger = get_logger(__name__)


def example_basic_jira_login():
    """
    Example 1: Basic Jira login workflow
    
    This demonstrates the simplest way to login to Jira.
    """
    logger.info("=== Example 1: Basic Jira Login ===")
    
    # Configure browser (Chrome in this example)
    config = (BrowserConfigBuilder()
              .set_browser_type("chrome")
              .set_headless(False)  # Set to True for headless mode
              .set_window_size(1920, 1080)
              .build())
    
    # Create browser and session
    factory = BrowserFactory()
    driver = factory.create_driver(config)
    session = SeleniumSession(driver)
    
    try:
        # Initialize Jira login page
        jira_login = JiraLoginPage(session, base_url="https://jira.inside45.ir")
        
        # Navigate to login page
        logger.info("Navigating to Jira login page...")
        jira_login.navigate()
        
        # Wait for page to be ready
        jira_login.wait_for_page_ready()
        logger.info(f"Login page loaded. Title: {jira_login.get_page_title()}")
        
        # Enter credentials (replace with actual credentials)
        logger.info("Entering credentials...")
        jira_login.enter_username("your_username")
        jira_login.enter_password("your_password")
        
        # Click login button
        logger.info("Clicking login button...")
        jira_login.click_login_button()
        
        # Wait for login to complete
        if jira_login.wait_for_login_completion(timeout=15):
            logger.info("✓ Login successful!")
            logger.info(f"Current URL: {session.get_current_url()}")
        else:
            error_msg = jira_login.get_error_message()
            logger.error(f"✗ Login failed: {error_msg}")
            jira_login.take_screenshot_on_error("basic_login_failure")
        
    except Exception as e:
        logger.error(f"Error during login: {e}")
        jira_login.take_screenshot_on_error("basic_login_exception")
    finally:
        # Clean up
        session.quit()
        logger.info("Browser closed")


def example_jira_login_with_remember_me():
    """
    Example 2: Jira login with 'Remember me' checkbox
    
    This demonstrates using the remember me functionality.
    """
    logger.info("=== Example 2: Jira Login with Remember Me ===")
    
    # Configure browser
    config = (BrowserConfigBuilder()
              .set_browser_type("chrome")
              .set_headless(False)
              .build())
    
    # Create browser and session
    factory = BrowserFactory()
    driver = factory.create_driver(config)
    session = SeleniumSession(driver)
    
    try:
        # Initialize Jira login page
        jira_login = JiraLoginPage(session)
        jira_login.navigate()
        jira_login.wait_for_page_ready()
        
        # Use the composite login method with remember_me option
        logger.info("Logging in with 'Remember me' enabled...")
        jira_login.login(
            username="your_username",
            password="your_password",
            remember_me=True
        )
        
        # Verify remember me is checked
        if jira_login.is_remember_me_checked():
            logger.info("✓ Remember me checkbox is checked")
        
        # Wait for login completion
        if jira_login.is_login_successful(timeout=15):
            logger.info("✓ Login successful with Remember Me!")
        else:
            logger.error("✗ Login failed")
        
    except Exception as e:
        logger.error(f"Error: {e}")
    finally:
        session.quit()


def example_jira_login_with_screenshot():
    """
    Example 3: Jira login with automatic screenshot on failure
    
    This demonstrates error handling with screenshots.
    """
    logger.info("=== Example 3: Jira Login with Screenshot on Failure ===")
    
    # Configure browser
    config = (BrowserConfigBuilder()
              .set_browser_type("chrome")
              .set_headless(False)
              .build())
    
    # Create browser and session
    factory = BrowserFactory()
    driver = factory.create_driver(config)
    session = SeleniumSession(driver)
    
    try:
        # Initialize Jira login page
        jira_login = JiraLoginPage(session)
        jira_login.navigate()
        
        # Use login_with_screenshot method
        # This automatically takes a screenshot if login fails
        logger.info("Attempting login with auto-screenshot...")
        success, error_msg = jira_login.login_with_screenshot(
            username="your_username",
            password="your_password",
            remember_me=False
        )
        
        if success:
            logger.info("✓ Login successful!")
        else:
            logger.error(f"✗ Login failed: {error_msg}")
            logger.info("Screenshot saved for debugging")
        
    except Exception as e:
        logger.error(f"Error: {e}")
    finally:
        session.quit()


def example_verify_jira_page_elements():
    """
    Example 4: Verify all Jira login page elements
    
    This demonstrates element verification and page inspection.
    """
    logger.info("=== Example 4: Verify Jira Login Page Elements ===")
    
    # Configure browser
    config = (BrowserConfigBuilder()
              .set_browser_type("chrome")
              .set_headless(False)
              .build())
    
    # Create browser and session
    factory = BrowserFactory()
    driver = factory.create_driver(config)
    session = SeleniumSession(driver)
    
    try:
        # Initialize Jira login page
        jira_login = JiraLoginPage(session)
        jira_login.navigate()
        jira_login.wait_for_page_ready()
        
        # Get Jira version
        version = jira_login.get_jira_version()
        logger.info(f"Jira Version: {version}")
        
        # Get login header text
        header_text = jira_login.get_login_header_text()
        logger.info(f"Login Header: {header_text}")
        
        # Verify all page elements
        logger.info("Verifying page elements...")
        elements = jira_login.verify_login_page_elements()
        
        for element_name, is_present in elements.items():
            status = "✓" if is_present else "✗"
            logger.info(f"{status} {element_name}: {is_present}")
        
        # Check if all critical elements are present
        critical_elements = ["login_form", "username_field", "password_field", "login_button"]
        all_present = all(elements.get(elem, False) for elem in critical_elements)
        
        if all_present:
            logger.info("✓ All critical elements are present!")
        else:
            logger.warning("✗ Some critical elements are missing")
        
        # Check field requirements
        logger.info(f"Username field required: {jira_login.is_username_field_required()}")
        logger.info(f"Password field required: {jira_login.is_password_field_required()}")
        
    except Exception as e:
        logger.error(f"Error: {e}")
    finally:
        session.quit()


def example_toggle_password_visibility():
    """
    Example 5: Toggle password visibility
    
    This demonstrates the password show/hide functionality.
    """
    logger.info("=== Example 5: Toggle Password Visibility ===")
    
    # Configure browser
    config = (BrowserConfigBuilder()
              .set_browser_type("chrome")
              .set_headless(False)
              .build())
    
    # Create browser and session
    factory = BrowserFactory()
    driver = factory.create_driver(config)
    session = SeleniumSession(driver)
    
    try:
        # Initialize Jira login page
        jira_login = JiraLoginPage(session)
        jira_login.navigate()
        jira_login.wait_for_page_ready()
        
        # Enter password
        logger.info("Entering password...")
        jira_login.enter_password("test_password_123")
        
        # Check initial state (should be hidden)
        is_visible = jira_login.is_password_visible()
        logger.info(f"Password initially visible: {is_visible}")
        
        # Toggle to show password
        logger.info("Toggling password visibility to SHOW...")
        jira_login.click_toggle_password_visibility()
        session.sleep(1)  # Brief pause to see the change
        
        is_visible = jira_login.is_password_visible()
        logger.info(f"Password now visible: {is_visible}")
        
        # Toggle back to hide password
        logger.info("Toggling password visibility to HIDE...")
        jira_login.click_toggle_password_visibility()
        session.sleep(1)
        
        is_visible = jira_login.is_password_visible()
        logger.info(f"Password now visible: {is_visible}")
        
    except Exception as e:
        logger.error(f"Error: {e}")
    finally:
        session.quit()


def example_alternative_login_submit():
    """
    Example 6: Login by pressing Enter key
    
    This demonstrates submitting the form using Enter key instead of clicking.
    """
    logger.info("=== Example 6: Login with Enter Key ===")
    
    # Configure browser
    config = (BrowserConfigBuilder()
              .set_browser_type("chrome")
              .set_headless(False)
              .build())
    
    # Create browser and session
    factory = BrowserFactory()
    driver = factory.create_driver(config)
    session = SeleniumSession(driver)
    
    try:
        # Initialize Jira login page
        jira_login = JiraLoginPage(session)
        jira_login.navigate()
        jira_login.wait_for_page_ready()
        
        # Enter credentials
        logger.info("Entering credentials...")
        jira_login.enter_username("your_username")
        jira_login.enter_password("your_password")
        
        # Submit by pressing Enter instead of clicking login button
        logger.info("Submitting form with Enter key...")
        jira_login.submit_form_by_enter_key()
        
        # Check login result
        if jira_login.is_login_successful(timeout=15):
            logger.info("✓ Login successful using Enter key!")
        else:
            logger.error("✗ Login failed")
        
    except Exception as e:
        logger.error(f"Error: {e}")
    finally:
        session.quit()


def example_check_already_logged_in():
    """
    Example 7: Check if already logged in
    
    This demonstrates checking login state before attempting login.
    """
    logger.info("=== Example 7: Check if Already Logged In ===")
    
    # Configure browser
    config = (BrowserConfigBuilder()
              .set_browser_type("chrome")
              .set_headless(False)
              .build())
    
    # Create browser and session
    factory = BrowserFactory()
    driver = factory.create_driver(config)
    session = SeleniumSession(driver)
    
    try:
        # Initialize Jira login page
        jira_login = JiraLoginPage(session)
        jira_login.navigate()
        
        # Check if already logged in
        if jira_login.is_logged_in_already():
            logger.info("✓ Already logged in! Skipping login process.")
        else:
            logger.info("Not logged in. Proceeding with login...")
            jira_login.quick_login("your_username", "your_password")
            
            if jira_login.is_login_successful():
                logger.info("✓ Login successful!")
            else:
                logger.error("✗ Login failed")
        
    except Exception as e:
        logger.error(f"Error: {e}")
    finally:
        session.quit()


if __name__ == "__main__":
    """
    Run the examples.
    
    Note: Replace 'your_username' and 'your_password' with actual credentials
    before running these examples.
    
    Uncomment the example you want to run:
    """
    
    # Example 1: Basic login
    # example_basic_jira_login()
    
    # Example 2: Login with remember me
    # example_jira_login_with_remember_me()
    
    # Example 3: Login with auto-screenshot on failure
    # example_jira_login_with_screenshot()
    
    # Example 4: Verify page elements
    example_verify_jira_page_elements()
    
    # Example 5: Toggle password visibility
    # example_toggle_password_visibility()
    
    # Example 6: Submit with Enter key
    # example_alternative_login_submit()
    
    # Example 7: Check if already logged in
    # example_check_already_logged_in()
