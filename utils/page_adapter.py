from pages.async_page import AsyncPage
from pages.sync_page import SyncPage


def get_page_adapter(page, mode='sync'):
    if mode == 'async':
        return AsyncPage(page)
    else:
        return SyncPage(page)
