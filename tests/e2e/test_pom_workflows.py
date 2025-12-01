"""
End-to-End Tests using Page Object Model

These tests demonstrate full user workflows using the POM pattern.
They can be run against real browsers (marked with browser tags).

Note: Update driver paths in test_data before running these tests.
"""

import pytest
from selenium.webdriver.common.by import By
from src.infra.browser_config_builder import BrowserConfigBuilder
from src.infra.selenium_session import SeleniumSession
from src.application.profile_service import ProfileService
from src.pages import BasePage, LoginPage, HomePage
from src.core.ports import Locator
from tests.test_data import TestData


@pytest.mark.e2e
@pytest.mark.slow
class TestLoginWorkflow:
    """End-to-end tests for login workflow using POM."""
    
    @pytest.fixture
    def login_page(self, browser_session):
        """Create a LoginPage instance."""
        return LoginPage(browser_session, base_url=TestData.DEMO_QA_URLS.base_url)
    
    @pytest.fixture
    def home_page(self, browser_session):
        """Create a HomePage instance."""
        return HomePage(browser_session, base_url=TestData.DEMO_QA_URLS.base_url)
    
    @pytest.mark.skip(reason="Requires real browser setup")
    def test_successful_login_flow(self, login_page, home_page, test_data):
        """Test complete successful login flow."""
        # Arrange
        user = test_data.VALID_USER
        
        # Act - Navigate to login page
        login_page.navigate()
        
        # Assert - Login page loaded
        assert login_page.wait_for_page_load()
        assert login_page.is_login_button_visible()
        
        # Act - Perform login
        login_page.login(user.username, user.password)
        
        # Assert - Successful login
        assert login_page.is_logged_in()
        
        # Assert - Home page loaded
        assert home_page.wait_for_page_load()
    
    @pytest.mark.skip(reason="Requires real browser setup")
    def test_login_with_invalid_credentials(self, login_page, test_data):
        """Test login with invalid credentials shows error."""
        # Arrange
        invalid_user = test_data.INVALID_USER
        
        # Act
        login_page.navigate()
        login_page.login(invalid_user.username, invalid_user.password)
        
        # Assert
        assert login_page.is_error_displayed()
        error_msg = login_page.get_error_message()
        assert len(error_msg) > 0
    
    @pytest.mark.skip(reason="Requires real browser setup")
    def test_login_with_remember_me(self, login_page, test_data):
        """Test login with remember me checkbox."""
        # Arrange
        user = test_data.VALID_USER
        
        # Act
        login_page.navigate()
        login_page.check_remember_me()
        
        # Assert
        assert login_page.is_remember_me_checked()
        
        # Act - Login
        login_page.login(user.username, user.password, remember_me=True)
        
        # Assert
        assert login_page.is_logged_in()


@pytest.mark.e2e
@pytest.mark.slow
class TestSearchWorkflow:
    """End-to-end tests for search functionality using POM."""
    
    @pytest.fixture
    def home_page(self, browser_session):
        """Create a HomePage instance."""
        return HomePage(browser_session, base_url=TestData.TEST_URLS.base_url)
    
    @pytest.mark.skip(reason="Requires real browser setup")
    def test_search_with_results(self, home_page, test_data):
        """Test search returns results."""
        # Arrange
        search_data = test_data.SEARCH_LAPTOP
        
        # Act
        home_page.navigate()
        home_page.wait_for_page_load()
        home_page.search(search_data.query)
        
        # Assert
        assert home_page.has_featured_items()
        item_count = home_page.get_featured_item_count()
        assert item_count > 0
    
    @pytest.mark.skip(reason="Requires real browser setup")
    def test_search_no_results(self, home_page, test_data):
        """Test search with no results."""
        # Arrange
        search_data = test_data.SEARCH_NO_RESULTS
        
        # Act
        home_page.navigate()
        home_page.search(search_data.query)
        
        # Assert
        assert not home_page.has_featured_items()


@pytest.mark.e2e
@pytest.mark.slow
class TestNavigationWorkflow:
    """End-to-end tests for navigation using POM."""
    
    @pytest.fixture
    def home_page(self, browser_session):
        """Create a HomePage instance."""
        return HomePage(browser_session, base_url=TestData.TEST_URLS.base_url)
    
    @pytest.mark.skip(reason="Requires real browser setup")
    def test_navigate_through_menu(self, home_page):
        """Test navigating through menu items."""
        # Act
        home_page.navigate()
        home_page.wait_for_page_load()
        
        initial_url = home_page.get_current_url()
        
        # Navigate to products
        home_page.navigate_to_products()
        products_url = home_page.get_current_url()
        
        # Assert
        assert products_url != initial_url
        assert "products" in products_url.lower() or "product" in products_url.lower()
    
    @pytest.mark.skip(reason="Requires real browser setup")
    def test_browser_navigation_buttons(self, home_page):
        """Test browser back/forward navigation."""
        # Act
        home_page.navigate()
        initial_url = home_page.get_current_url()
        
        home_page.navigate_to_products()
        products_url = home_page.get_current_url()
        
        home_page.go_back()
        back_url = home_page.get_current_url()
        
        home_page.go_forward()
        forward_url = home_page.get_current_url()
        
        # Assert
        assert back_url == initial_url
        assert forward_url == products_url


@pytest.mark.e2e
@pytest.mark.smoke
class TestCriticalUserJourneys:
    """Smoke tests for critical user journeys."""
    
    @pytest.mark.skip(reason="Requires real browser setup")
    def test_complete_user_journey(self, browser_session, test_data):
        """Test complete user journey from login to checkout."""
        # This is a placeholder for a complete E2E test
        # In real scenario, this would test:
        # 1. Login
        # 2. Search for product
        # 3. Add to cart
        # 4. Checkout
        # 5. Verify order
        
        login_page = LoginPage(browser_session)
        home_page = HomePage(browser_session)
        
        # Step 1: Login
        login_page.navigate()
        login_page.login(test_data.VALID_USER.username, test_data.VALID_USER.password)
        assert login_page.is_logged_in()
        
        # Step 2: Navigate to home
        home_page.navigate()
        assert home_page.is_page_loaded()
        
        # Additional steps would be implemented here
        pass


# ==================== Utility Test Helpers ====================

class TestBasePageUtilities:
    """Test BasePage utility methods."""
    
    def test_base_page_creation(self, browser_session):
        """Test creating a BasePage instance."""
        page = BasePage(browser_session)
        
        assert page.session == browser_session
        assert page.element_service is not None
    
    def test_base_page_with_custom_url(self, browser_session):
        """Test BasePage with custom URL."""
        page = BasePage(browser_session)
        page.url = "https://custom-url.com"
        
        assert page.url == "https://custom-url.com"
    
    @pytest.mark.skip(reason="Requires real browser")
    def test_base_page_navigation(self, browser_session):
        """Test BasePage navigation methods."""
        page = BasePage(browser_session)
        page.url = "https://example.com"
        
        # This would require a real browser
        # page.navigate()
        # assert "example.com" in page.get_current_url()
        pass


# ==================== Parametrized E2E Tests ====================

@pytest.mark.e2e
@pytest.mark.parametrize("user_role", ["valid", "admin"])
@pytest.mark.skip(reason="Requires real browser setup")
def test_login_with_different_users(browser_session, test_data, user_role):
    """Test login with different user roles."""
    login_page = LoginPage(browser_session)
    user = test_data.get_user_by_role(user_role)
    
    login_page.navigate()
    login_page.login(user.username, user.password)
    
    assert login_page.is_logged_in()


@pytest.mark.e2e
@pytest.mark.parametrize("search_query", ["laptop", "phone", "tablet"])
@pytest.mark.skip(reason="Requires real browser setup")
def test_search_with_different_queries(browser_session, search_query):
    """Test search with different queries."""
    home_page = HomePage(browser_session)
    
    home_page.navigate()
    home_page.search(search_query)
    
    # Verify some results are returned
    # (In real test, you'd verify search results match query)
    pass
