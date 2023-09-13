#!/usr/bin/python3
"""Capture screenshot of URL"""
from playwright.async_api import async_playwright

async def capture_screenshot_of_url(url, locator):
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        context = await browser.new_context(device_scale_factor=2)
        page = await context.new_page()
        
        try:
            await page.goto(url)

            # Capture screenshot
            element = await page.locator(locator) if locator else None
            screenshot = await (element.screenshot() if element else page.screenshot())

            return screenshot
        
        except Exception as e:
            raise e
        
        finally:
            await browser.close()