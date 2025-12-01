"""
Unit Tests for Core Layer - Locator

Tests the Locator class including:
- Locator creation with valid strategies
- Invalid strategy validation
- Locator tuple conversion
"""

import pytest
from selenium.webdriver.common.by import By
from src.core.ports import Locator


class TestLocator:
    """Test suite for Locator class."""
    
    def test_locator_creation_with_id(self):
        """Test creating locator with ID strategy."""
        locator = Locator(By.ID, "username")
        
        assert locator.by == By.ID
        assert locator.value == "username"
    
    def test_locator_creation_with_xpath(self):
        """Test creating locator with XPATH strategy."""
        locator = Locator(By.XPATH, "//div[@class='container']")
        
        assert locator.by == By.XPATH
        assert locator.value == "//div[@class='container']"
    
    def test_locator_creation_with_css_selector(self):
        """Test creating locator with CSS_SELECTOR strategy."""
        locator = Locator(By.CSS_SELECTOR, ".btn-primary")
        
        assert locator.by == By.CSS_SELECTOR
        assert locator.value == ".btn-primary"
    
    def test_locator_invalid_strategy_raises_error(self):
        """Test that invalid strategy raises ValueError."""
        with pytest.raises(ValueError) as exc_info:
            Locator("invalid_strategy", "value")
        
        assert "Invalid locator strategy" in str(exc_info.value)
    
    def test_locator_as_tuple(self):
        """Test converting locator to tuple."""
        locator = Locator(By.NAME, "email")
        
        result = locator.as_tuple()
        
        assert isinstance(result, tuple)
        assert result == (By.NAME, "email")
    
    def test_locator_with_all_valid_strategies(self):
        """Test creating locators with all valid strategies."""
        strategies = [
            By.ID,
            By.XPATH,
            By.LINK_TEXT,
            By.PARTIAL_LINK_TEXT,
            By.NAME,
            By.TAG_NAME,
            By.CLASS_NAME,
            By.CSS_SELECTOR,
        ]
        
        for strategy in strategies:
            locator = Locator(strategy, "test_value")
            assert locator.by == strategy
            assert locator.value == "test_value"
    
    def test_locator_valid_strategies_set(self):
        """Test that VALID_STRATEGIES contains expected strategies."""
        expected_strategies = {
            By.ID,
            By.XPATH,
            By.LINK_TEXT,
            By.PARTIAL_LINK_TEXT,
            By.NAME,
            By.TAG_NAME,
            By.CLASS_NAME,
            By.CSS_SELECTOR,
        }
        
        assert Locator.VALID_STRATEGIES == expected_strategies


class TestWaitCondition:
    """Test suite for WaitCondition constants."""
    
    def test_wait_condition_constants_exist(self):
        """Test that all expected wait condition constants exist."""
        from src.core.ports import WaitCondition
        
        assert hasattr(WaitCondition, 'ELEMENT_TO_BE_CLICKABLE')
        assert hasattr(WaitCondition, 'PRESENCE_OF_ELEMENT_LOCATED')
        assert hasattr(WaitCondition, 'VISIBILITY_OF_ELEMENT_LOCATED')
    
    def test_wait_condition_values(self):
        """Test wait condition constant values."""
        from src.core.ports import WaitCondition
        
        assert WaitCondition.ELEMENT_TO_BE_CLICKABLE == 'element_to_be_clickable'
        assert WaitCondition.PRESENCE_OF_ELEMENT_LOCATED == 'presence_of_element_located'
        assert WaitCondition.VISIBILITY_OF_ELEMENT_LOCATED == 'visibility_of_element_located'
