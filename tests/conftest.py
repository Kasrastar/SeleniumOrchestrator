"""
Pytest Configuration and Shared Fixtures

This file contains pytest configuration, fixtures, and hooks that are shared
across all tests in the test suite.

Fixtures defined here are automatically available to all test modules.
"""

import pytest
import os
import sys
from pathlib import Path
from typing import Dict, Generator
from datetime import datetime

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.infra.browser_config_builder import BrowserConfigBuilder
from src.infra.selenium_session import SeleniumSession
from src.application.profile_service import ProfileService
from tests.test_data import TestData, BrowserData


# ==================== Pytest Hooks ====================

def pytest_configure(config):
    """Pytest configuration hook - runs once before all tests."""
    # Create logs directory if it doesn't exist
    log_dir = Path("tests/logs")
    log_dir.mkdir(parents=True, exist_ok=True)
    
    # Create screenshots directory
    screenshot_dir = Path("tests/screenshots")
    screenshot_dir.mkdir(parents=True, exist_ok=True)
    
    print("\n" + "=" * 60)
    print("SeleniumOrchestrator Test Suite")
    print("=" * 60)


def pytest_collection_modifyitems(config, items):
    """Modify test items after collection."""
    # Add markers based on test path
    for item in items:
        if "unit" in str(item.fspath):
            item.add_marker(pytest.mark.unit)
        elif "integration" in str(item.fspath):
            item.add_marker(pytest.mark.integration)
        elif "e2e" in str(item.fspath):
            item.add_marker(pytest.mark.e2e)


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Hook to capture test results and take screenshots on failure."""
    outcome = yield
    report = outcome.get_result()
    
    # Take screenshot on failure for integration/e2e tests
    if report.when == "call" and report.failed:
        if hasattr(item, 'funcargs') and 'browser_session' in item.funcargs:
            session = item.funcargs['browser_session']
            if session and hasattr(session, 'driver') and session.driver:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                screenshot_name = f"{item.name}_{timestamp}.png"
                screenshot_path = Path("tests/screenshots") / screenshot_name
                try:
                    session.driver.save_screenshot(str(screenshot_path))
                    print(f"\nScreenshot saved: {screenshot_path}")
                except Exception as e:
                    print(f"\nFailed to save screenshot: {e}")


# ==================== Session Scope Fixtures ====================

@pytest.fixture(scope="session")
def test_data():
    """Provide access to centralized test data."""
    return TestData


@pytest.fixture(scope="session")
def project_root_dir():
    """Return the project root directory."""
    return project_root


@pytest.fixture(scope="session")
def test_config():
    """Load test configuration."""
    config_file = project_root / "tests" / "test_data" / "test_config.json"
    if config_file.exists():
        return TestData.load_from_json(str(config_file))
    return {}


# ==================== Browser Configuration Fixtures ====================

@pytest.fixture(scope="function")
def chrome_options():
    """Create Chrome browser options."""
    return (
        BrowserConfigBuilder('chrome')
        .set_no_sandbox()
        .disable_dev_shm_usage()
        .build()
    )


@pytest.fixture(scope="function")
def firefox_options():
    """Create Firefox browser options."""
    return (
        BrowserConfigBuilder('firefox')
        .set_headless()
        .build()
    )


@pytest.fixture(scope="function")
def headless_chrome_options():
    """Create headless Chrome browser options."""
    return (
        BrowserConfigBuilder('chrome')
        .set_headless()
        .set_no_sandbox()
        .disable_dev_shm_usage()
        .build()
    )


@pytest.fixture(scope="function")
def chrome_connection(test_data):
    """Create Chrome connection configuration."""
    browser_data = test_data.CHROME_CONFIG
    return browser_data.to_connection_dict()


@pytest.fixture(scope="function")
def firefox_connection(test_data):
    """Create Firefox connection configuration."""
    browser_data = test_data.FIREFOX_CONFIG
    return browser_data.to_connection_dict()


@pytest.fixture(scope="function")
def remote_connection(test_data):
    """Create remote connection configuration."""
    browser_data = test_data.REMOTE_CHROME_CONFIG
    return browser_data.to_connection_dict()


# ==================== Browser Session Fixtures ====================

@pytest.fixture(scope="function")
def browser_session():
    """
    Create a browser session (does not initialize driver).
    
    This is a lightweight fixture that just creates the session object.
    """
    session = SeleniumSession()
    yield session
    # Cleanup
    try:
        if session.driver:
            session.close()
    except Exception:
        pass


@pytest.fixture(scope="function")
def chrome_browser(chrome_options, chrome_connection):
    """
    Create and initialize a Chrome browser session.
    
    This fixture opens a real Chrome browser - use sparingly in unit tests.
    """
    session = SeleniumSession()
    try:
        session.open(
            browser_type='chrome',
            options=chrome_options,
            connection=chrome_connection
        )
        yield session
    finally:
        try:
            session.close()
        except Exception:
            pass


@pytest.fixture(scope="function")
def firefox_browser(firefox_options, firefox_connection):
    """
    Create and initialize a Firefox browser session.
    
    This fixture opens a real Firefox browser - use sparingly in unit tests.
    """
    session = SeleniumSession()
    try:
        session.open(
            browser_type='firefox',
            options=firefox_options,
            connection=firefox_connection
        )
        yield session
    finally:
        try:
            session.close()
        except Exception:
            pass


# ==================== Profile Service Fixtures ====================

@pytest.fixture(scope="function")
def profile_service():
    """Create a ProfileService instance."""
    return ProfileService()


@pytest.fixture(scope="function")
def chrome_profile(profile_service, browser_session, chrome_options, chrome_connection):
    """
    Create a Chrome profile with initialized browser.
    
    Returns a Profile object with session, tab_service, and element_service.
    """
    profile = profile_service.new_profile(
        driver_name='test_chrome',
        tab_name='main_tab',
        session=browser_session,
        profile_options=chrome_options,
        connection=chrome_connection
    )
    yield profile
    # Cleanup
    try:
        profile.close()
    except Exception:
        pass


# ==================== Mock Fixtures ====================

@pytest.fixture
def mock_driver(mocker):
    """Create a mock WebDriver instance."""
    mock = mocker.Mock()
    mock.current_window_handle = "mock-window-handle"
    mock.window_handles = ["mock-window-handle"]
    mock.title = "Mock Page Title"
    mock.current_url = "https://example.com"
    return mock


@pytest.fixture
def mock_element(mocker):
    """Create a mock WebElement instance."""
    mock = mocker.Mock()
    mock.text = "Mock Element Text"
    mock.is_displayed.return_value = True
    mock.is_enabled.return_value = True
    mock.is_selected.return_value = False
    return mock


# ==================== Utility Fixtures ====================

@pytest.fixture
def screenshot_dir():
    """Return the screenshots directory."""
    return Path("tests/screenshots")


@pytest.fixture
def log_dir():
    """Return the logs directory."""
    return Path("tests/logs")


@pytest.fixture(autouse=True)
def test_logger(caplog):
    """
    Automatically capture logs for all tests.
    
    This fixture is automatically used by all tests (autouse=True).
    """
    import logging
    caplog.set_level(logging.INFO)
    return caplog


# ==================== Parametrize Helpers ====================

@pytest.fixture
def browser_configs(test_data):
    """Provide list of browser configurations for parametrized tests."""
    return [
        ('chrome', test_data.CHROME_CONFIG),
        ('firefox', test_data.FIREFOX_CONFIG),
    ]


@pytest.fixture
def valid_users(test_data):
    """Provide list of valid users for parametrized tests."""
    return [
        test_data.VALID_USER,
        test_data.ADMIN_USER,
    ]


@pytest.fixture
def invalid_users(test_data):
    """Provide list of invalid users for parametrized tests."""
    return [
        test_data.INVALID_USER,
        test_data.EMPTY_CREDENTIALS,
    ]


# ==================== Conditional Skip Markers ====================

def pytest_runtest_setup(item):
    """Skip tests based on environment or conditions."""
    # Skip tests marked for CI if running in CI
    if item.get_closest_marker('skip_ci'):
        if os.getenv('CI') or os.getenv('CONTINUOUS_INTEGRATION'):
            pytest.skip("Skipped in CI environment")
    
    # Check for required browsers
    if item.get_closest_marker('browser_chrome'):
        chrome_config = TestData.CHROME_CONFIG
        if not Path(chrome_config.binary_path).exists():
            pytest.skip("Chrome driver not found")
    
    if item.get_closest_marker('browser_firefox'):
        firefox_config = TestData.FIREFOX_CONFIG
        if not Path(firefox_config.binary_path).exists():
            pytest.skip("Firefox driver not found")


# ==================== Custom Assertions ====================

class CustomAssertions:
    """Custom assertion helpers for tests."""
    
    @staticmethod
    def assert_element_visible(element, message="Element should be visible"):
        """Assert that an element is visible."""
        assert element is not None, f"{message} - Element is None"
        assert element.is_displayed(), message
    
    @staticmethod
    def assert_url_contains(driver, text, message="URL should contain text"):
        """Assert that current URL contains text."""
        assert text in driver.current_url, f"{message} - Expected '{text}' in '{driver.current_url}'"
    
    @staticmethod
    def assert_title_contains(driver, text, message="Title should contain text"):
        """Assert that page title contains text."""
        assert text in driver.title, f"{message} - Expected '{text}' in '{driver.title}'"


@pytest.fixture
def assert_helper():
    """Provide custom assertion helpers."""
    return CustomAssertions()
