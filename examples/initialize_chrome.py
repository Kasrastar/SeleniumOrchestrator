# from chromedriver_py import binary_path

from src.core.browser.browser_config_builder import BrowserConfigBuilder
from src.core.manager import SeleniumManager
from src.utils.logger import logger


chrome_connections = {
    'browser_type': 'chrome',
    # 'binary_path': binary_path
    'binary_path': '/path/to/chromedriver'
}

chrome_driver_options = BrowserConfigBuilder('chrome').set_headless().build()
logger.info('Chrome driver options created successfully')

manager = SeleniumManager()
logger.info('Selenium manager created successfully')

chrome = manager.new_profile(
    'test initilize chrome driver',
    'test tab',
    chrome_driver_options,
    chrome_connections
)
logger.info('Chrome driver created successfully')

chrome.driver.get('https://demoqa.com/')
logger.info('Navigated to demoqa.com')

chrome.new_tab('new tab')
logger.info('New tab created')

if chrome.is_tab_exist('new tab'):
    logger.info("'new tab' exists between tabs")

if chrome.is_tab_exist('test tab'):
    logger.info("'test tab' exists between tabs")

logger.info('All tabs checked successfully')

manager.remove_profile('test initilize chrome driver')
logger.info('Chrome driver closed and removed successfully')