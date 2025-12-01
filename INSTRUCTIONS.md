# SeleniumOrchestrator - AI Agent Instructions

**Version:** 1.0.0  
**Last Updated:** December 1, 2025

---

## 📋 Purpose

This document provides comprehensive instructions for AI agents working with the **SeleniumOrchestrator** codebase. It explains the architecture, design patterns, code organization, and conventions to help AI agents understand, maintain, and extend this project effectively.

> **⚠️ CRITICAL:** When making ANY changes to the codebase, AI agents MUST update this INSTRUCTIONS.md file to reflect:
> - New features or modules added
> - Architectural changes
> - New design patterns introduced
> - Modified conventions or practices
> - Updated dependencies

---

## 🏗️ Architecture Overview

### Design Pattern: Hexagonal Architecture (Ports & Adapters)

SeleniumOrchestrator follows **Hexagonal Architecture** (also known as Ports & Adapters pattern) to maintain clean separation of concerns and high testability.

```
┌─────────────────────────────────────────────────────────────┐
│                        APPLICATION LAYER                     │
│  (profile_service.py, tab_service.py, element_service.py)   │
│                    Business Logic & Orchestration            │
└──────────────────────┬──────────────────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────────────────┐
│                        DOMAIN LAYER                          │
│              (driver.py, tab.py, ports.py)                   │
│            Core Business Entities & Interfaces               │
└──────────────────────┬──────────────────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────────────────┐
│                    INFRASTRUCTURE LAYER                      │
│  (selenium_session.py, browser_factory.py,                  │
│   driver_creator.py, browser_config_builder.py)             │
│              External Dependencies & Adapters                │
└─────────────────────────────────────────────────────────────┘
```

### Layer Responsibilities

#### 1. **Domain Layer** (`src/domain/`)
- **Purpose:** Contains core business entities and domain models
- **Files:**
  - `driver.py`: Defines `DefaultDriverStatus` enum (OPEN, CLOSED)
  - `tab.py`: Defines `Tab` entity with status management
  - **Key Principle:** No external dependencies, pure domain logic

#### 2. **Core Layer** (`src/core/`)
- **Purpose:** Defines ports (interfaces) for the application
- **Files:**
  - `ports.py`: Contains `BrowserSessionPort` (abstract interface), `Locator` class, and `WaitCondition` constants
- **Key Principle:** Defines contracts that infrastructure must implement

#### 3. **Infrastructure Layer** (`src/infra/`)
- **Purpose:** Implements ports using external libraries (Selenium)
- **Files:**
  - `selenium_session.py`: Implements `BrowserSessionPort` using Selenium WebDriver
  - `browser_factory.py`: Factory pattern for creating different browser drivers
  - `driver_creator.py`: Static methods to instantiate Chrome, Firefox, and Remote drivers
  - `browser_config_builder.py`: Builder pattern for browser configuration
- **Key Principle:** All Selenium-specific code lives here

#### 4. **Application Layer** (`src/application/`)
- **Purpose:** Orchestrates business logic and provides high-level services
- **Files:**
  - `profile_service.py`: Manages browser profiles (collections of drivers)
  - `tab_service.py`: Manages tabs within a browser session
  - `element_service.py`: Provides high-level element interaction methods
- **Key Principle:** Coordinates domain objects and infrastructure

#### 5. **Utils Layer** (`src/utils/`)
- **Purpose:** Cross-cutting concerns and utilities
- **Files:**
  - `exceptions.py`: Custom exception hierarchy
  - `logger.py`: Logging configuration with sensitive data filtering
  - `settings.py`: Application settings and paths
  - `validators.py`: (Currently empty, reserved for validation logic)

---

## 🔑 Key Design Patterns

### 1. **Factory Pattern**
**Location:** `src/infra/browser_factory.py`

```python
class BrowserFactory:
    def __init__(self):
        self.driver_map = {
            "chrome": DriverCreator.create_chrome_driver,
            "firefox": DriverCreator.create_firefox_driver,
            "remote": DriverCreator.create_remote_driver,
        }
```

**Purpose:** Abstracts driver creation logic, making it easy to add new browser types.

**When Adding New Browsers:**
1. Add static method in `DriverCreator`
2. Register in `driver_map` dictionary
3. Update `BrowserConfigBuilder.BROWSER_OPTIONS_MAP` if needed

### 2. **Builder Pattern**
**Location:** `src/infra/browser_config_builder.py`

```python
options = BrowserConfigBuilder('chrome')
    .set_no_sandbox()
    .disable_dev_shm_usage()
    .set_browser_profile('./profiles/test_profile')
    .build()
```

**Purpose:** Provides fluent API for constructing complex browser configurations.

**When Adding New Options:**
- Add method that modifies `self.options` and returns `self`
- Maintain chainability pattern

### 3. **Service Layer Pattern**
**Location:** `src/application/*_service.py`

**Purpose:** Encapsulates business logic and provides high-level APIs.

**Services:**
- `ProfileService`: Manages multiple browser profiles
- `TabService`: Handles tab lifecycle (create, switch, close)
- `ElementService`: Abstracts element interactions (click, send_keys, find)

### 4. **Repository Pattern (Implicit)**
**Location:** `src/application/profile_service.py`

```python
class ProfileService:
    def __init__(self):
        self.profiles: Dict[str, Profile] = {}  # In-memory repository
```

**Purpose:** Manages profile instances with CRUD-like operations.

---

## 📦 Core Components Explained

### Profile Management

**Concept:** A "Profile" represents a browser instance with its configuration, tabs, and services.

```python
profile = profile_service.new_profile(
    driver_name='test_driver',        # Unique identifier
    tab_name='initial_tab',           # Name of first tab
    session=session,                  # SeleniumSession instance
    profile_options=options,          # Browser configuration
    connection=chrome_connections     # Driver connection info
)
```

**Access Points:**
- `profile.session`: Direct Selenium WebDriver access
- `profile.tab_service`: Tab management
- `profile.element_service`: Element interactions

### Tab Management

**Key Feature:** Named tabs instead of window handles.

Traditional Selenium:
```python
driver.switch_to.window("CDwindow-ABC123")  # Cryptic handle
```

SeleniumOrchestrator:
```python
profile.tab_service.switch_to("login_tab")  # Human-readable name
```

**Tab States:**
- `ACTIVE`: Currently focused tab
- `INACTIVE`: Background tab

### Element Locating

**Locator Class:**
```python
from src.core.ports import Locator
from selenium.webdriver.common.by import By

locator = Locator(By.ID, "username")
```

**Wait Conditions:** Defined in `WaitCondition` class (see `src/core/ports.py`)

**Usage:**
```python
profile.element_service.click(locator)
profile.element_service.send_keys(locator, "text")
elements = profile.element_service.find_all(locator)
```

---

## 🛠️ Exception Handling

### Exception Hierarchy

```
SeleniumWrapperException (Base)
├── BrowserInitializationError
├── TabManagementError
├── DriverNotFoundError
├── BrowserConfigError
└── InvalidTabOperationError
```

**Auto-Logging:** All exceptions automatically log with stack traces.

**Adding New Exceptions:**
1. Inherit from `SeleniumWrapperException`
2. Call `self.log_exception()` in `__init__`
3. Provide meaningful error messages

---

## 📝 Logging System

**Configuration:** `src/utils/logger.py`

**Features:**
- Dual output: File (`selenium_orchestrator.log`) + Console
- Sensitive data filtering (passwords, tokens)
- Pattern-based masking

**Filters:**
- `SensitiveDataFilter`: Excludes log entries with sensitive keywords
- `MaskingFilter`: Masks sensitive patterns with regex

**Usage:**
```python
from src.utils.logger import logger

logger.info("Safe message")
logger.error("Error occurred", exc_info=True)  # With stack trace
```

---

## 🔌 Connection Configuration

### Local Drivers

```python
chrome_connections = {
    'browser_type': 'chrome',
    'binary_path': '/path/to/chromedriver'
}
```

### Remote Drivers

```python
remote_connections = {
    'browser_type': 'remote',
    'remote_url': 'http://localhost:4444/wd/hub',
}
```

**Note:** For remote drivers, `profile_options` should match the remote browser type (e.g., Chrome standalone → Chrome options).

---

## 📐 Page Object Model (POM) Pattern

**Added:** Version 1.1.0 - December 1, 2025

### What is POM?

The Page Object Model is a design pattern that creates an object repository for web UI elements. It provides:
- **Separation of concerns**: Test logic separate from page implementation
- **Reusability**: Common page actions defined once, used everywhere
- **Maintainability**: UI changes require updates in one place only
- **Readability**: Tests read like user stories

### POM Architecture in SeleniumOrchestrator

```text
┌─────────────────────────────────────────────────────────┐
│                     Test Layer                          │
│              (examples/pom_example.py)                  │
└────────────────────┬────────────────────────────────────┘
                     │ uses
┌────────────────────▼────────────────────────────────────┐
│                  Page Objects Layer                     │
│         (src/pages/login_page, home_page, etc.)         │
│                                                         │
│  ┌──────────────────────────────────────────────────┐  │
│  │            BasePage (base_page.py)               │  │
│  │  - Common navigation methods                     │  │
│  │  - Element interaction wrappers                  │  │
│  │  - Wait conditions                               │  │
│  │  - JavaScript execution                          │  │
│  └──────────────────────────────────────────────────┘  │
│         ▲                  ▲                  ▲          │
│         │                  │                  │          │
│  ┌──────┴──────┐   ┌──────┴──────┐   ┌──────┴──────┐  │
│  │ LoginPage   │   │  HomePage   │   │  YourPage   │  │
│  │             │   │             │   │   (custom)  │  │
│  │ - Locators  │   │ - Locators  │   │ - Locators  │  │
│  │ - Actions   │   │ - Actions   │   │ - Actions   │  │
│  │ - Verifiers │   │ - Verifiers │   │ - Verifiers │  │
│  └─────────────┘   └─────────────┘   └─────────────┘  │
└────────────────────┬────────────────────────────────────┘
                     │ uses
┌────────────────────▼────────────────────────────────────┐
│              Application Layer                          │
│   (ElementService, TabService, SeleniumSession)         │
└─────────────────────────────────────────────────────────┘
```

### POM Components

#### 1. BasePage (`src/pages/base_page.py`)

**Purpose:** Provides common functionality inherited by all page objects.

**Key Features:**
- Navigation methods (navigate, refresh, go_back, go_forward)
- Element interaction (click, type, clear, clear_and_type)
- Element queries (find_element, find_elements, get_text, get_attribute)
- State verification (is_visible, is_clickable, is_present)
- JavaScript execution (execute_script, scroll methods)
- Wait conditions (wait_for_url_to_contain, wait_for_title_to_contain)
- Screenshots (take_screenshot, take_element_screenshot)

**Usage Pattern:**
```python
class YourPage(BasePage):
    def __init__(self, session, base_url="https://example.com"):
        super().__init__(session)
        self.url = f"{base_url}/your-path"
```

#### 2. Page Objects (LoginPage, HomePage, etc.)

**Structure:** Each page object should contain:

**A. Locators Section:**
```python
# Define as class-level constants
USERNAME_INPUT = Locator(By.ID, "username")
PASSWORD_INPUT = Locator(By.CSS_SELECTOR, "input[type='password']")
LOGIN_BUTTON = Locator(By.XPATH, "//button[@type='submit']")
```

**B. Actions Section:**
```python
def enter_username(self, username: str) -> None:
    """Enter username into the username field."""
    self.clear_and_type(self.USERNAME_INPUT, username)

def click_login_button(self) -> None:
    """Click the login button."""
    self.click(self.LOGIN_BUTTON)
```

**C. Composite Actions:**
```python
def login(self, username: str, password: str) -> None:
    """Perform complete login action."""
    self.enter_username(username)
    self.enter_password(password)
    self.click_login_button()
```

**D. Verification Methods:**
```python
def is_logged_in(self) -> bool:
    """Check if user is successfully logged in."""
    return self.wait_for_url_to_contain("dashboard", timeout=10)

def get_error_message(self) -> str:
    """Get the error message text."""
    return self.get_text(self.ERROR_MESSAGE)
```

### Using POM in Tests

**Traditional Approach (Without POM):**
```python
# Hard to read, tightly coupled to implementation
driver.find_element(By.ID, "username").send_keys("user")
driver.find_element(By.ID, "password").send_keys("pass")
driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
WebDriverWait(driver, 10).until(EC.url_contains("dashboard"))
```

**POM Approach:**
```python
# Readable, maintainable, reusable
login_page = LoginPage(session)
login_page.navigate()
login_page.login("user", "pass")
assert login_page.is_logged_in()
```

### Creating New Page Objects

**Step-by-Step Guide:**

1. **Create new file in `src/pages/`:**
   ```python
   # src/pages/checkout_page.py
   from selenium.webdriver.common.by import By
   from .base_page import BasePage
   from ..core.ports import Locator
   ```

2. **Define class inheriting from BasePage:**
   ```python
   class CheckoutPage(BasePage):
       def __init__(self, session, base_url="https://example.com"):
           super().__init__(session)
           self.url = f"{base_url}/checkout"
   ```

3. **Add locators:**
   ```python
   # Locators
   FIRST_NAME_INPUT = Locator(By.ID, "firstName")
   LAST_NAME_INPUT = Locator(By.ID, "lastName")
   SUBMIT_BUTTON = Locator(By.CSS_SELECTOR, "button[type='submit']")
   ```

4. **Add action methods:**
   ```python
   def fill_checkout_form(self, first_name: str, last_name: str) -> None:
       self.clear_and_type(self.FIRST_NAME_INPUT, first_name)
       self.clear_and_type(self.LAST_NAME_INPUT, last_name)
       self.click(self.SUBMIT_BUTTON)
   ```

5. **Add verification methods:**
   ```python
   def is_checkout_complete(self) -> bool:
       return self.wait_for_url_to_contain("confirmation")
   ```

6. **Register in `src/pages/__init__.py`:**
   ```python
   from .checkout_page import CheckoutPage
   
   __all__ = [
       'BasePage',
       'LoginPage',
       'HomePage',
       'CheckoutPage',  # Add your page here
   ]
   ```

7. **Update this INSTRUCTIONS.md file**

### POM Best Practices

1. **One Page Object per Page/Component:** Create separate page objects for distinct pages or major components

2. **Locators as Constants:** Define all locators at class level using descriptive names

3. **Action Methods Return None:** Methods that perform actions typically return None

4. **Verification Methods Return Bool/Data:** Methods that check state return boolean or data

5. **Composite Actions:** Combine atomic actions into higher-level operations

6. **Meaningful Method Names:** Use clear, action-oriented names (e.g., `click_login_button`, not `click`)

7. **Wait Implicitly:** Build waits into page objects, not in tests

8. **No Assertions in Page Objects:** Page objects verify state; tests make assertions

9. **Keep Tests Clean:** Tests should read like documentation

10. **Document Complex Locators:** Add comments for XPath or complex CSS selectors

### POM Examples

See `examples/pom_example.py` for complete working examples:
- `test_login_with_pom()`: Login workflow
- `test_search_with_pom()`: Search functionality
- `test_add_to_cart_with_pom()`: E-commerce interactions
- `test_navigation_with_pom()`: Page navigation patterns

---

## 📂 File Organization

```
SeleniumOrchestrator/
├── src/
│   ├── domain/          # Business entities (Tab, Driver status)
│   ├── core/            # Interfaces/ports (BrowserSessionPort)
│   ├── infra/           # Selenium implementations
│   ├── application/     # High-level services
│   ├── pages/           # Page Object Model (POM) classes
│   │   ├── base_page.py      # Base page with common functionality
│   │   ├── login_page.py     # Example login page object
│   │   └── home_page.py      # Example home page object
│   └── utils/           # Cross-cutting concerns
├── tests/               # Test suite (pytest)
│   ├── conftest.py           # Pytest fixtures and configuration
│   ├── unit/                 # Unit tests
│   ├── integration/          # Integration tests
│   ├── e2e/                  # End-to-end tests
│   ├── test_data/            # Test data management
│   ├── fixtures/             # Additional fixtures
│   ├── logs/                 # Test logs (auto-generated)
│   └── screenshots/          # Failure screenshots (auto-generated)
├── examples/            # Usage examples
│   ├── initialize_chrome.py   # Chrome driver setup example
│   ├── initialize_firefox.py  # Firefox driver setup example
│   ├── initialize_remote.py   # Remote driver setup example
│   └── pom_example.py         # Page Object Model usage examples
├── requirements/        # Dependency specifications
│   ├── base-requirements.txt  # Core dependencies
│   └── test-requirements.txt  # Testing dependencies
├── pytest.ini          # Pytest configuration
├── main.py             # Entry point example
├── README.md           # User-facing documentation
└── INSTRUCTIONS.md     # This file (AI agent reference)
```

---

## 🧪 Testing Framework

**Added:** Version 1.2.0 - December 1, 2025

### Overview

SeleniumOrchestrator now includes a comprehensive test suite built with **pytest**, covering:
- Unit tests for domain and core layers
- Integration tests for infrastructure components
- End-to-end tests using Page Object Model
- Centralized test data management
- Extensive fixtures and utilities

### Test Structure

```
tests/
├── conftest.py                    # Pytest configuration and fixtures
├── pytest.ini                     # Pytest settings (in project root)
├── README.md                      # Complete testing documentation
├── unit/                          # Unit tests (fast, isolated)
│   ├── test_tab.py               # Tab entity tests
│   ├── test_driver.py            # Driver status tests
│   ├── test_locator.py           # Locator class tests
│   └── test_browser_config_builder.py  # Builder pattern tests
├── integration/                   # Integration tests (with mocks)
│   ├── test_browser_factory.py   # Factory pattern tests
│   └── test_selenium_session.py  # Session lifecycle tests
├── e2e/                          # End-to-end tests (full automation)
│   └── test_pom_workflows.py     # POM-based workflow tests
├── fixtures/                      # Additional fixtures
├── test_data/                     # Test data management
│   ├── test_data.py              # TestData classes
│   ├── test_config.json          # JSON configuration
│   └── __init__.py
├── logs/                         # Test execution logs
└── screenshots/                  # Failure screenshots (auto-generated)
```

### Test Categories

Tests are organized by **pytest markers**:

| Marker | Description | Speed | Use Case |
|--------|-------------|-------|----------|
| `@pytest.mark.unit` | Unit tests | Very Fast | Domain, core logic |
| `@pytest.mark.integration` | Integration tests | Medium | Infrastructure with mocks |
| `@pytest.mark.e2e` | End-to-end tests | Slow | Full browser workflows |
| `@pytest.mark.smoke` | Smoke tests | Fast | Critical paths |
| `@pytest.mark.slow` | Long-running tests | Very Slow | Performance, stress |
| `@pytest.mark.browser_chrome` | Chrome-specific | - | Chrome driver required |
| `@pytest.mark.browser_firefox` | Firefox-specific | - | Firefox driver required |

### Running Tests

**Install test dependencies:**
```bash
pip install -r requirements/test-requirements.txt
```

**Run all tests:**
```bash
pytest
```

**Run by category:**
```bash
pytest -m unit           # Only unit tests
pytest -m integration    # Only integration tests
pytest -m e2e            # Only E2E tests
pytest -m "unit or integration"  # Multiple categories
```

**Run with coverage:**
```bash
pytest --cov=src --cov-report=html
```

**Run specific file:**
```bash
pytest tests/unit/test_tab.py
```

**Run in parallel:**
```bash
pytest -n 4  # 4 workers
```

### Test Data Management

**Centralized Test Data:**
All test data is managed in `tests/test_data/test_data.py`:

```python
from tests.test_data import TestData

# Access predefined test data
user = TestData.VALID_USER
browser = TestData.CHROME_CONFIG
urls = TestData.DEMO_QA_URLS

# Get by role
admin = TestData.get_user_by_role('admin')
```

**Test Data Classes:**
- `UserData`: User credentials and information
- `BrowserData`: Browser configurations
- `URLData`: URL endpoints
- `SearchData`: Search test data
- `ElementData`: Element locators

**TestDataFactory:**
For dynamic test data creation:

```python
from tests.test_data import TestDataFactory

user = TestDataFactory.create_user(
    username="custom",
    password="CustomPass123!"
)
```

### Pytest Fixtures

**Available fixtures** (defined in `conftest.py`):

**Test Data Fixtures:**
- `test_data` - Access to TestData class
- `test_config` - JSON configuration

**Browser Configuration:**
- `chrome_options` - Chrome browser options
- `firefox_options` - Firefox options
- `headless_chrome_options` - Headless Chrome
- `chrome_connection` - Chrome connection config
- `firefox_connection` - Firefox connection config

**Browser Sessions:**
- `browser_session` - Empty session (lightweight)
- `chrome_browser` - Initialized Chrome session
- `firefox_browser` - Initialized Firefox session
- `chrome_profile` - Full Chrome profile with services

**Mocks:**
- `mock_driver` - Mocked WebDriver
- `mock_element` - Mocked WebElement

**Utilities:**
- `assert_helper` - Custom assertions
- `screenshot_dir` - Screenshots directory
- `log_dir` - Logs directory

### Writing Tests

**Unit Test Example:**
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

**Integration Test Example:**
```python
from unittest.mock import Mock, patch

@patch('src.infra.browser_factory.DriverCreator.create_chrome_driver')
def test_factory_creates_chrome(mock_create):
    mock_create.return_value = Mock()
    
    factory = BrowserFactory()
    result = factory.create_browser('chrome', Mock(), {})
    
    assert result is not None
    mock_create.assert_called_once()
```

**E2E Test Example:**
```python
@pytest.mark.e2e
@pytest.mark.skip(reason="Requires real browser")
def test_login_workflow(browser_session, test_data):
    login_page = LoginPage(browser_session)
    login_page.navigate()
    login_page.login(test_data.VALID_USER.username, test_data.VALID_USER.password)
    
    assert login_page.is_logged_in()
```

**Parametrized Test:**
```python
@pytest.mark.parametrize("username,password", [
    ("user1", "pass1"),
    ("user2", "pass2"),
])
def test_multiple_logins(username, password):
    # Test with different credentials
    pass
```

### Test Configuration

**pytest.ini** (project root):
- Test discovery patterns
- Markers definition
- Logging configuration
- Coverage settings

**conftest.py** (tests directory):
- Shared fixtures
- Pytest hooks
- Auto-screenshot on failure
- Custom assertions

### Coverage

**Generate coverage report:**
```bash
pytest --cov=src --cov-report=html --cov-report=term
```

**View HTML report:**
```bash
open htmlcov/index.html
```

**Coverage target:** Aim for >80% code coverage

### Best Practices

1. **Test Independence:** Each test should run in isolation
2. **Use Proper Markers:** Mark tests appropriately
3. **AAA Pattern:** Arrange, Act, Assert
4. **Descriptive Names:** Clear test method names
5. **Mock External Deps:** Use mocks for integration tests
6. **Clean Up:** Use fixtures with proper cleanup
7. **Centralize Test Data:** Use TestData classes
8. **Document Tests:** Add docstrings
9. **Avoid Hard-coding:** Use configuration
10. **Review Coverage:** Check coverage reports

### CI/CD Integration

**GitHub Actions example:**
```yaml
- name: Run tests
  run: |
    pytest -m unit --cov=src --cov-report=xml

- name: Upload coverage
  uses: codecov/codecov-action@v2
```

**Skip tests in CI:**
```python
@pytest.mark.skip_ci
def test_local_only():
    pass
```

### Debugging Tests

**Run with debugger:**
```bash
pytest --pdb  # Drop to debugger on failure
pytest -x --pdb  # Stop on first failure
```

**View logs:**
```bash
cat tests/logs/pytest.log
tail -f tests/logs/pytest.log  # Real-time
```

**Screenshots:**
Automatically captured on E2E test failures in `tests/screenshots/`

### Testing Strategy

- **Unit Tests:** Test domain and application logic without Selenium
- **Integration Tests:** Test infrastructure layer with mocked dependencies
- **E2E Tests:** Full workflow validation with real browsers

---

## 📋 Coding Conventions

### Naming Conventions

- **Classes:** PascalCase (e.g., `ProfileService`, `BrowserFactory`)
- **Functions/Methods:** snake_case (e.g., `new_profile`, `switch_tab`)
- **Constants:** UPPER_SNAKE_CASE (e.g., `DEFAULT_TIMEOUT`)
- **Private Methods:** Prefix with underscore (e.g., `_find`, `_locate`)

### Type Hints

**Required:** Use type hints for all public methods.

```python
def new_profile(
    self,
    driver_name: str,
    tab_name: str,
    session: SeleniumSession,
    profile_options: BrowserConfigBuilder,
    connection: dict
) -> Profile:
```

### Documentation

**Docstrings:** Recommended for public APIs (currently minimal in codebase).

**Comments:** Use sparingly, prefer self-documenting code.

---

## 🚀 Adding New Features

### Adding a New Browser Type

1. **Update `BrowserConfigBuilder`:**
   ```python
   BROWSER_OPTIONS_MAP = {
       "chrome": ChromeOptions,
       "safari": SafariOptions,  # New
   }
   ```

2. **Create Driver Method in `DriverCreator`:**
   ```python
   @staticmethod
   def create_safari_driver(options, connection):
       # Implementation
   ```

3. **Register in `BrowserFactory`:**
   ```python
   self.driver_map = {
       "safari": DriverCreator.create_safari_driver,
   }
   ```

4. **Update this INSTRUCTIONS.md file**

### Adding Element Interaction Methods

1. Add method to `ElementService`:
   ```python
   def double_click(self, locator: Locator, root_element=None):
       el = self._locate(locator, WaitCondition.ELEMENT_TO_BE_CLICKABLE)
       if el:
           ActionChains(self.session.driver).double_click(el).perform()
   ```

2. **Update this INSTRUCTIONS.md file**

### Adding Wait Conditions

1. Add constant to `WaitCondition` class in `src/core/ports.py`
2. Map to Selenium EC in `SeleniumSession.find_element`
3. **Update this INSTRUCTIONS.md file**

---

## 🔍 Debugging Tips

### Enable Verbose Logging

```python
from src.utils.logger import setup_logger
import logging

logger = setup_logger("SeleniumOrchestrator", level=logging.DEBUG)
```

### Accessing Raw Driver

```python
profile.session.driver  # Direct WebDriver instance
```

### Inspecting Tab State

```python
active_tab = profile.tab_service.get_active_tab()
print(active_tab)  # Shows name, handle, status
```

---

## 📚 Dependencies

**Key Libraries:**
- `selenium==4.22.0`: Core WebDriver functionality
- `chromedriver-py`: Chrome driver binary
- `webdriver-manager==4.0.1`: Automatic driver management

**Full List:** See `requirements/base-requirements.txt`

---

## 🔄 Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0   | 2025-12-01 | Initial documentation created |
| 1.1.0   | 2025-12-01 | Added Page Object Model (POM) structure with BasePage, LoginPage, HomePage, and usage examples |
| 1.2.0   | 2025-12-01 | Added comprehensive pytest testing framework with unit, integration, and E2E tests; TestData management; fixtures; and test utilities |

---

## 🤖 AI Agent Checklist

When modifying this codebase, ensure you:

- [ ] Follow the hexagonal architecture pattern
- [ ] Place code in the correct layer (domain/core/infra/application/pages/utils)
- [ ] Use appropriate design patterns (Factory, Builder, Service, POM)
- [ ] Add type hints to new methods
- [ ] Log exceptions using the custom exception classes
- [ ] For new page objects, inherit from BasePage and follow POM conventions
- [ ] Update `src/pages/__init__.py` when adding new page objects
- [ ] Write tests for new features (unit, integration, or E2E as appropriate)
- [ ] Update test data in `tests/test_data/test_data.py` if needed
- [ ] Use pytest markers appropriately (@pytest.mark.unit, etc.)
- [ ] Ensure tests pass locally before committing
- [ ] Update this INSTRUCTIONS.md file with changes
- [ ] Maintain backward compatibility where possible
- [ ] Test with Chrome, Firefox, and Remote configurations
- [ ] Update examples if public API changes

---

## 📞 Support & Questions

For questions about this codebase:

1. Review this INSTRUCTIONS.md thoroughly
2. Check examples in `examples/` directory
3. Examine test cases (when available)
4. Review README.md for user-facing documentation

---

**Remember:** This document is the source of truth for AI agents. Keep it updated!
