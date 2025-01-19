
# SeleniumOrchestrator

**SeleniumOrchestrator** is a powerful and flexible Python-based Selenium wrapper designed to simplify and optimize your Selenium testing workflow. This project addresses the challenges and complexities often associated with Selenium, such as driver initialization, tab and session management, and robust exception handling. With **SeleniumOrchestrator**, you can focus on your test scenarios while leaving the intricacies of Selenium management to the framework.

## Key Features

### 1. **Simplified Driver Initialization**
   - **Browser Configuration Support**: Instead of manually configuring each browser driver, **SeleniumOrchestrator** handles the initialization of both local and remote drivers with comprehensive configuration options.
   - **Automatic Driver Management**: The project handles the complexities of initializing both local and remote browsers, as well as different browsers like Chrome and Firefox, all with minimal effort. No need to worry about missing driver binaries—SeleniumOrchestrator simplifies the process.
   - **Support for Custom and Remote Drivers**: Whether you're working with local drivers or remote environments, **SeleniumOrchestrator** supports both seamlessly. For remote drivers, simply provide the remote URL, and the tool will handle the connection.

### 2. **Tab and Session Management**
   - **Named Sessions and Tabs**: Selenium traditionally uses session IDs and window handles to manage tabs. With **SeleniumOrchestrator**, you can assign custom names to your sessions and tabs, providing better readability and management.
   - **Better Control**: This shift from session IDs to named sessions makes it easier to identify and manage multiple sessions and tabs, making your Selenium scripts more intuitive and user-friendly.

### 3. **Enhanced Exception Handling**
   - **Robust Exception Classes**: **SeleniumOrchestrator** introduces a comprehensive suite of custom exception classes, designed to cover all key error scenarios such as browser initialization failures, tab management issues, and invalid driver operations.
   - **Integrated Logging**: All exceptions are automatically logged with detailed stack traces, helping you quickly identify and resolve issues. This logging mechanism ensures your tests are both safe and traceable, providing clear insights into any failures.

### 4. **Powerful Configuration System**
   - **Browser Config Builder**: The project includes a flexible configuration system, allowing you to define and customize browser settings for local and remote environments with ease.
   - **Dynamic Configuration**: Use `BrowserConfigBuilder` to manage browser configurations dynamically, making it easy to adjust and optimize your browser setups for various environments.

### 5. **Future-Proof Design**
   - **Scalability**: **SeleniumOrchestrator** is built to scale and grow as your testing needs expand. The current design allows for future integrations and features, such as advanced logging (with filters and multi-destination outputs), additional browser support, and further enhancements to tab and session management.
   - **Unit and Integration Tests**: The framework is designed to be fully tested, ensuring that every feature is robust and reliable. Unit and integration tests are an essential part of the development process, ensuring that your Selenium workflows are rock-solid.

---

## Installation

### Prerequisites
Ensure you have Python 3.x installed on your system. You will also need the following dependencies:

- **Selenium**: The core library used for browser automation.
- **WebDriver**: Required drivers (e.g., ChromeDriver, GeckoDriver) for the respective browsers.
- **Other dependencies**: Various utility packages used for logging, exception handling, and configuration.

### Install via pip

```bash
pip install -r requirements\base-requirements.txt 
```

---

## Usage

Here's a simple example to get started with **SeleniumOrchestrator**:

### Initialize a Chrome Driver:

```python 
from src.core.browser.browser_config_builder import BrowserConfigBuilder
from src.core.manager import SeleniumManager
from src.utils.logger import logger


chrome_connections = {
    'browser_type': 'chrome',
    'binary_path': '/path/to/chromedriver'
}

chrome_driver_options = BrowserConfigBuilder('chrome').set_headless().build()
manager = SeleniumManager()

chrome = manager.new_profile(
    'test driver',
    'test tab',
    chrome_driver_options,
    chrome_connections
)

chrome.driver.get('https://demoqa.com/')

chrome.new_tab('new tab')

if chrome.is_tab_exist('new tab'):
    logger.info("'new tab' exists between tabs")

if chrome.is_tab_exist('test tab'):
    logger.info("'test tab' exists between tabs")

manager.remove_profile('test initilize chrome driver')
```

### Initialize a Firefox Driver:

```python
from src.core.browser.browser_config_builder import BrowserConfigBuilder
from src.core.manager import SeleniumManager
from src.utils.logger import logger


chrome_connections = {
    'browser_type': 'firefox',
    'binary_path': '/path/to/geckodriver'
}

chrome_driver_options = BrowserConfigBuilder('firefox').set_headless().build()
manager = SeleniumManager()

chrome = manager.new_profile(
    'test gecko driver',
    'test tab',
    chrome_driver_options,
    chrome_connections
)

chrome.driver.get('https://demoqa.com/')

chrome.new_tab('new tab')

if chrome.is_tab_exist('new tab'):
    logger.info("'new tab' exists between tabs")

if chrome.is_tab_exist('test tab'):
    logger.info("'test tab' exists between tabs")

manager.remove_profile('test initilize gecko driver')
```

### Initialize Remote WebDriver:

```python
from src.core.browser.browser_config_builder import BrowserConfigBuilder
from src.core.manager import SeleniumManager
from src.utils.logger import logger


chrome_connections = {
    'browser_type': 'remote',
    'remote_url': 'http://localhost:7997/wd/hub',
}

# due the remote driver, is chrome-standalone, the options should be chrome type
chrome_driver_options = BrowserConfigBuilder('chrome').set_headless().build()
manager = SeleniumManager()
logger.info('Selenium manager created successfully')

chrome = manager.new_profile(
    'test remote driver',
    'test tab',
    chrome_driver_options,
    chrome_connections
)

chrome.driver.get('https://demoqa.com/')

chrome.new_tab('new tab')

if chrome.is_tab_exist('new tab'):
    logger.info("'new tab' exists between tabs")

if chrome.is_tab_exist('test tab'):
    logger.info("'test tab' exists between tabs")

manager.remove_profile('test initilize remote driver')
```

---

## Exception Handling and Logging

**SeleniumOrchestrator** automatically integrates powerful logging and exception handling throughout the framework. All exceptions are logged with detailed stack traces for easier debugging.

For example, if a browser initialization fails, the exception will not only be raised but also logged to your logs for future reference:

```python
from seleniumOrchestrator.utils.exceptions import BrowserInitializationError

try:
    driver = DriverCreator.create_chrome_driver(browser_config, connection_info)
except BrowserInitializationError as e:
    # Exception is logged automatically
    print(e)
```

---

## Why Choose SeleniumOrchestrator?

- **Ease of Use**: Simplifies driver initialization and session management, saving you time and effort in setting up your tests.
- **Robust Logging**: Automatically logs all exceptions with detailed error messages, providing deep insights into test failures.
- **Custom Tab/Session Management**: Move beyond traditional Selenium session IDs with named sessions and tabs for better readability and control.
- **Scalable**: Built with scalability in mind, the framework allows for easy extensions, additional features, and integrations.
- **Comprehensive Exception Handling**: With multiple custom exceptions and logging integrated, you can trust that your test failures will be handled and recorded in the most transparent and useful way possible.

---

## Contribution

We welcome contributions to **SeleniumOrchestrator**! If you would like to help improve the project, feel free to fork the repository, submit a pull request, or open an issue with your feedback or bug reports.

### How to contribute:

1. Fork the repository
2. Create a new branch (`git checkout -b feature-xyz`)
3. Make your changes and commit (`git commit -am 'Add feature xyz'`)
4. Push to the branch (`git push origin feature-xyz`)
5. Create a new pull request


---

## Conclusion

**SeleniumOrchestrator** is more than just a Selenium wrapper—it's a powerful tool that streamlines your browser automation and testing workflows, enhances error management, and provides a flexible, scalable framework for all your testing needs. Whether you're testing locally or remotely, SeleniumOrchestrator simplifies the process while maintaining the flexibility and control you need for effective browser automation.
