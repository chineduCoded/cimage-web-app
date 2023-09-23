#!/usr/bin/python3
"""Capture screenshot of URL"""
from playwright.async_api import async_playwright

async def capture_screenshot_of_url(url, selector=None):
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        context = await browser.new_context(device_scale_factor=1) 
        page = await context.new_page()

        try:
            # Set the viewport size
            # await page.set_viewport_size({"width": width, "height": height})

            await page.goto(url)

            if selector:
                # Capture screenshot of the specified element
                element = await page.query_selector(f".{selector}")
                if element:
                    screenshot = await element.screenshot()
                else:
                    raise ValueError(f"No element found with selector: {selector}")
            else:
                # Capture screenshot of the whole page
                screenshot = await page.screenshot()

            return screenshot

        except Exception as e:
            # Improved error handling with a more informative message
            print(f"Error capturing screenshot: {e}")
            raise ValueError(f"Error capturing screenshot: {str(e)}")

        finally:
            await browser.close()
