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


class TestBrowserConfigBuilderNewMethods:
    """Test suite for new anti-detection methods in BrowserConfigBuilder."""
    
    def test_disable_blink_features_chrome(self):
        """Test disabling Blink features in Chrome."""
        builder = BrowserConfigBuilder('chrome')
        options = builder.disable_blink_features('AutomationControlled').build()
        
        assert '--disable-blink-features=AutomationControlled' in options.arguments
    
    def test_disable_blink_features_custom_feature(self):
        """Test disabling custom Blink feature."""
        builder = BrowserConfigBuilder('chrome')
        options = builder.disable_blink_features('CustomFeature').build()
        
        assert '--disable-blink-features=CustomFeature' in options.arguments
    
    def test_disable_blink_features_firefox_no_op(self):
        """Test that disable_blink_features is no-op for Firefox."""
        builder = BrowserConfigBuilder('firefox')
        options = builder.disable_blink_features('AutomationControlled').build()
        
        # Firefox doesn't have this argument, should not raise error
        assert isinstance(options, FirefoxOptions)
    
    def test_add_experimental_option_chrome(self):
        """Test adding experimental option in Chrome."""
        builder = BrowserConfigBuilder('chrome')
        options = builder.add_experimental_option('prefs', {'key': 'value'}).build()
        
        assert isinstance(options, ChromeOptions)
        # Experimental options are stored in options.experimental_options
        assert 'prefs' in options.experimental_options
    
    def test_exclude_switches_chrome(self):
        """Test excluding switches in Chrome."""
        builder = BrowserConfigBuilder('chrome')
        options = builder.exclude_switches(['enable-logging']).build()
        
        assert isinstance(options, ChromeOptions)
        assert 'excludeSwitches' in options.experimental_options
        assert 'enable-logging' in options.experimental_options['excludeSwitches']
    
    def test_exclude_switches_multiple(self):
        """Test excluding multiple switches."""
        builder = BrowserConfigBuilder('chrome')
        options = builder.exclude_switches(['enable-logging', 'enable-automation']).build()
        
        assert 'excludeSwitches' in options.experimental_options
        assert 'enable-logging' in options.experimental_options['excludeSwitches']
        assert 'enable-automation' in options.experimental_options['excludeSwitches']
    
    def test_disable_automation_extension_chrome(self):
        """Test disabling automation extension in Chrome."""
        builder = BrowserConfigBuilder('chrome')
        options = builder.disable_automation_extension().build()
        
        assert isinstance(options, ChromeOptions)
        assert 'useAutomationExtension' in options.experimental_options
        assert options.experimental_options['useAutomationExtension'] is False
    
    def test_disable_automation_extension_firefox_no_op(self):
        """Test that disable_automation_extension is no-op for Firefox."""
        builder = BrowserConfigBuilder('firefox')
        options = builder.disable_automation_extension().build()
        
        # Firefox doesn't support this, should not raise error
        assert isinstance(options, FirefoxOptions)
    
    def test_method_chaining_with_new_methods(self):
        """Test that new methods support chaining."""
        builder = BrowserConfigBuilder('chrome')
        
        result = (builder
                  .set_no_sandbox()
                  .disable_blink_features()
                  .exclude_switches(['enable-logging'])
                  .disable_automation_extension())
        
        assert isinstance(result, BrowserConfigBuilder)
    
    def test_complete_anti_detection_setup_chrome(self):
        """Test complete anti-detection setup for Chrome."""
        builder = BrowserConfigBuilder('chrome')
        options = (builder
                   .set_no_sandbox()
                   .disable_dev_shm_usage()
                   .disable_blink_features('AutomationControlled')
                   .exclude_switches(['enable-logging'])
                   .disable_automation_extension()
                   .build())
        
        assert '--no-sandbox' in options.arguments
        assert '--disable-dev-shm-usage' in options.arguments
        assert '--disable-blink-features=AutomationControlled' in options.arguments
        assert 'excludeSwitches' in options.experimental_options
        assert options.experimental_options['useAutomationExtension'] is False
    
    def test_complete_anti_detection_setup_firefox(self):
        """Test that anti-detection setup doesn't break Firefox."""
        builder = BrowserConfigBuilder('firefox')
        options = (builder
                   .set_no_sandbox()
                   .disable_dev_shm_usage()
                   .disable_blink_features('AutomationControlled')
                   .exclude_switches(['enable-logging'])
                   .disable_automation_extension()
                   .build())
        
        # Firefox should still work with Chrome-specific methods (no-op)
        assert isinstance(options, FirefoxOptions)
        assert '--no-sandbox' in options.arguments
        assert '--disable-dev-shm-usage' in options.arguments
    
    @pytest.mark.parametrize("browser_name", ['chrome', 'firefox', 'edge'])
    def test_cross_browser_compatibility(self, browser_name):
        """Test that new methods work across all browsers without errors."""
        builder = BrowserConfigBuilder(browser_name)
        
        # This should not raise any errors for any browser
        options = (builder
                   .disable_blink_features()
                   .exclude_switches(['enable-logging'])
                   .disable_automation_extension()
                   .build())
        
        assert options is not None
    
    def test_backward_compatibility_existing_code(self):
        """Test that existing code patterns still work."""
        # Old pattern should still work
        builder = BrowserConfigBuilder('chrome')
        options = builder.set_no_sandbox().disable_dev_shm_usage().build()
        
        assert '--no-sandbox' in options.arguments
        assert '--disable-dev-shm-usage' in options.arguments

