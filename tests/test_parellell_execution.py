import pytest
from playwright.sync_api import sync_playwright
from queue import Queue
import threading
import math

def worker(contacts, queue, form_url, error_queue):
    worker_name = threading.current_thread().name  # Get the worker name
    with sync_playwright() as p:
        # Launch browser in non-headless mode to show UI
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()
        page.set_default_timeout(10000)
        for contact in contacts:
            try:
                # Navigate to the form page
                page.goto(form_url)
                # Fill in the form
                page.fill("[name='q']", contact["name"])
                # Log success with worker name
                queue.put(f"[{worker_name}] Successfully submitted form for {contact['name']}")
            except Exception as e:
                # Log error with worker name
                error_message = f"[{worker_name}] Error submitting form for {contact['name']}: {str(e)}"
                queue.put(error_message)
                error_queue.put(error_message)  # Store errors for failing the test
        browser.close()

@pytest.mark.parametrize("form_url", ["https://www.google.com"])
def test_parallel_form_submission(form_url):
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
        {"name": "William Martinez", "phone": "012-345-6789"}, {"name": "John Doe", "phone": "123-456-7890"},
        {"name": "Jane Smith", "phone": "234-567-8901"},
        {"name": "Alice Johnson", "phone": "345-678-9012"},
        {"name": "Bob Williams", "phone": "456-789-0123"},
        {"name": "Emma Brown", "phone": "567-890-1234"},
        {"name": "Michael Davis", "phone": "678-901-2345"},
        {"name": "Olivia Wilson", "phone": "789-012-3456"},
        {"name": "James Taylor", "phone": "890-123-4567"},
        {"name": "Sophia Anderson", "phone": "901-234-5678"},
        {"name": "William Martinez", "phone": "012-345-6789"}, {"name": "John Doe", "phone": "123-456-7890"},
        {"name": "Jane Smith", "phone": "234-567-8901"},
        {"name": "Alice Johnson", "phone": "345-678-9012"},
        {"name": "Bob Williams", "phone": "456-789-0123"},
        {"name": "Emma Brown", "phone": "567-890-1234"},
        {"name": "Michael Davis", "phone": "678-901-2345"},
        {"name": "Olivia Wilson", "phone": "789-012-3456"},
        {"name": "James Taylor", "phone": "890-123-4567"},
        {"name": "Sophia Anderson", "phone": "901-234-5678"},
        {"name": "William Martinez", "phone": "012-345-6789"}, {"name": "John Doe", "phone": "123-456-7890"},
        {"name": "Jane Smith", "phone": "234-567-8901"},
        {"name": "Alice Johnson", "phone": "345-678-9012"},
        {"name": "Bob Williams", "phone": "456-789-0123"},
        {"name": "Emma Brown", "phone": "567-890-1234"},
        {"name": "Michael Davis", "phone": "678-901-2345"},
        {"name": "Olivia Wilson", "phone": "789-012-3456"},
        {"name": "James Taylor", "phone": "890-123-4567"},
        {"name": "Sophia Anderson", "phone": "901-234-5678"},
        {"name": "William Martinez", "phone": "012-345-6789"}, {"name": "John Doe", "phone": "123-456-7890"},
        {"name": "Jane Smith", "phone": "234-567-8901"},
        {"name": "Alice Johnson", "phone": "345-678-9012"},
        {"name": "Bob Williams", "phone": "456-789-0123"},
        {"name": "Emma Brown", "phone": "567-890-1234"},
        {"name": "Michael Davis", "phone": "678-901-2345"},
        {"name": "Olivia Wilson", "phone": "789-012-3456"},
        {"name": "James Taylor", "phone": "890-123-4567"},
        {"name": "Sophia Anderson", "phone": "901-234-5678"},
        {"name": "William Martinez", "phone": "012-345-6789"}, {"name": "John Doe", "phone": "123-456-7890"},
        {"name": "Jane Smith", "phone": "234-567-8901"},
        {"name": "Alice Johnson", "phone": "345-678-9012"},
        {"name": "Bob Williams", "phone": "456-789-0123"},
        {"name": "Emma Brown", "phone": "567-890-1234"},
        {"name": "Michael Davis", "phone": "678-901-2345"},
        {"name": "Olivia Wilson", "phone": "789-012-3456"},
        {"name": "James Taylor", "phone": "890-123-4567"},
        {"name": "Sophia Anderson", "phone": "901-234-5678"},
        {"name": "William Martinez", "phone": "012-345-6789"}, {"name": "John Doe", "phone": "123-456-7890"},
        {"name": "Jane Smith", "phone": "234-567-8901"},
        {"name": "Alice Johnson", "phone": "345-678-9012"},
        {"name": "Bob Williams", "phone": "456-789-0123"},
        {"name": "Emma Brown", "phone": "567-890-1234"},
        {"name": "Michael Davis", "phone": "678-901-2345"},
        {"name": "Olivia Wilson", "phone": "789-012-3456"},
        {"name": "James Taylor", "phone": "890-123-4567"},
        {"name": "Sophia Anderson", "phone": "901-234-5678"},
        {"name": "William Martinez", "phone": "012-345-6789"}, {"name": "John Doe", "phone": "123-456-7890"},
        {"name": "Jane Smith", "phone": "234-567-8901"},
        {"name": "Alice Johnson", "phone": "345-678-9012"},
        {"name": "Bob Williams", "phone": "456-789-0123"},
        {"name": "Emma Brown", "phone": "567-890-1234"},
        {"name": "Michael Davis", "phone": "678-901-2345"},
        {"name": "Olivia Wilson", "phone": "789-012-3456"},
        {"name": "James Taylor", "phone": "890-123-4567"},
        {"name": "Sophia Anderson", "phone": "901-234-5678"},
        {"name": "William Martinez", "phone": "012-345-6789"}, {"name": "John Doe", "phone": "123-456-7890"},
        {"name": "Jane Smith", "phone": "234-567-8901"},
        {"name": "Alice Johnson", "phone": "345-678-9012"},
        {"name": "Bob Williams", "phone": "456-789-0123"},
        {"name": "Emma Brown", "phone": "567-890-1234"},
        {"name": "Michael Davis", "phone": "678-901-2345"},
        {"name": "Olivia Wilson", "phone": "789-012-3456"},
        {"name": "James Taylor", "phone": "890-123-4567"},
        {"name": "Sophia Anderson", "phone": "901-234-5678"},
        {"name": "William Martinez", "phone": "012-345-6789"}, {"name": "John Doe", "phone": "123-456-7890"},
        {"name": "Jane Smith", "phone": "234-567-8901"},
        {"name": "Alice Johnson", "phone": "345-678-9012"},
        {"name": "Bob Williams", "phone": "456-789-0123"},
        {"name": "Emma Brown", "phone": "567-890-1234"},
        {"name": "Michael Davis", "phone": "678-901-2345"},
        {"name": "Olivia Wilson", "phone": "789-012-3456"},
        {"name": "James Taylor", "phone": "890-123-4567"},
        {"name": "Sophia Anderson", "phone": "901-234-5678"},
        {"name": "William Martinez", "phone": "012-345-6789"}, {"name": "John Doe", "phone": "123-456-7890"},
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

    # Divide contacts among workers
    num_workers = 3
    chunk_size = math.ceil(len(contacts) / num_workers)
    chunks = [contacts[i:i + chunk_size] for i in range(0, len(contacts), chunk_size)]

    # Create queues for logging and errors
    queue = Queue()
    error_queue = Queue()

    # Create and start worker threads
    threads = []
    for chunk in chunks:
        t = threading.Thread(target=worker, args=(chunk, queue, form_url, error_queue))
        threads.append(t)
        t.start()

    # Wait for all threads to complete
    for t in threads:
        t.join()

    # Collect and print logs
    while not queue.empty():
        log = queue.get()
        print(log)

    # If there are any errors, fail the test
    if not error_queue.empty():
        error_messages = []
        while not error_queue.empty():
            error_messages.append(error_queue.get())
        pytest.fail(f"Test failed due to the following errors:\n" + "\n".join(error_messages))

if __name__ == "__main__":
    pytest.main(["-v", __file__])
