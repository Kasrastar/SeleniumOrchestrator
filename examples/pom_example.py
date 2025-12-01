"""
Example: Using Page Object Model (POM) with SeleniumOrchestrator

This example demonstrates how to use the Page Object Model pattern
with SeleniumOrchestrator for cleaner, more maintainable test code.

The POM pattern separates page-specific code from test logic, making
tests more readable and easier to maintain.
"""

from src.application.profile_service import ProfileService
from src.infra.browser_config_builder import BrowserConfigBuilder
from src.infra.selenium_session import SeleniumSession
from src.pages.login_page import LoginPage
from src.pages.home_page import HomePage
from src.utils.logger import logger


def test_login_with_pom():
    """
    Example: Login test using Page Object Model.
    
    This demonstrates the clean separation between test logic
    and page implementation details.
    """
    
    # Setup: Initialize browser session
    chrome_connections = {
        'browser_type': 'chrome',
        'binary_path': '/path/to/chromedriver'  # Update with your driver path
    }
    
    options = BrowserConfigBuilder('chrome').set_no_sandbox().disable_dev_shm_usage().build()
    session = SeleniumSession()
    profile_service = ProfileService()
    
    profile = profile_service.new_profile(
        driver_name='test_driver',
        tab_name='main_tab',
        session=session,
        profile_options=options,
        connection=chrome_connections
    )
    
    try:
        # Create page objects
        login_page = LoginPage(profile.session, base_url="https://example.com")
        home_page = HomePage(profile.session, base_url="https://example.com")
        
        # Test steps using page objects
        logger.info("Starting login test with POM")
        
        # Navigate to login page
        login_page.navigate()
        logger.info("Navigated to login page")
        
        # Verify page loaded
        assert login_page.wait_for_page_load(), "Login page did not load"
        logger.info("Login page loaded successfully")
        
        # Perform login
        login_page.login(username="testuser", password="testpass123", remember_me=True)
        logger.info("Submitted login credentials")
        
        # Verify login success
        if login_page.is_logged_in():
            logger.info("Login successful!")
            
            # Verify home page loaded
            assert home_page.wait_for_page_load(), "Home page did not load"
            logger.info(f"Welcome message: {home_page.get_welcome_message()}")
            
            # Check featured items
            item_count = home_page.get_featured_item_count()
            logger.info(f"Found {item_count} featured items")
            
            if item_count > 0:
                items = home_page.get_all_item_details()
                for idx, item in enumerate(items):
                    logger.info(f"Item {idx + 1}: {item['title']} - {item['price']}")
        else:
            error_msg = login_page.get_error_message()
            logger.error(f"Login failed: {error_msg}")
            
    except Exception as e:
        logger.error(f"Test failed with error: {str(e)}", exc_info=True)
    finally:
        # Cleanup
        profile.close()
        logger.info("Browser closed")


def test_search_with_pom():
    """
    Example: Search functionality test using Page Object Model.
    """
    
    # Setup
    chrome_connections = {
        'browser_type': 'chrome',
        'binary_path': '/path/to/chromedriver'
    }
    
    options = BrowserConfigBuilder('chrome').set_headless().build()
    session = SeleniumSession()
    profile_service = ProfileService()
    
    profile = profile_service.new_profile(
        driver_name='search_test',
        tab_name='search_tab',
        session=session,
        profile_options=options,
        connection=chrome_connections
    )
    
    try:
        # Create page object
        home_page = HomePage(profile.session, base_url="https://example.com")
        
        logger.info("Starting search test with POM")
        
        # Navigate to home page
        home_page.navigate()
        logger.info("Navigated to home page")
        
        # Verify search is available
        assert home_page.is_search_available(), "Search functionality not available"
        
        # Perform search
        search_query = "laptop"
        home_page.search(search_query)
        logger.info(f"Searched for: {search_query}")
        
        # Verify results
        if home_page.has_featured_items():
            items = home_page.get_all_item_details()
            matching_items = [
                item for item in items 
                if search_query.lower() in item['title'].lower()
            ]
            logger.info(f"Found {len(matching_items)} matching items")
        else:
            logger.warning("No search results found")
            
    except Exception as e:
        logger.error(f"Search test failed: {str(e)}", exc_info=True)
    finally:
        profile.close()
        logger.info("Browser closed")


def test_add_to_cart_with_pom():
    """
    Example: Add to cart test using Page Object Model.
    """
    
    # Setup
    firefox_connections = {
        'browser_type': 'firefox',
        'binary_path': '/usr/bin/geckodriver'
    }
    
    options = BrowserConfigBuilder('firefox').set_fullscreen().build()
    session = SeleniumSession()
    profile_service = ProfileService()
    
    profile = profile_service.new_profile(
        driver_name='cart_test',
        tab_name='cart_tab',
        session=session,
        profile_options=options,
        connection=firefox_connections
    )
    
    try:
        # Create page object
        home_page = HomePage(profile.session, base_url="https://example.com")
        
        logger.info("Starting add to cart test with POM")
        
        # Navigate and wait for page load
        home_page.navigate()
        home_page.wait_for_page_load()
        logger.info("Home page loaded")
        
        # Add first item to cart
        if home_page.has_featured_items():
            home_page.add_item_to_cart(item_index=0)
            logger.info("Added first item to cart")
            
            # Or add by title
            home_page.add_item_to_cart_by_title("Premium Laptop")
            logger.info("Added item by title to cart")
        else:
            logger.warning("No items available to add to cart")
            
    except Exception as e:
        logger.error(f"Add to cart test failed: {str(e)}", exc_info=True)
    finally:
        profile.close()
        logger.info("Browser closed")


def test_navigation_with_pom():
    """
    Example: Navigation test using Page Object Model.
    """
    
    # Setup
    remote_connections = {
        'browser_type': 'remote',
        'remote_url': 'http://localhost:4444/wd/hub',
    }
    
    options = BrowserConfigBuilder('chrome').build()
    session = SeleniumSession()
    profile_service = ProfileService()
    
    profile = profile_service.new_profile(
        driver_name='nav_test',
        tab_name='nav_tab',
        session=session,
        profile_options=options,
        connection=remote_connections
    )
    
    try:
        # Create page object
        home_page = HomePage(profile.session, base_url="https://example.com")
        
        logger.info("Starting navigation test with POM")
        
        # Navigate to home
        home_page.navigate()
        home_page.wait_for_page_load()
        logger.info(f"Current URL: {home_page.get_current_url()}")
        
        # Navigate through menu
        home_page.navigate_to_products()
        logger.info("Navigated to Products page")
        
        home_page.navigate_to_about()
        logger.info("Navigated to About page")
        
        # Go back
        home_page.go_back()
        logger.info("Went back to previous page")
        
        # Take screenshot
        home_page.take_screenshot("/tmp/navigation_test.png")
        logger.info("Screenshot saved")
        
    except Exception as e:
        logger.error(f"Navigation test failed: {str(e)}", exc_info=True)
    finally:
        profile.close()
        logger.info("Browser closed")


if __name__ == "__main__":
    """
    Run the examples.
    
    Note: Update the driver paths and URLs before running.
    """
    
    print("=" * 60)
    print("SeleniumOrchestrator - Page Object Model Examples")
    print("=" * 60)
    print()
    
    # Uncomment the test you want to run:
    
    # test_login_with_pom()
    # test_search_with_pom()
    # test_add_to_cart_with_pom()
    # test_navigation_with_pom()
    
    print()
    print("Update driver paths and uncomment test functions to run examples")
