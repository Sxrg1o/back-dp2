"""
Web scraper for static content extraction.
"""
import asyncio
import random
from typing import Optional, Dict, Any
from urllib.parse import urljoin, urlparse

import httpx
from bs4 import BeautifulSoup

from app.core.config import settings
from app.core.logging import logger
from app.oai.contracts.menu_contract import MenuContract, MenuItemContract


class WebScraper:
    """Web scraper for extracting data from static websites."""
    
    def __init__(self):
        self.client = httpx.AsyncClient(
            headers={
                "User-Agent": settings.SCRAPING_USER_AGENT,
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                "Accept-Language": "en-US,en;q=0.5",
                "Accept-Encoding": "gzip, deflate",
                "Connection": "keep-alive",
            },
            timeout=30.0,
        )
    
    async def __aenter__(self):
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.client.aclose()
    
    async def _get_page(self, url: str) -> BeautifulSoup:
        """Fetch and parse a web page."""
        
        # Add random delay to avoid being blocked
        delay = random.uniform(settings.SCRAPING_DELAY_MIN, settings.SCRAPING_DELAY_MAX)
        await asyncio.sleep(delay)
        
        logger.info("Fetching page", url=url)
        
        try:
            response = await self.client.get(url)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, "lxml")
            return soup
            
        except httpx.HTTPError as e:
            logger.error("HTTP error while fetching page", url=url, error=str(e))
            raise
        except Exception as e:
            logger.error("Unexpected error while fetching page", url=url, error=str(e))
            raise
    
    async def scrape_menu(self, restaurant_url: str) -> Optional[MenuContract]:
        """
        Scrape menu from a restaurant website.
        
        This is a generic implementation that should be customized
        for specific restaurant websites.
        """
        
        try:
            soup = await self._get_page(restaurant_url)
            
            # Extract restaurant name (customize selector as needed)
            restaurant_name = "Unknown Restaurant"
            name_element = soup.find("h1") or soup.find("title")
            if name_element:
                restaurant_name = name_element.get_text(strip=True)
            
            # Extract menu items (customize selectors as needed)
            items = []
            
            # Example: Look for common menu item patterns
            menu_items = soup.find_all(["div", "li"], class_=lambda x: x and any(
                keyword in x.lower() for keyword in ["menu-item", "dish", "product", "item"]
            ))
            
            for item_element in menu_items:
                try:
                    item = await self._extract_menu_item(item_element, restaurant_url)
                    if item:
                        items.append(item)
                except Exception as e:
                    logger.warning("Error extracting menu item", error=str(e))
                    continue
            
            if not items:
                logger.warning("No menu items found", url=restaurant_url)
                return None
            
            # Create menu contract
            menu = MenuContract(
                restaurant_id=urlparse(restaurant_url).netloc,
                restaurant_name=restaurant_name,
                items=items,
                source="web_scraper",
            )
            
            logger.info(
                "Successfully scraped menu",
                url=restaurant_url,
                items_count=len(items),
            )
            
            return menu
            
        except Exception as e:
            logger.error("Error scraping menu", url=restaurant_url, error=str(e))
            return None
    
    async def _extract_menu_item(
        self,
        item_element: BeautifulSoup,
        base_url: str
    ) -> Optional[MenuItemContract]:
        """Extract menu item data from HTML element."""
        
        # Extract name
        name_element = item_element.find(["h1", "h2", "h3", "h4", "h5", "h6"]) or \
                      item_element.find(class_=lambda x: x and "name" in x.lower())
        
        if not name_element:
            return None
        
        name = name_element.get_text(strip=True)
        if not name:
            return None
        
        # Extract description
        description = None
        desc_element = item_element.find("p") or \
                      item_element.find(class_=lambda x: x and "description" in x.lower())
        if desc_element:
            description = desc_element.get_text(strip=True)
        
        # Extract price
        price = 0.0
        price_element = item_element.find(class_=lambda x: x and "price" in x.lower()) or \
                       item_element.find(string=lambda text: text and "$" in text)
        
        if price_element:
            price_text = price_element if isinstance(price_element, str) else price_element.get_text()
            # Extract numeric price (basic implementation)
            import re
            price_match = re.search(r'[\d,]+\.?\d*', price_text.replace("$", "").replace(",", ""))
            if price_match:
                try:
                    price = float(price_match.group())
                except ValueError:
                    pass
        
        # Extract image URL
        image_url = None
        img_element = item_element.find("img")
        if img_element and img_element.get("src"):
            image_url = urljoin(base_url, img_element["src"])
        
        # Extract category (if available)
        category = "General"
        category_element = item_element.find_parent(class_=lambda x: x and "category" in x.lower())
        if category_element:
            category_text = category_element.get_text(strip=True)
            if category_text:
                category = category_text
        
        return MenuItemContract(
            external_id=f"scraped_{hash(name)}",
            name=name,
            description=description,
            price=price,
            category=category,
            image_url=image_url,
            available=True,
        )
    
    async def scrape_custom_site(
        self,
        url: str,
        selectors: Dict[str, str]
    ) -> Dict[str, Any]:
        """
        Scrape data from a website using custom selectors.
        
        Args:
            url: Target URL
            selectors: Dictionary mapping field names to CSS selectors
        
        Returns:
            Dictionary with extracted data
        """
        
        soup = await self._get_page(url)
        data = {}
        
        for field, selector in selectors.items():
            try:
                elements = soup.select(selector)
                if elements:
                    if len(elements) == 1:
                        data[field] = elements[0].get_text(strip=True)
                    else:
                        data[field] = [elem.get_text(strip=True) for elem in elements]
                else:
                    data[field] = None
            except Exception as e:
                logger.warning(f"Error extracting field {field}", error=str(e))
                data[field] = None
        
        return data