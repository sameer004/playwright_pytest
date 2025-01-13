import pytest
from playwright.sync_api import sync_playwright
from queue import Queue
import threading
import math



@pytest.mark.parametrize("form_url", ["https://www.google.com"])
def test_parallel_form_submission(form_url, page_setup):
    # Create JSON array with 10 records of name and phone number
    contacts = [
        {"name": "John Doe", "phone": "123-456-7890"},
        {"name": "Jane Smith", "phone": "234-567-8901"},
        {"name": "Alice Johnson", "phone": "345-678-9012"},
        {"name": "Bob Williams", "phone": "456-789-0123"},
        {"name": "Emma Brown", "phone": "567-890-1234"},
        {"name": "Michael Davis", "phone": "678-901-2345"},
        {"name": "Olivia Wilson", "phone": "789-012-3456"},
        {"name": "James Taylor", "phone": "890-123-4567"},
        {"name": "Sophia Anderson", "phone": "901-234-5678"},
        {"name": "William Martinez", "phone": "012-345-6789"},{"name": "John Doe", "phone": "123-456-7890"},
        {"name": "Jane Smith", "phone": "234-567-8901"},
        {"name": "Alice Johnson", "phone": "345-678-9012"},
        {"name": "Bob Williams", "phone": "456-789-0123"},
        {"name": "Emma Brown", "phone": "567-890-1234"},
        {"name": "Michael Davis", "phone": "678-901-2345"},
        {"name": "Olivia Wilson", "phone": "789-012-3456"},
        {"name": "James Taylor", "phone": "890-123-4567"},
        {"name": "Sophia Anderson", "phone": "901-234-5678"},
        {"name": "William Martinez", "phone": "012-345-6789"},{"name": "John Doe", "phone": "123-456-7890"},
        {"name": "Jane Smith", "phone": "234-567-8901"},
        {"name": "Alice Johnson", "phone": "345-678-9012"},
        {"name": "Bob Williams", "phone": "456-789-0123"},
        {"name": "Emma Brown", "phone": "567-890-1234"},
        {"name": "Michael Davis", "phone": "678-901-2345"},
        {"name": "Olivia Wilson", "phone": "789-012-3456"},
        {"name": "James Taylor", "phone": "890-123-4567"},
        {"name": "Sophia Anderson", "phone": "901-234-5678"},
        {"name": "William Martinez", "phone": "012-345-6789"},{"name": "John Doe", "phone": "123-456-7890"},
        {"name": "Jane Smith", "phone": "234-567-8901"},
        {"name": "Alice Johnson", "phone": "345-678-9012"},
        {"name": "Bob Williams", "phone": "456-789-0123"},
        {"name": "Emma Brown", "phone": "567-890-1234"},
        {"name": "Michael Davis", "phone": "678-901-2345"},
        {"name": "Olivia Wilson", "phone": "789-012-3456"},
        {"name": "James Taylor", "phone": "890-123-4567"},
        {"name": "Sophia Anderson", "phone": "901-234-5678"},
        {"name": "William Martinez", "phone": "012-345-6789"},{"name": "John Doe", "phone": "123-456-7890"},
        {"name": "Jane Smith", "phone": "234-567-8901"},
        {"name": "Alice Johnson", "phone": "345-678-9012"},
        {"name": "Bob Williams", "phone": "456-789-0123"},
        {"name": "Emma Brown", "phone": "567-890-1234"},
        {"name": "Michael Davis", "phone": "678-901-2345"},
        {"name": "Olivia Wilson", "phone": "789-012-3456"},
        {"name": "James Taylor", "phone": "890-123-4567"},
        {"name": "Sophia Anderson", "phone": "901-234-5678"},
        {"name": "William Martinez", "phone": "012-345-6789"},{"name": "John Doe", "phone": "123-456-7890"},
        {"name": "Jane Smith", "phone": "234-567-8901"},
        {"name": "Alice Johnson", "phone": "345-678-9012"},
        {"name": "Bob Williams", "phone": "456-789-0123"},
        {"name": "Emma Brown", "phone": "567-890-1234"},
        {"name": "Michael Davis", "phone": "678-901-2345"},
        {"name": "Olivia Wilson", "phone": "789-012-3456"},
        {"name": "James Taylor", "phone": "890-123-4567"},
        {"name": "Sophia Anderson", "phone": "901-234-5678"},
        {"name": "William Martinez", "phone": "012-345-6789"},{"name": "John Doe", "phone": "123-456-7890"},
        {"name": "Jane Smith", "phone": "234-567-8901"},
        {"name": "Alice Johnson", "phone": "345-678-9012"},
        {"name": "Bob Williams", "phone": "456-789-0123"},
        {"name": "Emma Brown", "phone": "567-890-1234"},
        {"name": "Michael Davis", "phone": "678-901-2345"},
        {"name": "Olivia Wilson", "phone": "789-012-3456"},
        {"name": "James Taylor", "phone": "890-123-4567"},
        {"name": "Sophia Anderson", "phone": "901-234-5678"},
        {"name": "William Martinez", "phone": "012-345-6789"},{"name": "John Doe", "phone": "123-456-7890"},
        {"name": "Jane Smith", "phone": "234-567-8901"},
        {"name": "Alice Johnson", "phone": "345-678-9012"},
        {"name": "Bob Williams", "phone": "456-789-0123"},
        {"name": "Emma Brown", "phone": "567-890-1234"},
        {"name": "Michael Davis", "phone": "678-901-2345"},
        {"name": "Olivia Wilson", "phone": "789-012-3456"},
        {"name": "James Taylor", "phone": "890-123-4567"},
        {"name": "Sophia Anderson", "phone": "901-234-5678"},
        {"name": "William Martinez", "phone": "012-345-6789"},{"name": "John Doe", "phone": "123-456-7890"},
        {"name": "Jane Smith", "phone": "234-567-8901"},
        {"name": "Alice Johnson", "phone": "345-678-9012"},
        {"name": "Bob Williams", "phone": "456-789-0123"},
        {"name": "Emma Brown", "phone": "567-890-1234"},
        {"name": "Michael Davis", "phone": "678-901-2345"},
        {"name": "Olivia Wilson", "phone": "789-012-3456"},
        {"name": "James Taylor", "phone": "890-123-4567"},
        {"name": "Sophia Anderson", "phone": "901-234-5678"},
        {"name": "William Martinez", "phone": "012-345-6789"},{"name": "John Doe", "phone": "123-456-7890"},
        {"name": "Jane Smith", "phone": "234-567-8901"},
        {"name": "Alice Johnson", "phone": "345-678-9012"},
        {"name": "Bob Williams", "phone": "456-789-0123"},
        {"name": "Emma Brown", "phone": "567-890-1234"},
        {"name": "Michael Davis", "phone": "678-901-2345"},
        {"name": "Olivia Wilson", "phone": "789-012-3456"},
        {"name": "James Taylor", "phone": "890-123-4567"},
        {"name": "Sophia Anderson", "phone": "901-234-5678"},
        {"name": "William Martinez", "phone": "012-345-6789"},{"name": "John Doe", "phone": "123-456-7890"},
        {"name": "Jane Smith", "phone": "234-567-8901"},
        {"name": "Alice Johnson", "phone": "345-678-9012"},
        {"name": "Bob Williams", "phone": "456-789-0123"},
        {"name": "Emma Brown", "phone": "567-890-1234"},
        {"name": "Michael Davis", "phone": "678-901-2345"},
        {"name": "Olivia Wilson", "phone": "789-012-3456"},
        {"name": "James Taylor", "phone": "890-123-4567"},
        {"name": "Sophia Anderson", "phone": "901-234-5678"},
        {"name": "William Martinez", "phone": "012-345-6789"}
    ]
    page = page_setup
    page.set_default_timeout(10000)
    for contact in contacts:
        try:
            # Navigate to the form page
            page.goto(form_url)
            # Fill in the form
            page.fill("[name='q']", contact["name"])
            # Log success with worker name

        except Exception as e:
            # Log error with worker name
            error_message = f"[  Error submitting form for {contact['name']}: {str(e)}"

