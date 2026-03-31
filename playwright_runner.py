from playwright.sync_api import sync_playwright
import time

def execute_test(commands):
    steps = []
    results = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        try:
            for cmd in commands:

                # OPEN WEBSITE
                if cmd["action"] == "open":
                    steps.append(f"🌐 Opening {cmd['url']}...")
                    page.goto(cmd["url"])
                    time.sleep(3)
                    results.append(f"Opened {cmd['url']}")

                # SEARCH (YouTube / Google)
                elif cmd["action"] == "search":
                    steps.append(f"🔍 Searching {cmd['query']}...")
                    page.fill("input[name='search_query']", cmd["query"])
                    page.keyboard.press("Enter")
                    time.sleep(3)
                    results.append(f"Searched {cmd['query']}")

                # PLAY VIDEO
                elif cmd["action"] == "play":
                    steps.append(f"🎬 Playing video: {cmd['query']}...")

                    page.fill("input[name='search_query']", cmd["query"])
                    page.keyboard.press("Enter")
                    time.sleep(3)

                    page.click("ytd-video-renderer a#video-title")
                    time.sleep(5)

                    results.append(f"Playing video: {cmd['query']}")

                # TYPE (LOGIN)
                elif cmd["action"] == "type":
                    if cmd["selector"] == "#username":
                        steps.append("👤 Entering Username...")
                    elif cmd["selector"] == "#password":
                        steps.append("🔒 Entering Password...")

                    page.fill(cmd["selector"], cmd["text"])
                    time.sleep(1)

                    if cmd["selector"] == "#username":
                        results.append(f"Entered Username: {cmd['text']}")
                    elif cmd["selector"] == "#password":
                        results.append(f"Entered Password: {cmd['text']}")

                # CLICK BUTTON
                elif cmd["action"] == "click":
                    steps.append("🖱️ Clicking Login Button...")
                    page.click(cmd["selector"])
                    time.sleep(2)
                    results.append("Clicked Login Button")

                # ASSERTION
                elif cmd["action"] == "assert":
                    steps.append("✅ Checking result...")
                    content = page.content()

                    if cmd["text"].lower() in content.lower():
                        results.append("Assertion Passed ✅")
                    else:
                        results.append("Assertion Failed ❌")

        except Exception as e:
            results.append(f"Error: {str(e)}")

        browser.close()

    return steps, results