"""
E2E Tests for Jira Login Page

This module contains end-to-end tests for the JiraLoginPage class.
Tests verify actual interactions with the Jira login page at https://jira.inside45.ir

Test Categories:
- Page element verification
- Login functionality (requires valid credentials)
- Error handling
- Remember me functionality
- Password visibility toggle
- Form validation
"""

import pytest
from src.pages.jira_login_page import JiraLoginPage
from tests.test_data.test_data import TestData

# Mark all tests in this module as E2E and skip by default
# Remove @pytest.mark.skip when ready to run with real browser
pytestmark = [pytest.mark.e2e, pytest.mark.skip(reason="Requires real browser and network access")]


class TestJiraLoginPageElements:
    """Test suite for verifying Jira login page elements."""
    
    def test_login_page_loads_successfully(self, chrome_session):
        """Test that the Jira login page loads and displays all elements."""
        # Arrange
        jira_login = JiraLoginPage(chrome_session, base_url="https://jira.inside45.ir")
        
        # Act
        jira_login.navigate()
        jira_login.wait_for_page_ready(timeout=15)
        
        # Assert
        assert jira_login.is_login_page_loaded(), "Login page should be fully loaded"
        assert jira_login.is_username_field_visible(), "Username field should be visible"
        assert jira_login.is_password_field_visible(), "Password field should be visible"
        assert jira_login.is_login_button_enabled(), "Login button should be enabled"
    
    def test_all_critical_elements_present(self, chrome_session):
        """Test that all critical page elements are present."""
        # Arrange
        jira_login = JiraLoginPage(chrome_session, base_url="https://jira.inside45.ir")
        jira_login.navigate()
        jira_login.wait_for_page_ready()
        
        # Act
        elements = jira_login.verify_login_page_elements()
        
        # Assert
        critical_elements = ["login_form", "username_field", "password_field", "login_button"]
        for element in critical_elements:
            assert elements.get(element, False), f"{element} should be present on the page"
    
    def test_page_title_and_header(self, chrome_session):
        """Test that page title and header text are correct."""
        # Arrange
        jira_login = JiraLoginPage(chrome_session, base_url="https://jira.inside45.ir")
        jira_login.navigate()
        jira_login.wait_for_page_ready()
        
        # Act
        title = jira_login.get_page_title()
        header_text = jira_login.get_login_header_text()
        
        # Assert
        assert title is not None and len(title) > 0, "Page should have a title"
        assert "Log in" in header_text, "Header should contain 'Log in' text"
    
    def test_jira_version_displayed(self, chrome_session):
        """Test that Jira version information is accessible."""
        # Arrange
        jira_login = JiraLoginPage(chrome_session, base_url="https://jira.inside45.ir")
        jira_login.navigate()
        jira_login.wait_for_page_ready()
        
        # Act
        version = jira_login.get_jira_version()
        
        # Assert
        assert version is not None, "Jira version should be available"
        assert len(version) > 0, "Jira version should not be empty"
    
    def test_remember_me_checkbox_present(self, chrome_session):
        """Test that remember me checkbox is present and functional."""
        # Arrange
        jira_login = JiraLoginPage(chrome_session, base_url="https://jira.inside45.ir")
        jira_login.navigate()
        jira_login.wait_for_page_ready()
        
        # Assert
        elements = jira_login.verify_login_page_elements()
        assert elements.get("remember_me", False), "Remember me checkbox should be present"
    
    def test_forgot_password_link_present(self, chrome_session):
        """Test that forgot password link is present."""
        # Arrange
        jira_login = JiraLoginPage(chrome_session, base_url="https://jira.inside45.ir")
        jira_login.navigate()
        jira_login.wait_for_page_ready()
        
        # Assert
        elements = jira_login.verify_login_page_elements()
        assert elements.get("forgot_password_link", False), "Forgot password link should be present"


class TestJiraLoginFunctionality:
    """Test suite for Jira login functionality (requires valid credentials)."""
    
    @pytest.mark.parametrize("username,password", [
        pytest.param("valid_user", "valid_pass", id="valid_credentials",
                    marks=pytest.mark.skip(reason="Replace with actual valid credentials")),
    ])
    def test_successful_login(self, chrome_session, username, password):
        """Test successful login with valid credentials."""
        # Arrange
        jira_login = JiraLoginPage(chrome_session, base_url="https://jira.inside45.ir")
        jira_login.navigate()
        jira_login.wait_for_page_ready()
        
        # Act
        jira_login.login(username, password, remember_me=False)
        
        # Assert
        assert jira_login.is_login_successful(timeout=15), "Login should succeed with valid credentials"
        current_url = chrome_session.get_current_url()
        assert "login.jsp" not in current_url, "Should be redirected away from login page"
    
    @pytest.mark.parametrize("username,password", [
        ("invalid_user", "invalid_pass"),
        ("", "password123"),
        ("username", ""),
        ("", ""),
    ])
    def test_failed_login_invalid_credentials(self, chrome_session, username, password):
        """Test login failure with invalid credentials."""
        # Arrange
        jira_login = JiraLoginPage(chrome_session, base_url="https://jira.inside45.ir")
        jira_login.navigate()
        jira_login.wait_for_page_ready()
        
        # Act
        if username and password:  # Only try to login if both fields have values
            jira_login.login(username, password)
        else:
            # For empty fields, just fill what we have and click
            if username:
                jira_login.enter_username(username)
            if password:
                jira_login.enter_password(password)
            jira_login.click_login_button()
        
        # Assert
        assert not jira_login.is_login_successful(timeout=5), "Login should fail with invalid credentials"
        # Should either show error or stay on login page
        current_url = chrome_session.get_current_url()
        assert "login.jsp" in current_url or jira_login.has_error_message(), \
            "Should remain on login page or show error"
    
    def test_login_with_screenshot_on_failure(self, chrome_session):
        """Test that screenshot is taken on login failure."""
        # Arrange
        jira_login = JiraLoginPage(chrome_session, base_url="https://jira.inside45.ir")
        jira_login.navigate()
        jira_login.wait_for_page_ready()
        
        # Act
        success, error_msg = jira_login.login_with_screenshot(
            username="invalid_user",
            password="invalid_pass"
        )
        
        # Assert
        assert not success, "Login should fail with invalid credentials"
        assert error_msg is not None or error_msg == "", "Should return error message"


class TestJiraRememberMeFunctionality:
    """Test suite for remember me checkbox functionality."""
    
    def test_toggle_remember_me_from_unchecked_to_checked(self, chrome_session):
        """Test toggling remember me checkbox from unchecked to checked."""
        # Arrange
        jira_login = JiraLoginPage(chrome_session, base_url="https://jira.inside45.ir")
        jira_login.navigate()
        jira_login.wait_for_page_ready()
        
        # Act - Check the box
        jira_login.toggle_remember_me(should_remember=True)
        
        # Assert
        assert jira_login.is_remember_me_checked(), "Remember me should be checked"
    
    def test_toggle_remember_me_from_checked_to_unchecked(self, chrome_session):
        """Test toggling remember me checkbox from checked to unchecked."""
        # Arrange
        jira_login = JiraLoginPage(chrome_session, base_url="https://jira.inside45.ir")
        jira_login.navigate()
        jira_login.wait_for_page_ready()
        
        # Act - Check then uncheck
        jira_login.toggle_remember_me(should_remember=True)
        assert jira_login.is_remember_me_checked(), "Setup: checkbox should be checked"
        
        jira_login.toggle_remember_me(should_remember=False)
        
        # Assert
        assert not jira_login.is_remember_me_checked(), "Remember me should be unchecked"
    
    def test_remember_me_state_in_login_method(self, chrome_session):
        """Test that remember me state is correctly set in login method."""
        # Arrange
        jira_login = JiraLoginPage(chrome_session, base_url="https://jira.inside45.ir")
        jira_login.navigate()
        jira_login.wait_for_page_ready()
        
        # Act - Use login method with remember_me=True
        jira_login.enter_username("test_user")
        jira_login.enter_password("test_pass")
        jira_login.toggle_remember_me(True)
        
        # Assert
        assert jira_login.is_remember_me_checked(), "Remember me should be checked after login setup"


class TestJiraPasswordVisibility:
    """Test suite for password visibility toggle functionality."""
    
    def test_password_initially_hidden(self, chrome_session):
        """Test that password field is initially hidden (type=password)."""
        # Arrange
        jira_login = JiraLoginPage(chrome_session, base_url="https://jira.inside45.ir")
        jira_login.navigate()
        jira_login.wait_for_page_ready()
        
        # Act
        jira_login.enter_password("test_password")
        
        # Assert
        assert not jira_login.is_password_visible(), "Password should initially be hidden"
    
    def test_toggle_password_visibility_to_visible(self, chrome_session):
        """Test toggling password to visible state."""
        # Arrange
        jira_login = JiraLoginPage(chrome_session, base_url="https://jira.inside45.ir")
        jira_login.navigate()
        jira_login.wait_for_page_ready()
        jira_login.enter_password("test_password")
        
        # Act
        jira_login.click_toggle_password_visibility()
        chrome_session.sleep(0.5)  # Brief wait for UI update
        
        # Assert
        assert jira_login.is_password_visible(), "Password should be visible after toggle"
    
    def test_toggle_password_visibility_back_to_hidden(self, chrome_session):
        """Test toggling password back to hidden state."""
        # Arrange
        jira_login = JiraLoginPage(chrome_session, base_url="https://jira.inside45.ir")
        jira_login.navigate()
        jira_login.wait_for_page_ready()
        jira_login.enter_password("test_password")
        
        # Act - Toggle twice (show then hide)
        jira_login.click_toggle_password_visibility()
        chrome_session.sleep(0.5)
        assert jira_login.is_password_visible(), "Setup: password should be visible"
        
        jira_login.click_toggle_password_visibility()
        chrome_session.sleep(0.5)
        
        # Assert
        assert not jira_login.is_password_visible(), "Password should be hidden after second toggle"


class TestJiraFieldOperations:
    """Test suite for field input and validation operations."""
    
    def test_enter_and_retrieve_username(self, chrome_session):
        """Test entering username and retrieving its value."""
        # Arrange
        jira_login = JiraLoginPage(chrome_session, base_url="https://jira.inside45.ir")
        jira_login.navigate()
        jira_login.wait_for_page_ready()
        test_username = "test_user_123"
        
        # Act
        jira_login.enter_username(test_username)
        actual_username = jira_login.get_username_value()
        
        # Assert
        assert actual_username == test_username, f"Username should be '{test_username}'"
    
    def test_enter_and_retrieve_password(self, chrome_session):
        """Test entering password and retrieving its value."""
        # Arrange
        jira_login = JiraLoginPage(chrome_session, base_url="https://jira.inside45.ir")
        jira_login.navigate()
        jira_login.wait_for_page_ready()
        test_password = "test_pass_456"
        
        # Act
        jira_login.enter_password(test_password)
        actual_password = jira_login.get_password_value()
        
        # Assert
        assert actual_password == test_password, f"Password should be '{test_password}'"
    
    def test_clear_username_field(self, chrome_session):
        """Test clearing username field."""
        # Arrange
        jira_login = JiraLoginPage(chrome_session, base_url="https://jira.inside45.ir")
        jira_login.navigate()
        jira_login.wait_for_page_ready()
        jira_login.enter_username("test_user")
        
        # Act
        jira_login.clear_username()
        
        # Assert
        assert jira_login.get_username_value() == "", "Username field should be empty"
    
    def test_clear_password_field(self, chrome_session):
        """Test clearing password field."""
        # Arrange
        jira_login = JiraLoginPage(chrome_session, base_url="https://jira.inside45.ir")
        jira_login.navigate()
        jira_login.wait_for_page_ready()
        jira_login.enter_password("test_pass")
        
        # Act
        jira_login.clear_password()
        
        # Assert
        assert jira_login.get_password_value() == "", "Password field should be empty"
    
    def test_clear_all_fields(self, chrome_session):
        """Test clearing both username and password fields."""
        # Arrange
        jira_login = JiraLoginPage(chrome_session, base_url="https://jira.inside45.ir")
        jira_login.navigate()
        jira_login.wait_for_page_ready()
        jira_login.enter_username("test_user")
        jira_login.enter_password("test_pass")
        
        # Act
        jira_login.clear_all_fields()
        
        # Assert
        assert jira_login.get_username_value() == "", "Username field should be empty"
        assert jira_login.get_password_value() == "", "Password field should be empty"
    
    def test_username_field_is_required(self, chrome_session):
        """Test that username field has required attribute."""
        # Arrange
        jira_login = JiraLoginPage(chrome_session, base_url="https://jira.inside45.ir")
        jira_login.navigate()
        jira_login.wait_for_page_ready()
        
        # Assert
        assert jira_login.is_username_field_required(), "Username field should be required"
    
    def test_password_field_is_required(self, chrome_session):
        """Test that password field has required attribute."""
        # Arrange
        jira_login = JiraLoginPage(chrome_session, base_url="https://jira.inside45.ir")
        jira_login.navigate()
        jira_login.wait_for_page_ready()
        
        # Assert
        assert jira_login.is_password_field_required(), "Password field should be required"


class TestJiraAlternativeLoginMethods:
    """Test suite for alternative login submission methods."""
    
    def test_submit_login_with_enter_key(self, chrome_session):
        """Test submitting login form by pressing Enter key."""
        # Arrange
        jira_login = JiraLoginPage(chrome_session, base_url="https://jira.inside45.ir")
        jira_login.navigate()
        jira_login.wait_for_page_ready()
        
        # Act
        jira_login.enter_username("test_user")
        jira_login.enter_password("test_pass")
        jira_login.submit_form_by_enter_key()
        
        # Assert
        # Should attempt to submit (will fail with invalid creds, but form submission should occur)
        chrome_session.sleep(2)  # Wait for any response
        # Either error message appears or we're still on login page
        current_url = chrome_session.get_current_url()
        assert "login.jsp" in current_url or jira_login.has_error_message(), \
            "Form should be submitted (staying on login page or showing error)"
    
    def test_quick_login_method(self, chrome_session):
        """Test the quick_login convenience method."""
        # Arrange
        jira_login = JiraLoginPage(chrome_session, base_url="https://jira.inside45.ir")
        jira_login.navigate()
        jira_login.wait_for_page_ready()
        
        # Act
        jira_login.quick_login("test_user", "test_pass")
        
        # Assert
        # Should attempt login (will fail but method should execute)
        assert not jira_login.is_remember_me_checked(), \
            "Quick login should not check remember me"


class TestJiraNavigationAndWait:
    """Test suite for navigation and wait operations."""
    
    def test_navigate_to_login_page(self, chrome_session):
        """Test navigation to Jira login page."""
        # Arrange
        jira_login = JiraLoginPage(chrome_session, base_url="https://jira.inside45.ir")
        
        # Act
        jira_login.navigate()
        
        # Assert
        current_url = chrome_session.get_current_url()
        assert "jira.inside45.ir" in current_url, "Should navigate to Jira domain"
        assert "login.jsp" in current_url, "Should be on login page"
    
    def test_wait_for_page_ready(self, chrome_session):
        """Test waiting for page to be ready."""
        # Arrange
        jira_login = JiraLoginPage(chrome_session, base_url="https://jira.inside45.ir")
        jira_login.navigate()
        
        # Act & Assert - Should not raise exception
        jira_login.wait_for_page_ready(timeout=15)
        assert jira_login.is_login_page_loaded(), "Page should be ready after wait"
    
    def test_wait_for_login_completion_with_invalid_creds(self, chrome_session):
        """Test waiting for login completion with invalid credentials."""
        # Arrange
        jira_login = JiraLoginPage(chrome_session, base_url="https://jira.inside45.ir")
        jira_login.navigate()
        jira_login.wait_for_page_ready()
        
        # Act
        jira_login.enter_username("invalid")
        jira_login.enter_password("invalid")
        jira_login.click_login_button()
        
        result = jira_login.wait_for_login_completion(timeout=10)
        
        # Assert
        assert not result, "Login completion should return False for invalid credentials"
