"""
Integration Tests for SeleniumSession

Tests the Selenium session with mocked drivers.
These tests verify session lifecycle and operations.
"""

import pytest
from unittest.mock import Mock, MagicMock, patch
from selenium.webdriver.common.by import By
from src.infra.selenium_session import SeleniumSession
from src.core.ports import Locator, WaitCondition


class TestSeleniumSession:
    """Test suite for SeleniumSession integration."""
    
    def test_session_initialization(self):
        """Test session initializes without driver."""
        session = SeleniumSession()
        
        assert session.driver is None
        assert session.factory is not None
    
    @patch('src.infra.selenium_session.BrowserFactory')
    def test_session_open_creates_driver(self, mock_factory_class):
        """Test that open() creates driver via factory."""
        mock_factory = Mock()
        mock_driver = Mock()
        mock_factory.create_browser.return_value = mock_driver
        mock_factory_class.return_value = mock_factory
        
        session = SeleniumSession()
        session.open('chrome', Mock(), {'browser_type': 'chrome'})
        
        assert session.driver == mock_driver
        mock_factory.create_browser.assert_called_once()
    
    def test_session_close_quits_driver(self):
        """Test that close() quits the driver."""
        session = SeleniumSession()
        mock_driver = Mock()
        session.driver = mock_driver
        
        session.close()
        
        mock_driver.quit.assert_called_once()
        assert session.driver is None
    
    def test_session_get_navigates_to_url(self):
        """Test that get() navigates to URL."""
        session = SeleniumSession()
        mock_driver = Mock()
        session.driver = mock_driver
        
        session.get('https://example.com')
        
        mock_driver.get.assert_called_once_with('https://example.com')
    
    def test_session_new_tab_creates_new_window(self):
        """Test that new_tab() creates a new window."""
        session = SeleniumSession()
        mock_driver = Mock()
        mock_driver.current_window_handle = 'new-handle'
        session.driver = mock_driver
        
        handle = session.new_tab()
        
        assert handle == 'new-handle'
        assert mock_driver.switch_to.new_window.called
    
    def test_session_switch_tab_switches_window(self):
        """Test that switch_tab() switches to window."""
        session = SeleniumSession()
        mock_driver = Mock()
        session.driver = mock_driver
        
        session.switch_tab('target-handle')
        
        mock_driver.switch_to.window.assert_called_once_with('target-handle')
    
    def test_session_close_tab_closes_window(self):
        """Test that close_tab() closes specific window."""
        session = SeleniumSession()
        mock_driver = Mock()
        session.driver = mock_driver
        
        session.close_tab('target-handle')
        
        mock_driver.switch_to.window.assert_called_once_with('target-handle')
        mock_driver.close.assert_called_once()
    
    def test_session_execute_cdp_calls_driver_method(self):
        """Test that execute_cdp() calls driver CDP command."""
        session = SeleniumSession()
        mock_driver = Mock()
        mock_driver.execute_cdp_cmd.return_value = {'result': 'success'}
        session.driver = mock_driver
        
        result = session.execute_cdp('Network.enable', {})
        
        assert result == {'result': 'success'}
        mock_driver.execute_cdp_cmd.assert_called_once()
    
    @patch('src.infra.selenium_session.WebDriverWait')
    def test_session_find_element_with_wait(self, mock_wait_class):
        """Test that find_element() uses WebDriverWait."""
        session = SeleniumSession()
        mock_driver = Mock()
        session.driver = mock_driver
        
        mock_element = Mock()
        mock_wait = Mock()
        mock_wait.until.return_value = mock_element
        mock_wait_class.return_value = mock_wait
        
        locator = Locator(By.ID, 'test-id')
        result = session.find_element(locator, timeout=10)
        
        assert result == mock_element
        mock_wait_class.assert_called_once()
    
    @patch('src.infra.selenium_session.WebDriverWait')
    def test_session_find_elements_returns_list(self, mock_wait_class):
        """Test that find_elements() returns list of elements."""
        session = SeleniumSession()
        mock_driver = Mock()
        session.driver = mock_driver
        
        mock_elements = [Mock(), Mock(), Mock()]
        mock_wait = Mock()
        mock_wait.until.return_value = mock_elements
        mock_wait_class.return_value = mock_wait
        
        locator = Locator(By.CSS_SELECTOR, '.item')
        result = session.find_elements(locator)
        
        assert result == mock_elements
        assert len(result) == 3


@pytest.mark.integration
class TestSeleniumSessionWithMockDriver:
    """Test SeleniumSession with fully mocked driver."""
    
    @pytest.fixture
    def mock_session(self, mock_driver):
        """Create session with mocked driver."""
        session = SeleniumSession()
        session.driver = mock_driver
        return session
    
    def test_session_operations_with_mock_driver(self, mock_session, mock_driver):
        """Test various session operations with mocked driver."""
        # Test get
        mock_session.get('https://test.com')
        mock_driver.get.assert_called_with('https://test.com')
        
        # Test properties
        assert mock_session.driver == mock_driver
        
        # Test close
        mock_session.close()
        mock_driver.quit.assert_called_once()
