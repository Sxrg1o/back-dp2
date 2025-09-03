"""
RPA (Robotic Process Automation) for dynamic content and interactions.
"""
import asyncio
from typing import Optional, Dict, Any, List
from urllib.parse import urlparse

from playwright.async_api import async_playwright, Browser, Page, TimeoutError as PlaywrightTimeoutError

from app.core.config import settings
from app.core.logging import logger
from app.oai.contracts.menu_contract import MenuContract, MenuItemContract


class RPABot:
    """RPA bot for automating browser interactions."""
    
    def __init__(self):
        self.browser: Optional[Browser] = None
        self.page: Optional[Page] = None
    
    async def __aenter__(self):
        """Async context manager entry."""
        await self.start()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        await self.stop()
    
    async def start(self):
        """Start the browser."""
        self.playwright = await async_playwright().start()
        
        # Launch browser
        self.browser = await self.playwright.chromium.launch(
            headless=settings.RPA_HEADLESS,
            args=[
                "--no-sandbox",
                "--disable-dev-shm-usage",
                "--disable-gpu",
                "--disable-web-security",
                "--disable-features=VizDisplayCompositor",
            ]
        )
        
        # Create new page
        self.page = await self.browser.new_page()
        
        # Set user agent
        await self.page.set_extra_http_headers({
            "User-Agent": settings.SCRAPING_USER_AGENT
        })
        
        logger.info("RPA bot started")
    
    async def stop(self):
        """Stop the browser."""
        if self.page:
            await self.page.close()
        
        if self.browser:
            await self.browser.close()
        
        if hasattr(self, 'playwright'):
            await self.playwright.stop()
        
        logger.info("RPA bot stopped")
    
    async def navigate_to(self, url: str, wait_for: str = "networkidle") -> bool:
        """Navigate to a URL."""
        try:
            logger.info("Navigating to URL", url=url)
            
            await self.page.goto(url, wait_until=wait_for, timeout=settings.RPA_TIMEOUT * 1000)
            
            # Wait a bit for dynamic content
            await asyncio.sleep(2)
            
            return True
            
        except PlaywrightTimeoutError:
            logger.error("Timeout while navigating", url=url)
            return False
        except Exception as e:
            logger.error("Error navigating to URL", url=url, error=str(e))
            return False
    
    async def login(self, username: str, password: str, login_config: Dict[str, str]) -> bool:
        """
        Perform login using provided credentials and selectors.
        
        Args:
            username: Username/email
            password: Password
            login_config: Dictionary with selectors for login elements
                - username_selector: CSS selector for username field
                - password_selector: CSS selector for password field
                - submit_selector: CSS selector for submit button
                - success_indicator: CSS selector to verify successful login
        
        Returns:
            True if login successful, False otherwise
        """
        
        try:
            logger.info("Attempting login")
            
            # Fill username
            await self.page.fill(login_config["username_selector"], username)
            await asyncio.sleep(0.5)
            
            # Fill password
            await self.page.fill(login_config["password_selector"], password)
            await asyncio.sleep(0.5)
            
            # Click submit button
            await self.page.click(login_config["submit_selector"])
            
            # Wait for navigation or success indicator
            if "success_indicator" in login_config:
                await self.page.wait_for_selector(
                    login_config["success_indicator"],
                    timeout=settings.RPA_TIMEOUT * 1000
                )
            else:
                await self.page.wait_for_load_state("networkidle")
            
            logger.info("Login successful")
            return True
            
        except Exception as e:
            logger.error("Login failed", error=str(e))
            return False
    
    async def extract_data(self, selectors: Dict[str, str]) -> Dict[str, Any]:
        """
        Extract data from the current page using CSS selectors.
        
        Args:
            selectors: Dictionary mapping field names to CSS selectors
        
        Returns:
            Dictionary with extracted data
        """
        
        data = {}
        
        for field, selector in selectors.items():
            try:
                # Wait for element to be present
                await self.page.wait_for_selector(selector, timeout=5000)
                
                # Extract text content
                elements = await self.page.query_selector_all(selector)
                
                if elements:
                    if len(elements) == 1:
                        data[field] = await elements[0].text_content()
                    else:
                        texts = []
                        for element in elements:
                            text = await element.text_content()
                            if text:
                                texts.append(text.strip())
                        data[field] = texts
                else:
                    data[field] = None
                    
            except Exception as e:
                logger.warning(f"Error extracting field {field}", error=str(e))
                data[field] = None
        
        return data
    
    async def scrape_dynamic_menu(
        self,
        restaurant_url: str,
        menu_config: Dict[str, str]
    ) -> Optional[MenuContract]:
        """
        Scrape menu from a dynamic website (SPA, JavaScript-heavy).
        
        Args:
            restaurant_url: Restaurant website URL
            menu_config: Configuration with selectors for menu elements
        
        Returns:
            MenuContract with scraped data or None if failed
        """
        
        try:
            # Navigate to the menu page
            if not await self.navigate_to(restaurant_url):
                return None
            
            # Wait for menu items to load
            menu_selector = menu_config.get("menu_container", ".menu-item")
            await self.page.wait_for_selector(menu_selector, timeout=10000)
            
            # Extract restaurant name
            restaurant_name = "Unknown Restaurant"
            if "restaurant_name_selector" in menu_config:
                name_element = await self.page.query_selector(menu_config["restaurant_name_selector"])
                if name_element:
                    restaurant_name = await name_element.text_content() or restaurant_name
            
            # Extract menu items
            items = []
            menu_items = await self.page.query_selector_all(menu_selector)
            
            for item_element in menu_items:
                try:
                    item_data = await self._extract_menu_item_rpa(item_element, menu_config)
                    if item_data:
                        items.append(item_data)
                except Exception as e:
                    logger.warning("Error extracting menu item", error=str(e))
                    continue
            
            if not items:
                logger.warning("No menu items found", url=restaurant_url)
                return None
            
            menu = MenuContract(
                restaurant_id=urlparse(restaurant_url).netloc,
                restaurant_name=restaurant_name.strip(),
                items=items,
                source="rpa_bot",
            )
            
            logger.info(
                "Successfully scraped dynamic menu",
                url=restaurant_url,
                items_count=len(items),
            )
            
            return menu
            
        except Exception as e:
            logger.error("Error scraping dynamic menu", url=restaurant_url, error=str(e))
            return None
    
    async def _extract_menu_item_rpa(
        self,
        item_element,
        config: Dict[str, str]
    ) -> Optional[MenuItemContract]:
        """Extract menu item data from element using RPA."""
        
        try:
            # Extract name
            name = None
            name_selector = config.get("item_name_selector", "h3, .name, .title")
            name_element = await item_element.query_selector(name_selector)
            if name_element:
                name = await name_element.text_content()
            
            if not name or not name.strip():
                return None
            
            name = name.strip()
            
            # Extract description
            description = None
            desc_selector = config.get("item_description_selector", "p, .description")
            desc_element = await item_element.query_selector(desc_selector)
            if desc_element:
                description = await desc_element.text_content()
                if description:
                    description = description.strip()
            
            # Extract price
            price = 0.0
            price_selector = config.get("item_price_selector", ".price")
            price_element = await item_element.query_selector(price_selector)
            if price_element:
                price_text = await price_element.text_content()
                if price_text:
                    # Extract numeric price
                    import re
                    price_match = re.search(r'[\d,]+\.?\d*', price_text.replace("$", "").replace(",", ""))
                    if price_match:
                        try:
                            price = float(price_match.group())
                        except ValueError:
                            pass
            
            # Extract category
            category = "General"
            category_selector = config.get("item_category_selector")
            if category_selector:
                category_element = await item_element.query_selector(category_selector)
                if category_element:
                    category_text = await category_element.text_content()
                    if category_text:
                        category = category_text.strip()
            
            # Extract image URL
            image_url = None
            img_selector = config.get("item_image_selector", "img")
            img_element = await item_element.query_selector(img_selector)
            if img_element:
                src = await img_element.get_attribute("src")
                if src:
                    image_url = src
            
            return MenuItemContract(
                external_id=f"rpa_{hash(name)}",
                name=name,
                description=description,
                price=price,
                category=category,
                image_url=image_url,
                available=True,
            )
            
        except Exception as e:
            logger.error("Error extracting menu item with RPA", error=str(e))
            return None
    
    async def download_file(self, download_url: str, file_path: str) -> bool:
        """Download a file using the browser."""
        try:
            logger.info("Starting file download", url=download_url, path=file_path)
            
            # Start waiting for download
            async with self.page.expect_download() as download_info:
                await self.page.goto(download_url)
            
            download = await download_info.value
            
            # Save the file
            await download.save_as(file_path)
            
            logger.info("File downloaded successfully", path=file_path)
            return True
            
        except Exception as e:
            logger.error("Error downloading file", url=download_url, error=str(e))
            return False