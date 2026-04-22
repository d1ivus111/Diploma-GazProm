import re
from playwright.async_api import Playwright, sync_playwright, expect, APIRequestContext, Page
from conftest import api_request_context
import re
from playwright.sync_api import Playwright, sync_playwright, expect


def test_last_created_issue_should_be_on_the_server(api_request_context: APIRequestContext):
    new_issue = api_request_context.get(url='/booking')
    print(new_issue.ok)
    print(new_issue.json())
