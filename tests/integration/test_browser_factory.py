"""
Integration Tests for BrowserFactory

Tests the browser factory with real driver creation (mocked).
These tests verify the factory pattern implementation.
"""

import pytest
from unittest.mock import Mock, patch
from src.infra.browser_factory import BrowserFactory
from src.utils.exceptions import BrowserInitializationError


class TestBrowserFactory:
    """Test suite for BrowserFactory integration."""
    
    def test_factory_initialization(self):
        """Test factory initializes with driver map."""
        factory = BrowserFactory()
        
        assert 'chrome' in factory.driver_map
        assert 'firefox' in factory.driver_map
        assert 'remote' in factory.driver_map
    
    @patch('src.infra.browser_factory.DriverCreator.create_chrome_driver')
    def test_factory_creates_chrome_browser(self, mock_create_chrome):
        """Test factory creates Chrome browser."""
        mock_driver = Mock()
        mock_create_chrome.return_value = mock_driver
        
        factory = BrowserFactory()
        options = Mock()
        connection = {'browser_type': 'chrome', 'binary_path': '/path/to/driver'}
        
        result = factory.create_browser('chrome', options, connection)
        
        assert result == mock_driver
        mock_create_chrome.assert_called_once_with(options, connection)
    
    @patch('src.infra.browser_factory.DriverCreator.create_firefox_driver')
    def test_factory_creates_firefox_browser(self, mock_create_firefox):
        """Test factory creates Firefox browser."""
        mock_driver = Mock()
        mock_create_firefox.return_value = mock_driver
        
        factory = BrowserFactory()
        options = Mock()
        connection = {'browser_type': 'firefox', 'binary_path': '/path/to/driver'}
        
        result = factory.create_browser('firefox', options, connection)
        
        assert result == mock_driver
        mock_create_firefox.assert_called_once_with(options, connection)
    
    @patch('src.infra.browser_factory.DriverCreator.create_remote_driver')
    def test_factory_creates_remote_browser(self, mock_create_remote):
        """Test factory creates remote browser."""
        mock_driver = Mock()
        mock_create_remote.return_value = mock_driver
        
        factory = BrowserFactory()
        options = Mock()
        connection = {'browser_type': 'remote', 'remote_url': 'http://localhost:4444'}
        
        result = factory.create_browser('remote', options, connection)
        
        assert result == mock_driver
        mock_create_remote.assert_called_once_with(options, connection)
    
    def test_factory_invalid_browser_type_raises_error(self):
        """Test that invalid browser type raises BrowserInitializationError."""
        factory = BrowserFactory()
        
        with pytest.raises(BrowserInitializationError):
            factory.create_browser('safari', Mock(), {})
    
    @patch('src.infra.browser_factory.DriverCreator.create_chrome_driver')
    def test_factory_browser_type_case_insensitive(self, mock_create_chrome):
        """Test that browser type is case insensitive."""
        mock_driver = Mock()
        mock_create_chrome.return_value = mock_driver
        
        factory = BrowserFactory()
        
        factory.create_browser('CHROME', Mock(), {'browser_type': 'chrome'})
        factory.create_browser('Chrome', Mock(), {'browser_type': 'chrome'})
        factory.create_browser('chrome', Mock(), {'browser_type': 'chrome'})
        
        assert mock_create_chrome.call_count == 3
