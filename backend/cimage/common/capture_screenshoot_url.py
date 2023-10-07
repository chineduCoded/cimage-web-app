#!/usr/bin/python3
"""Capture screenshot function"""

from playwright.async_api import async_playwright

async def capture_screenshot_of_url(url, selector=None):
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        context = await browser.new_context(device_scale_factor=1)
        page = await context.new_page()

        try:
            await page.goto(url)

            if selector:
                element = await page.query_selector(f".{selector}")
                if element:
                    screenshot = await element.screenshot()
                else:
                    raise ValueError(f"No element found with selector: {selector}")
            else:
                screenshot = await page.screenshot()

            return screenshot

        except Exception as e:
            print(f"Error capturing screenshot: {e}")
            raise ValueError(f"Error capturing screenshot: {str(e)}")

        finally:
            await page.close()
            await context.close()
            await browser.close()