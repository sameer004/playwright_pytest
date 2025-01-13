import pytest
import os
import base64

import pytest_html
from playwright.sync_api import sync_playwright
from pathlib import Path
from pytest_html.extras import image  # Ensure pytest-html is installed


# Fixtures for Playwright setup
@pytest.fixture(scope="session")
def playwright_instance():
    with sync_playwright() as playwright:
        yield playwright


@pytest.fixture(scope="session")
def browser(playwright_instance):
    # Launch the browser with the maximized window
    browser = playwright_instance.chromium.launch(
        headless=False,  # Set to True for headless mode
        args=["--start-maximized"]  # Maximizes the window
    )
    yield browser
    browser.close()


@pytest.fixture(scope="function")
def page_setup(browser):
    # Create a new browser context with a maximized viewport
    context = browser.new_context(no_viewport=True)
    page = context.new_page()

    yield page
    page.close()


def pytest_html_report_title(report):
    report.title = "Pytest HTML Report Example"


# Pytest-html configuration
def pytest_configure(config):
    # Set the report file name and location
    config.option.htmlpath = "reports/test_report.html"
    config.option.self_contained_html = True  # Embed resources in the HTML file


# Hook to capture screenshots for failed tests
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item):
    # Execute all other hooks to obtain the report object
    outcome = yield
    report = outcome.get_result()
    extra = getattr(report, "extra", [])
    if report.when == "call" and report.failed:
        # Define the screenshot path
        screenshot_path = Path("./screenshots/failed_screenshot.png")

        # Remove the old screenshot if it exists
        if screenshot_path.exists():
            screenshot_path.unlink()

        # Capture a new screenshot (assuming you use Playwright's page object)
        page = item.funcargs.get("page_setup")
        if page:
            screenshot_path.parent.mkdir(parents=True, exist_ok=True)  # Ensure the directory exists
            page.screenshot(path=str(screenshot_path))

            # Encode the screenshot and attach it to the report
            with open(screenshot_path, "rb") as image_file:
                encoded_string = base64.b64encode(image_file.read()).decode()
                extra.append(pytest_html.extras.image(encoded_string))
        report.extras = extra


# Customizing the HTML report
@pytest.hookimpl(optionalhook=True)
def pytest_html_results_table_header(cells):
    # Add a header for the screenshot column
    cells.insert(2, "Screenshot")


@pytest.hookimpl(optionalhook=True)
def pytest_html_results_table_row(report, cells):
    # Insert the screenshot into the results table if it exists
    screenshot = next(
        (extra for extra in getattr(report, "extra", []) if extra.get("image")),
        None,
    )
    if screenshot:
        cells.insert(2, f'<a href="data:image/png;base64,{screenshot["content"]}" target="_blank">View</a>')
    else:
        cells.insert(2, "N/A")
