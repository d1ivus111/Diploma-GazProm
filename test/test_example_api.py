from playwright.sync_api import APIRequestContext

def test_last_created_issue_should_be_on_the_server(api_request_context: APIRequestContext):
    new_issue = api_request_context.get(url='/booking')
    print(new_issue.ok)
    print(new_issue.json())