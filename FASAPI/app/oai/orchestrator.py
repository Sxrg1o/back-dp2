"""
Orchestrator for selecting between HTTP scraping and RPA strategies.
"""
from enum import Enum
from typing import Optional, Dict, Any

from app.core.logging import logger
from app.oai.contracts.menu_contract import MenuContract
from app.oai.sources.scraper import WebScraper
from app.oai.sources.rpa import RPABot


class IntegrationStrategy(str, Enum):
    """Integration strategy enumeration."""
    HTTP_SCRAPING = "http_scraping"
    RPA = "rpa"
    AUTO = "auto"


class IntegrationOrchestrator:
    """Orchestrator for external integrations."""
    
    def __init__(self):
        self.strategy_configs = {
            # Example configurations for different restaurant websites
            "example-restaurant.com": {
                "strategy": IntegrationStrategy.HTTP_SCRAPING,
                "selectors": {
                    "menu_items": ".menu-item",
                    "item_name": "h3",
                    "item_price": ".price",
                    "item_description": "p",
                }
            },
            "dynamic-restaurant.com": {
                "strategy": IntegrationStrategy.RPA,
                "config": {
                    "menu_container": ".menu-grid .item",
                    "item_name_selector": ".item-name",
                    "item_price_selector": ".item-price",
                    "item_description_selector": ".item-desc",
                    "restaurant_name_selector": "h1.restaurant-title",
                },
                "login_required": True,
                "login_config": {
                    "username_selector": "#username",
                    "password_selector": "#password",
                    "submit_selector": "button[type='submit']",
                    "success_indicator": ".dashboard",
                }
            }
        }
    
    def _get_domain(self, url: str) -> str:
        """Extract domain from URL."""
        from urllib.parse import urlparse
        return urlparse(url).netloc
    
    def _determine_strategy(self, url: str) -> IntegrationStrategy:
        """Determine the best integration strategy for a URL."""
        domain = self._get_domain(url)
        
        # Check if we have specific configuration for this domain
        if domain in self.strategy_configs:
            return self.strategy_configs[domain]["strategy"]
        
        # Default to HTTP scraping for unknown domains
        return IntegrationStrategy.HTTP_SCRAPING
    
    async def scrape_menu(
        self,
        restaurant_url: str,
        strategy: IntegrationStrategy = IntegrationStrategy.AUTO,
        credentials: Optional[Dict[str, str]] = None
    ) -> Optional[MenuContract]:
        """
        Scrape menu using the appropriate strategy.
        
        Args:
            restaurant_url: Restaurant website URL
            strategy: Integration strategy to use
            credentials: Login credentials if required (username, password)
        
        Returns:
            MenuContract with scraped data or None if failed
        """
        
        # Determine strategy if auto
        if strategy == IntegrationStrategy.AUTO:
            strategy = self._determine_strategy(restaurant_url)
        
        logger.info(
            "Starting menu scraping",
            url=restaurant_url,
            strategy=strategy.value,
        )
        
        try:
            if strategy == IntegrationStrategy.HTTP_SCRAPING:
                return await self._scrape_with_http(restaurant_url)
            elif strategy == IntegrationStrategy.RPA:
                return await self._scrape_with_rpa(restaurant_url, credentials)
            else:
                logger.error("Unknown integration strategy", strategy=strategy)
                return None
                
        except Exception as e:
            logger.error(
                "Error during menu scraping",
                url=restaurant_url,
                strategy=strategy.value,
                error=str(e),
            )
            return None
    
    async def _scrape_with_http(self, url: str) -> Optional[MenuContract]:
        """Scrape using HTTP client and BeautifulSoup."""
        
        async with WebScraper() as scraper:
            return await scraper.scrape_menu(url)
    
    async def _scrape_with_rpa(
        self,
        url: str,
        credentials: Optional[Dict[str, str]] = None
    ) -> Optional[MenuContract]:
        """Scrape using RPA bot."""
        
        domain = self._get_domain(url)
        config = self.strategy_configs.get(domain, {})
        
        async with RPABot() as bot:
            # Navigate to the website
            if not await bot.navigate_to(url):
                return None
            
            # Perform login if required
            if config.get("login_required") and credentials:
                login_config = config.get("login_config", {})
                if not await bot.login(
                    credentials.get("username", ""),
                    credentials.get("password", ""),
                    login_config
                ):
                    logger.error("Login failed, cannot proceed with scraping")
                    return None
            
            # Scrape menu
            menu_config = config.get("config", {})
            return await bot.scrape_dynamic_menu(url, menu_config)
    
    async def extract_custom_data(
        self,
        url: str,
        selectors: Dict[str, str],
        strategy: IntegrationStrategy = IntegrationStrategy.AUTO,
        credentials: Optional[Dict[str, str]] = None
    ) -> Optional[Dict[str, Any]]:
        """
        Extract custom data using provided selectors.
        
        Args:
            url: Target URL
            selectors: Dictionary mapping field names to CSS selectors
            strategy: Integration strategy to use
            credentials: Login credentials if required
        
        Returns:
            Dictionary with extracted data or None if failed
        """
        
        # Determine strategy if auto
        if strategy == IntegrationStrategy.AUTO:
            strategy = self._determine_strategy(url)
        
        logger.info(
            "Starting custom data extraction",
            url=url,
            strategy=strategy.value,
        )
        
        try:
            if strategy == IntegrationStrategy.HTTP_SCRAPING:
                async with WebScraper() as scraper:
                    return await scraper.scrape_custom_site(url, selectors)
            
            elif strategy == IntegrationStrategy.RPA:
                async with RPABot() as bot:
                    if not await bot.navigate_to(url):
                        return None
                    
                    # Perform login if credentials provided
                    if credentials:
                        domain = self._get_domain(url)
                        config = self.strategy_configs.get(domain, {})
                        login_config = config.get("login_config", {})
                        
                        if login_config:
                            await bot.login(
                                credentials.get("username", ""),
                                credentials.get("password", ""),
                                login_config
                            )
                    
                    return await bot.extract_data(selectors)
            
            else:
                logger.error("Unknown integration strategy", strategy=strategy)
                return None
                
        except Exception as e:
            logger.error(
                "Error during custom data extraction",
                url=url,
                strategy=strategy.value,
                error=str(e),
            )
            return None


# Create orchestrator instance
integration_orchestrator = IntegrationOrchestrator()