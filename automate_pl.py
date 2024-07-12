import asyncio
from playwright.async_api import async_playwright
import json
from time import sleep

# Storage for network requests
network_requests = {
    'GET': [],
    'POST': []
}

# Function to capture network events
async def capture_network_events(route):
    request = route.request
    method = request.method
    if method in network_requests:
        headers = dict(request.headers)
        # print(request)
        # print(type(request.post_data()))
        try:
            post_data = request.post_data if method == 'POST' else None
        except Exception as e:
            post_data = f"You are fucked up. It's using javascript for post request: {e}"
            print(e) 
        # body = post_data.decode('utf-8') if post_data else ''
        network_requests[method].append({
            'url': request.url,
            'method': method,
            'headers': headers,
            'body': post_data
        })
    await route.continue_()

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)  # Set headless=True for not visible browser
        context = await browser.new_context(record_har_path='network_requests.har')  # Save HAR file

        page = await context.new_page()

        # Enable network request interception
        await page.route("**/*", capture_network_events)

        # Open a website with increased timeout
        await page.goto('https://clay-email-finder.netlify.app', timeout=60000)

        # Perform actions on the website
        try:
            await page.fill('input[name="fullName"]', "nivrita")
        except Exception as e:
            print(f"Error finding 'fullName' input: {e}")

        try:
            await page.fill('input[name="domain"]', "google.com")
        except Exception as e:
            print(f"Error finding 'domain' input: {e}")

        try:
            # for i in range(10):
            #     print(i)
            #     await asyncio.sleep(1)
            # Wait for the button to be visible and clickable
            await page.wait_for_selector('css=button')
            await page.click('css=button')
            print("Button was clicked")
        except Exception as e:
            print(f"Error finding or clicking button: {e}")

        # Give some time for the requests to complete
        await asyncio.sleep(10)  # Adjust as needed

        # Cleanup
        await context.close()
        await browser.close()

        # Process captured events
        print("GET Requests:")
        print(json.dumps(network_requests['GET'], indent=4))
        print("POST Requests:")
        print(json.dumps(network_requests['POST'], indent=4))

# Run the main function
asyncio.run(main())
