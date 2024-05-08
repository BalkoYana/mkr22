import scrapy
from mkr22.SeleniumRequest import SeleniumRequest
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from mkr22.items import Item



class OlxSpider(scrapy.Spider):
    name = "olx"
    allowed_domains = ["olx.ua"]
    start_urls = ["https://olx.ua"]
    start_urls1 = [f"https://www.olx.ua/uk/list/q-%D0%BF%D0%B8%D0%BB%D0%BE%D1%81%D0%BE%D1%81/?page={page}" for page in range(1, 25)]

    def start_requests(self):
        for url in self.start_urls1:
            yield SeleniumRequest(
                url=url,
                callback=self.parse,
                wait_time=10,
                wait_until=expected_conditions.element_to_be_clickable(
                    (By.CSS_SELECTOR,
                     "button")
                ),
                execute=self.search
            )
    def search(self, driver, wait):
        wait.until(expected_conditions.element_to_be_clickable((By.XPATH, '//input[@type="text"]')))
    def parse(self, response):
        items = response.xpath("//div[contains(@class, 'css-1sw7q4x')]")

        for item in items:
            name = item.css('::text').get().strip()
            price = item.css('p::text').get().strip()
            location_date = item.css('p[data-testid="location-date"]::text').get().strip()



            yield Item(
                name=name,
                price=price,
                place=location_date,
            )

        pass
