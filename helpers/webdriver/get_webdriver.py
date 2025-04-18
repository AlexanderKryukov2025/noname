import pytest

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.chrome.service import Service as ChromiumService
from selenium.webdriver.firefox.service import Service as FirefoxService

from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from webdriver_manager.core.os_manager import ChromeType

from settings import BROWSER


# class fixtures not supported (maybe in the future)
class WebDriver:

    def __init__(self, params=(), resolution=()):
        self.browser = 'chrome'
        self.page_load_strategy = 'normal'
        # self.browser = pytest.CFG[BROWSER_TYPE]
        # self.browser_binary = pytest.CFG[BROWSER_BINARY]
        # self.driver_binary = pytest.CFG[DRIVER_BINARY]
        # self.driver_version = pytest.CFG[DRIVER_VERSION]
        # self.remote_url = pytest.CFG[REMOTE_URL]
        # self.graphic_interface = pytest.CFG[GRAPHIC_INTERFACE]
        # self.disable_check_media = pytest.CFG[DISABLE_CHECK_MEDIA]

        self.params = params
        self.resolution = resolution

    def define_browser_options(self):

        if self.browser == BROWSER.CHROME:
            self.init_browser_chrome()

        elif self.browser == BROWSER.CHROMIUM:
            self.init_browser_chromium()

        elif self.browser == BROWSER.FIREFOX:
            self.init_browser_firefox()

        elif self.browser == BROWSER.EDGE:
            self.init_browser_edge()

        else:
            raise Exception('Unknown browser type')

    def init_browser_chrome(self):

        self.options = webdriver.ChromeOptions()
        self.add_options()
        # if self.driver_binary:
        #     self.driver = webdriver.Chrome(
        #         service=ChromeService(self.driver_binary),
        #         options=self.options
        #     )
        #
        # elif self.driver_version:
        #     path = ChromeDriverManager(self.driver_version).install()
        #     self.driver = webdriver.Chrome(
        #         service=ChromeService(path),
        #         options=self.options
        #     )
        # else:

        path = ChromeDriverManager().install()
        self.driver = webdriver.Chrome(
            service=ChromeService(path),
            options=self.options
        )

    def init_browser_chromium(self):

        self.options = webdriver.ChromeOptions()
        self.add_options()

        if self.driver_binary and self.browser_binary:
            service = ChromiumService(executable_path=self.driver_binary)

        else:
            service = ChromiumService(ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install())

        if not self.remote_url:
            self.driver = webdriver.Chrome(
                service=service,
                options=self.options
            )

    def init_browser_firefox(self):

        self.options = webdriver.FirefoxOptions()
        self.add_options()
        if not self.remote_url:
            self.driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()))

    def init_browser_edge(self):

        self.options = webdriver.EdgeOptions()
        self.add_options()
        if not self.remote_url:
            self.driver = webdriver.Edge(service=EdgeService(EdgeChromiumDriverManager().install()))

    def add_options(self):

        self.chrome_options()
        # if self.browser == WEBBR.CHROME:
        #     self.chrome_options()
        #
        # elif self.browser == WEBBR.CHROMIUM:
        #     self.chromium_options()

    def chromium_options(self):
        self.options.binary_location = self.browser_binary
        self.chrome_options()

    def chrome_options(self):
        log_prefs = {
            # 'browser': 'ALL',
            # 'driver': 'ALL',
            # 'client': 'ALL',
            # 'server': 'ALL',
            'performance': 'ALL'
        }

        self.options.set_capability("goog:loggingPrefs", log_prefs)

        # self.options.add_experimental_option('perfLoggingPrefs', {
        #     'enableNetwork': True,
        #     'enablePage': True,
        # })

        if self.page_load_strategy:
            # https://www.selenium.dev/documentation/webdriver/drivers/options/
            self.options.page_load_strategy = self.page_load_strategy

        if 'headless' in self.params:
            # for non-remote testing https://stackoverflow.com/a/59678801
            # https://stackoverflow.com/q/57463616
            # For those who are running Protractor tests in Docker it's known
            # that you have to add this flags to prevent the browser crash issue:
            self.options.add_argument("--headless")
            self.options.add_argument("--no-sandbox")
            self.options.add_argument("--disable-gpu")
            self.options.add_argument("--disable-dev-shm-usage")
            self.options.add_argument("--window-size=1920x1080")
            self.options.add_argument("--use-fake-ui-for-media-stream")  # появляется лишь аудио устройство
            self.options.add_argument("--use-fake-device-for-media-stream")
            self.options.add_argument('--allow-file-access-from-files')
            self.options.add_argument(
                '--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36')

        if 'use-old-user-agent' in self.params:
            self.options.add_argument(
                f'user-agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79 Safari/537.36"')

        if 'disable-gpu' in self.params:
            self.options.add_argument('--disable-gpu')
            self.options.add_argument('--disable-software-rasterizer')

        if 'use-fake-ui-for-media-stream' in self.params:
            self.options.add_argument('--use-fake-ui-for-media-stream')

        if 'auto-select-desktop-capture-source' in self.params:
            pass
            # if get_screen_count() == 1:
            #     # https://groups.google.com/g/discuss-webrtc/c/JU6jwFUa5T4
            #     self.options.add_argument(f'auto-select-desktop-capture-source=Entire screen')
            # else:
            #     # and for several displays
            #     self.options.add_argument(f'auto-select-desktop-capture-source=Screen 1')

        self.options.add_argument('--allow-file-access-from-files')
        # добавить фейковую камеру со звуком
        self.options.add_argument('--use-fake-device-for-media-stream')
        # if not self.disable_check_media:
        #     self.options.add_argument(f'--use-file-for-fake-audio-capture={PATH_TO_AUDIO}')
        #     self.options.add_argument(f'--use-file-for-fake-video-capture={PATH_TO_VIDEO}')

        self.options.add_argument('ignore-certificate-errors')
        # отключить предупреждение Chrome is being controlled by automated test software
        self.options.add_experimental_option("excludeSwitches", ["enable-automation"])
        self.options.add_experimental_option('useAutomationExtension', False)

        # https://stackoverflow.com/a/72890648
        self.options.add_experimental_option("prefs", {
            "profile.content_settings.exceptions.clipboard": {'*': {'setting': 1}},
            "profile.default_content_setting_values.media_stream_mic": 1,
            "profile.default_content_setting_values.media_stream_camera": 1,
            "profile.default_content_setting_values.notifications": 1,
            # отключить предложение сохранять пароль
            "credentials_enable_service": False,
            "profile.password_manager_enabled": False
        })

    def define_resolution(self):
        if self.resolution:
            self.driver.set_window_size(*self.resolution)
        else:
            self.driver.maximize_window()

    def get(self):
        self.define_browser_options()

        if not hasattr(self, 'driver'):
            self.driver = webdriver.Remote(
                command_executor=self.remote_url,
                options=self.options
            )

        self.define_resolution()

        return self.driver


class WebDriver1080(WebDriver):
    def __init__(self, params=()):
        WebDriver.__init__(self, params, (1080, 720))


class WebDriver1600(WebDriver):
    def __init__(self, params=()):
        WebDriver.__init__(self, params, (1600, 900))


class WebDriver1920(WebDriver):
    def __init__(self, params=()):
        WebDriver.__init__(self, params, (1920, 1080))


class WebDriverMaxWindow(WebDriver):
    def __init__(self, params=()):
        WebDriver.__init__(self, params, ())
