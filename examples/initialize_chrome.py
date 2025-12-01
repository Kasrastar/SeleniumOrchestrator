# from chromedriver_py import binary_path


from src.application.profile_service import ProfileService
from src.infra.browser_config_builder import BrowserConfigBuilder
from src.infra.selenium_session import SeleniumSession
from src.utils.logger import logger



chrome_connections = {
    'browser_type': 'chrome',
    #  'binary_path': binary_path
    'binary_path': '/path/to/chromedriver'
}

# due the remote driver, is chrome-standalone, the options should be chrome type
options = BrowserConfigBuilder('chrome').set_no_sandbox().disable_dev_shm_usage().set_browser_profile('./profiles/test_profile').build()
session = SeleniumSession()
profile_service = ProfileService()

new_profile = profile_service.new_profile(
    driver_name='test_driver',
    tab_name='initial_tab',
    session=session,
    profile_options=options,
    connection=chrome_connections
)

url = 'https://demoqa.com'
new_profile.session.get(url)
logger.info('Navigated to demoqa.com')
