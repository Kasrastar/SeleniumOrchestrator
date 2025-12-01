"""
Unit Tests for Infrastructure Layer - BrowserConfigBuilder

Tests the BrowserConfigBuilder including:
- Builder pattern functionality
- Option chaining
- Browser-specific configurations
"""

import pytest
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from src.infra.browser_config_builder import BrowserConfigBuilder


class TestBrowserConfigBuilder:
    """Test suite for BrowserConfigBuilder."""
    
    def test_builder_creates_chrome_options(self):
        """Test that builder creates Chrome options."""
        builder = BrowserConfigBuilder('chrome')
        options = builder.build()
        
        assert isinstance(options, ChromeOptions)
    
    def test_builder_creates_firefox_options(self):
        """Test that builder creates Firefox options."""
        builder = BrowserConfigBuilder('firefox')
        options = builder.build()
        
        assert isinstance(options, FirefoxOptions)
    
    def test_builder_unsupported_browser_raises_error(self):
        """Test that unsupported browser raises ValueError."""
        with pytest.raises(ValueError) as exc_info:
            BrowserConfigBuilder('safari')
        
        assert "Unsupported browser" in str(exc_info.value)
    
    def test_builder_method_chaining(self):
        """Test that builder methods support chaining."""
        builder = BrowserConfigBuilder('chrome')
        
        result = builder.set_headless().set_no_sandbox().disable_dev_shm_usage()
        
        assert isinstance(result, BrowserConfigBuilder)
    
    def test_builder_set_headless_option(self):
        """Test setting headless option."""
        builder = BrowserConfigBuilder('chrome')
        options = builder.set_headless().build()
        
        assert '--headless' in options.arguments
    
    def test_builder_set_no_sandbox_option(self):
        """Test setting no-sandbox option."""
        builder = BrowserConfigBuilder('chrome')
        options = builder.set_no_sandbox().build()
        
        assert '--no-sandbox' in options.arguments
    
    def test_builder_disable_dev_shm_usage_option(self):
        """Test disabling dev-shm-usage."""
        builder = BrowserConfigBuilder('chrome')
        options = builder.disable_dev_shm_usage().build()
        
        assert '--disable-dev-shm-usage' in options.arguments
    
    def test_builder_multiple_options_combined(self):
        """Test combining multiple options."""
        builder = BrowserConfigBuilder('chrome')
        options = (
            builder
            .set_headless()
            .set_no_sandbox()
            .disable_dev_shm_usage()
            .disable_gpu()
            .build()
        )
        
        assert '--headless' in options.arguments
        assert '--no-sandbox' in options.arguments
        assert '--disable-dev-shm-usage' in options.arguments
        assert '--disable-gpu' in options.arguments
    
    def test_builder_set_window_size(self):
        """Test setting window size."""
        builder = BrowserConfigBuilder('chrome')
        options = builder.set_window_size(1920, 1080).build()
        
        assert '--window-size=1920,1080' in options.arguments
    
    def test_builder_set_incognito(self):
        """Test setting incognito mode."""
        builder = BrowserConfigBuilder('chrome')
        options = builder.set_incognito().build()
        
        assert '--incognito' in options.arguments
    
    def test_builder_set_user_agent(self):
        """Test setting custom user agent."""
        user_agent = "Mozilla/5.0 Custom Agent"
        builder = BrowserConfigBuilder('chrome')
        options = builder.set_user_agent(user_agent).build()
        
        expected_arg = f'--user-agent={user_agent}'
        assert expected_arg in options.arguments
    
    def test_builder_browser_name_case_insensitive(self):
        """Test that browser name is case insensitive."""
        builder_lower = BrowserConfigBuilder('chrome')
        builder_upper = BrowserConfigBuilder('CHROME')
        builder_mixed = BrowserConfigBuilder('Chrome')
        
        assert isinstance(builder_lower.build(), ChromeOptions)
        assert isinstance(builder_upper.build(), ChromeOptions)
        assert isinstance(builder_mixed.build(), ChromeOptions)
    
    @pytest.mark.parametrize("browser_name,expected_type", [
        ('chrome', ChromeOptions),
        ('firefox', FirefoxOptions),
    ])
    def test_builder_supported_browsers(self, browser_name, expected_type):
        """Test that all supported browsers create correct options."""
        builder = BrowserConfigBuilder(browser_name)
        options = builder.build()
        
        assert isinstance(options, expected_type)
