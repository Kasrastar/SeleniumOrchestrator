# SeleniumOrchestrator Test Suite

Comprehensive test suite for the SeleniumOrchestrator project using pytest.

## 📋 Table of Contents

- [Overview](#overview)
- [Test Structure](#test-structure)
- [Installation](#installation)
- [Running Tests](#running-tests)
- [Test Categories](#test-categories)
- [Test Data Management](#test-data-management)
- [Writing Tests](#writing-tests)
- [CI/CD Integration](#cicd-integration)

## 🎯 Overview

This test suite provides comprehensive coverage of the SeleniumOrchestrator framework with:

- **Unit Tests**: Fast tests for individual components (domain, core, application layers)
- **Integration Tests**: Tests for infrastructure components with mocked dependencies
- **E2E Tests**: Full workflow tests using the Page Object Model pattern
- **Test Data Management**: Centralized test data with easy configuration
- **Fixtures**: Reusable pytest fixtures for common setup
- **Reporting**: HTML reports, coverage reports, and logging

## 📁 Test Structure

```
tests/
├── conftest.py              # Pytest configuration and shared fixtures
├── pytest.ini               # Pytest settings (moved to project root)
├── unit/                    # Unit tests (fast, no external dependencies)
│   ├── test_tab.py
│   ├── test_driver.py
│   ├── test_locator.py
│   └── test_browser_config_builder.py
├── integration/             # Integration tests (with mocked Selenium)
│   ├── test_browser_factory.py
│   └── test_selenium_session.py
├── e2e/                     # End-to-end tests (full browser automation)
│   └── test_pom_workflows.py
├── fixtures/                # Additional test fixtures
├── test_data/               # Test data management
│   ├── __init__.py
│   ├── test_data.py         # TestData classes and utilities
│   └── test_config.json     # JSON configuration for test data
├── logs/                    # Test execution logs
└── screenshots/             # Failure screenshots (auto-generated)
```

## 🚀 Installation

### 1. Install Test Dependencies

```bash
pip install -r requirements/test-requirements.txt
```

### 2. Update Test Configuration

Edit `tests/test_data/test_data.py` to update:
- Browser driver paths
- Test URLs
- User credentials
- Timeout values

Or edit `tests/test_data/test_config.json` for JSON-based configuration.

## ▶️ Running Tests

### Run All Tests

```bash
pytest
```

### Run Specific Test Categories

```bash
# Run only unit tests (fast)
pytest -m unit

# Run only integration tests
pytest -m integration

# Run only E2E tests (slow)
pytest -m e2e

# Run smoke tests
pytest -m smoke
```

### Run Tests by Directory

```bash
# Run all unit tests
pytest tests/unit/

# Run all integration tests
pytest tests/integration/

# Run all E2E tests
pytest tests/e2e/
```

### Run Specific Test File

```bash
pytest tests/unit/test_tab.py
```

### Run Specific Test Method

```bash
pytest tests/unit/test_tab.py::TestTab::test_tab_creation
```

### Run with Coverage

```bash
# Generate coverage report
pytest --cov=src --cov-report=html

# View report
open htmlcov/index.html
```

### Run with HTML Report

```bash
pytest --html=tests/logs/report.html --self-contained-html
```

### Run in Parallel

```bash
# Run with 4 workers
pytest -n 4
```

### Run with Verbose Output

```bash
pytest -v
pytest -vv  # Extra verbose
```

## 🏷️ Test Categories

Tests are marked with pytest markers for easy filtering:

| Marker | Description | Speed | Dependencies |
|--------|-------------|-------|--------------|
| `unit` | Unit tests | Fast | None |
| `integration` | Integration tests | Medium | Mocked Selenium |
| `e2e` | End-to-end tests | Slow | Real browser |
| `smoke` | Critical path tests | Fast | Varies |
| `regression` | Full regression suite | Slow | All |
| `slow` | Long-running tests | Very Slow | Varies |
| `browser_chrome` | Requires Chrome | - | Chrome driver |
| `browser_firefox` | Requires Firefox | - | Firefox driver |
| `browser_remote` | Requires remote driver | - | Remote setup |
| `skip_ci` | Skip in CI | - | - |
| `flaky` | May be flaky | - | - |

### Examples

```bash
# Run only fast unit tests
pytest -m unit

# Run smoke tests
pytest -m smoke

# Run all tests except slow ones
pytest -m "not slow"

# Run Chrome-specific tests
pytest -m browser_chrome

# Run integration and E2E tests
pytest -m "integration or e2e"
```

## 📊 Test Data Management

### Using TestData Class

```python
from tests.test_data import TestData

# Access predefined test data
user = TestData.VALID_USER
browser = TestData.CHROME_CONFIG
urls = TestData.DEMO_QA_URLS

# Get test data by role
admin = TestData.get_user_by_role('admin')
chrome = TestData.get_browser_config('chrome')
```

### Using TestDataFactory

```python
from tests.test_data import TestDataFactory

# Create custom test data dynamically
user = TestDataFactory.create_user(
    username="custom_user",
    password="CustomPass123!"
)

browser = TestDataFactory.create_browser_config(
    browser_type="firefox",
    binary_path="/custom/path"
)
```

### Loading from JSON

```python
from tests.test_data import TestData

# Load configuration from JSON
config = TestData.load_from_json('tests/test_data/test_config.json')

# Save configuration to JSON
TestData.save_to_json(config, 'output.json')
```

## ✍️ Writing Tests

### Unit Test Example

```python
import pytest
from src.domain.tab import Tab, DefaultTabStatus

class TestTab:
    def test_tab_creation(self):
        """Test creating a new tab."""
        tab = Tab("test_tab", "handle-123", DefaultTabStatus.ACTIVE)
        
        assert tab.name == "test_tab"
        assert tab.is_active()
```

### Integration Test Example

```python
import pytest
from unittest.mock import Mock, patch
from src.infra.browser_factory import BrowserFactory

class TestBrowserFactory:
    @patch('src.infra.browser_factory.DriverCreator.create_chrome_driver')
    def test_creates_chrome_browser(self, mock_create):
        mock_create.return_value = Mock()
        
        factory = BrowserFactory()
        result = factory.create_browser('chrome', Mock(), {})
        
        assert result is not None
        mock_create.assert_called_once()
```

### E2E Test Example

```python
import pytest
from src.pages import LoginPage
from tests.test_data import TestData

@pytest.mark.e2e
@pytest.mark.skip(reason="Requires real browser")
class TestLoginFlow:
    def test_successful_login(self, browser_session):
        login_page = LoginPage(browser_session)
        user = TestData.VALID_USER
        
        login_page.navigate()
        login_page.login(user.username, user.password)
        
        assert login_page.is_logged_in()
```

### Using Fixtures

```python
@pytest.fixture
def user_data(test_data):
    """Provide user data for tests."""
    return test_data.VALID_USER

def test_with_fixture(user_data):
    """Test using fixture."""
    assert user_data.username == "testuser"
```

### Parametrized Tests

```python
@pytest.mark.parametrize("username,password", [
    ("user1", "pass1"),
    ("user2", "pass2"),
    ("user3", "pass3"),
])
def test_multiple_users(username, password):
    """Test with multiple user combinations."""
    # Test logic here
    pass
```

## 🔧 Test Fixtures

### Available Fixtures

All fixtures are defined in `tests/conftest.py`:

#### Test Data Fixtures
- `test_data` - Access to TestData class
- `test_config` - Loaded JSON configuration
- `project_root_dir` - Project root directory

#### Browser Configuration Fixtures
- `chrome_options` - Chrome browser options
- `firefox_options` - Firefox browser options
- `headless_chrome_options` - Headless Chrome options
- `chrome_connection` - Chrome connection config
- `firefox_connection` - Firefox connection config
- `remote_connection` - Remote connection config

#### Browser Session Fixtures
- `browser_session` - Empty session object
- `chrome_browser` - Initialized Chrome session
- `firefox_browser` - Initialized Firefox session

#### Service Fixtures
- `profile_service` - ProfileService instance
- `chrome_profile` - Chrome profile with session

#### Mock Fixtures
- `mock_driver` - Mocked WebDriver
- `mock_element` - Mocked WebElement

#### Utility Fixtures
- `screenshot_dir` - Screenshots directory
- `log_dir` - Logs directory
- `assert_helper` - Custom assertions

## 📈 Coverage

### Generate Coverage Report

```bash
pytest --cov=src --cov-report=html --cov-report=term
```

### Coverage Configuration

Coverage settings are in `pytest.ini`:
- Source: `src/` directory
- Omit: tests, venv, __pycache__
- Precision: 2 decimal places

### View HTML Coverage Report

```bash
open htmlcov/index.html  # macOS
xdg-open htmlcov/index.html  # Linux
start htmlcov/index.html  # Windows
```

## 🔄 CI/CD Integration

### GitHub Actions Example

```yaml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v2
    
    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: '3.9'
    
    - name: Install dependencies
      run: |
        pip install -r requirements/test-requirements.txt
    
    - name: Run unit tests
      run: |
        pytest -m unit --cov=src --cov-report=xml
    
    - name: Upload coverage
      uses: codecov/codecov-action@v2
```

### Skip Tests in CI

Mark tests to skip in CI:

```python
@pytest.mark.skip_ci
def test_local_only():
    """This test only runs locally."""
    pass
```

## 🐛 Debugging

### Run Tests with Debugging

```bash
# Use pytest's built-in debugger
pytest --pdb

# Drop into debugger on first failure
pytest -x --pdb

# Use ipdb (if installed)
pytest --pdbcls=IPython.terminal.debugger:TerminalPdb
```

### View Logs

Logs are automatically saved to `tests/logs/pytest.log`.

```bash
# View logs
cat tests/logs/pytest.log

# Tail logs in real-time
tail -f tests/logs/pytest.log
```

### Screenshots on Failure

Screenshots are automatically captured on E2E test failures and saved to `tests/screenshots/`.

## 📝 Best Practices

1. **Keep tests independent**: Each test should be able to run in isolation
2. **Use appropriate markers**: Mark tests with correct categories
3. **Follow AAA pattern**: Arrange, Act, Assert
4. **Use descriptive names**: Test names should explain what they test
5. **Mock external dependencies**: Use mocks for integration tests
6. **Clean up resources**: Use fixtures with cleanup
7. **Update test data**: Keep test data centralized and documented
8. **Write documentation**: Add docstrings to test classes and methods
9. **Avoid hard-coded values**: Use test data classes
10. **Review coverage**: Aim for >80% code coverage

## 🔗 Related Documentation

- **INSTRUCTIONS.md**: Complete codebase documentation
- **README.md**: Project documentation
- **pytest.ini**: Pytest configuration
- **conftest.py**: Fixture definitions

## 🤝 Contributing

When adding new tests:

1. Place tests in appropriate directory (unit/integration/e2e)
2. Use proper markers (@pytest.mark.unit, etc.)
3. Update test data if needed
4. Add fixtures to conftest.py if reusable
5. Update this README if adding new patterns
6. Run tests locally before committing
7. Ensure coverage doesn't decrease

## 📞 Troubleshooting

### Common Issues

**Issue**: Import errors
**Solution**: Ensure project root is in PYTHONPATH (pytest.ini handles this)

**Issue**: Driver not found
**Solution**: Update driver paths in `tests/test_data/test_data.py`

**Issue**: Tests hanging
**Solution**: Use `--timeout=300` flag or check browser driver setup

**Issue**: Flaky tests
**Solution**: Use `@pytest.mark.flaky` and `pytest-rerunfailures`

**Issue**: No coverage report
**Solution**: Install `pytest-cov`: `pip install pytest-cov`

---

**Happy Testing! 🎉**
