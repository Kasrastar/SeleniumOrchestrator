"""
Test Data Management Module

This module provides centralized test data management for all tests.
It includes data classes for different test scenarios and utilities for loading test data.

Usage:
    from tests.test_data.test_data import TestData, UserData, BrowserData
    
    user = TestData.VALID_USER
    browser = TestData.CHROME_CONFIG
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional
from pathlib import Path
import json


@dataclass
class UserData:
    """Test user data."""
    username: str
    password: str
    email: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    
    def to_dict(self) -> Dict:
        """Convert to dictionary."""
        return {
            'username': self.username,
            'password': self.password,
            'email': self.email,
            'first_name': self.first_name,
            'last_name': self.last_name,
        }


@dataclass
class BrowserData:
    """Browser configuration test data."""
    browser_type: str
    binary_path: Optional[str] = None
    remote_url: Optional[str] = None
    options: List[str] = field(default_factory=list)
    
    def to_connection_dict(self) -> Dict:
        """Convert to connection dictionary format."""
        conn = {'browser_type': self.browser_type}
        if self.binary_path:
            conn['binary_path'] = self.binary_path
        if self.remote_url:
            conn['remote_url'] = self.remote_url
        return conn


@dataclass
class URLData:
    """URL test data."""
    base_url: str
    login_path: str = "/login"
    home_path: str = "/home"
    dashboard_path: str = "/dashboard"
    
    @property
    def login_url(self) -> str:
        return f"{self.base_url}{self.login_path}"
    
    @property
    def home_url(self) -> str:
        return f"{self.base_url}{self.home_path}"
    
    @property
    def dashboard_url(self) -> str:
        return f"{self.base_url}{self.dashboard_path}"


@dataclass
class ElementData:
    """Element locator test data."""
    by: str
    value: str
    description: Optional[str] = None


@dataclass
class SearchData:
    """Search test data."""
    query: str
    expected_results: int = 0
    exact_match: bool = False


class TestData:
    """
    Centralized test data repository.
    
    This class provides access to all test data used across the test suite.
    Modify values here to update test data globally.
    """
    
    # ==================== User Test Data ====================
    
    VALID_USER = UserData(
        username="testuser",
        password="TestPass123!",
        email="testuser@example.com",
        first_name="Test",
        last_name="User"
    )
    
    INVALID_USER = UserData(
        username="invaliduser",
        password="WrongPass123!"
    )
    
    ADMIN_USER = UserData(
        username="admin",
        password="AdminPass123!",
        email="admin@example.com"
    )
    
    EMPTY_CREDENTIALS = UserData(
        username="",
        password=""
    )
    
    # ==================== Browser Test Data ====================
    
    CHROME_CONFIG = BrowserData(
        browser_type="chrome",
        binary_path="/usr/bin/chromedriver",  # Update with actual path
        options=["--no-sandbox", "--disable-dev-shm-usage"]
    )
    
    FIREFOX_CONFIG = BrowserData(
        browser_type="firefox",
        binary_path="/usr/bin/geckodriver",  # Update with actual path
        options=["--headless"]
    )
    
    REMOTE_CHROME_CONFIG = BrowserData(
        browser_type="remote",
        remote_url="http://localhost:4444/wd/hub",
        options=[]
    )
    
    # ==================== URL Test Data ====================
    
    DEMO_QA_URLS = URLData(
        base_url="https://demoqa.com",
        login_path="/login",
        home_path="/",
        dashboard_path="/profile"
    )
    
    TEST_URLS = URLData(
        base_url="https://example.com",
        login_path="/auth/login",
        home_path="/home",
        dashboard_path="/dashboard"
    )
    
    # ==================== Search Test Data ====================
    
    SEARCH_LAPTOP = SearchData(
        query="laptop",
        expected_results=5,
        exact_match=False
    )
    
    SEARCH_PHONE = SearchData(
        query="phone",
        expected_results=10,
        exact_match=False
    )
    
    SEARCH_NO_RESULTS = SearchData(
        query="xyznonexistent123",
        expected_results=0,
        exact_match=True
    )
    
    # ==================== Timeout Configuration ====================
    
    TIMEOUTS = {
        'short': 5,
        'medium': 10,
        'long': 30,
        'element_wait': 15,
        'page_load': 20,
    }
    
    # ==================== Error Messages ====================
    
    ERROR_MESSAGES = {
        'invalid_login': "Invalid username or password",
        'empty_field': "This field is required",
        'browser_init_failed': "Failed to initialize browser",
        'element_not_found': "Element not found",
        'timeout': "Timeout waiting for element",
    }
    
    # ==================== Test Configuration ====================
    
    CONFIG = {
        'implicit_wait': 10,
        'page_load_timeout': 30,
        'screenshot_on_failure': True,
        'log_level': 'INFO',
        'retry_attempts': 3,
    }
    
    @classmethod
    def load_from_json(cls, filepath: str) -> Dict:
        """
        Load test data from JSON file.
        
        Args:
            filepath (str): Path to JSON file
            
        Returns:
            Dict: Loaded test data
        """
        path = Path(filepath)
        if not path.exists():
            raise FileNotFoundError(f"Test data file not found: {filepath}")
        
        with open(path, 'r') as f:
            return json.load(f)
    
    @classmethod
    def save_to_json(cls, data: Dict, filepath: str) -> None:
        """
        Save test data to JSON file.
        
        Args:
            data (Dict): Data to save
            filepath (str): Path to JSON file
        """
        path = Path(filepath)
        path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(path, 'w') as f:
            json.dump(data, f, indent=2)
    
    @classmethod
    def get_user_by_role(cls, role: str) -> Optional[UserData]:
        """
        Get user data by role.
        
        Args:
            role (str): User role ('valid', 'invalid', 'admin')
            
        Returns:
            Optional[UserData]: User data or None
        """
        role_map = {
            'valid': cls.VALID_USER,
            'invalid': cls.INVALID_USER,
            'admin': cls.ADMIN_USER,
            'empty': cls.EMPTY_CREDENTIALS,
        }
        return role_map.get(role.lower())
    
    @classmethod
    def get_browser_config(cls, browser: str) -> Optional[BrowserData]:
        """
        Get browser configuration by browser type.
        
        Args:
            browser (str): Browser type ('chrome', 'firefox', 'remote')
            
        Returns:
            Optional[BrowserData]: Browser configuration or None
        """
        browser_map = {
            'chrome': cls.CHROME_CONFIG,
            'firefox': cls.FIREFOX_CONFIG,
            'remote': cls.REMOTE_CHROME_CONFIG,
        }
        return browser_map.get(browser.lower())


class TestDataFactory:
    """
    Factory class for creating test data dynamically.
    
    Use this when you need to generate test data on-the-fly
    rather than using predefined data.
    """
    
    @staticmethod
    def create_user(
        username: str = "testuser",
        password: str = "TestPass123!",
        **kwargs
    ) -> UserData:
        """Create a user with custom attributes."""
        return UserData(username=username, password=password, **kwargs)
    
    @staticmethod
    def create_browser_config(
        browser_type: str = "chrome",
        **kwargs
    ) -> BrowserData:
        """Create a browser configuration."""
        return BrowserData(browser_type=browser_type, **kwargs)
    
    @staticmethod
    def create_url_data(base_url: str, **kwargs) -> URLData:
        """Create URL data."""
        return URLData(base_url=base_url, **kwargs)
    
    @staticmethod
    def create_search_data(query: str, **kwargs) -> SearchData:
        """Create search data."""
        return SearchData(query=query, **kwargs)
