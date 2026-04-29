import pytest
from playwright.sync_api import Playwright
from pathlib import Path

URL = 'https://simple-grocery-store-api.click'


@pytest.fixture(scope='session')
def api_context(playwright: Playwright):
    request_context = playwright.request.new_context(
        base_url=URL,
        extra_http_headers={"Content-Type": "application/json"}
    )
    yield request_context
    request_context.dispose()


@pytest.fixture(scope='function')
def data_dir():
    return Path(__file__).resolve().parent.parent / "Simple_Grocery_Store_Data"
