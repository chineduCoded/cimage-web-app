#!/usr/bin/python3
"""Capture screenshot of URL"""
from playwright.async_api import async_playwright

async def capture_screenshot_of_url(url, selector=None, width=1024, height=768):
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        context = await browser.new_context(device_scale_factor=1)  # Set the device scale factor as needed
        page = await context.new_page()

        try:
            # Set the viewport size
            await page.set_viewport_size({"width": width, "height": height})

            await page.goto(url)

            if selector:
                # Capture screenshot of the specified element
                element = await page.query_selector(f".{selector}")
                screenshot = await element.screenshot()
            else:
                # Capture screenshot of the whole page
                screenshot = await page.screenshot()

            return screenshot

        except Exception as e:
            raise e

        finally:
            await browser.close()
