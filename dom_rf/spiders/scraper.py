import scrapy
from selenium import webdriver
from scrapy_selenium import SeleniumRequest
from bs4 import BeautifulSoup
import json

from dom_rf.items import DomRfItem


class ScraperSpider(scrapy.Spider):
    # default spider parameters
    name = "scraper"
    allowed_domains = ["xn--80az8a.xn--d1aqf.xn--p1ai"]

    # development parameters
    meta = {"dont_redirect": True}

    def __init__(self):
        self.option = webdriver.ChromeOptions()
        self.driver = webdriver.Chrome(options=self.option)

    def get_data_from_ads(self, response):
        self.driver.get(response.url)
        html_data = self.driver.page_source  # page_source returns HTML format
        soup = BeautifulSoup(html_data, 'lxml')
        json_ads_data = json.loads(soup.pre.string)  # ads data in json format
        return json_ads_data["data"]

    # default method
    def start_requests(self):
        start_url = "https://xn--80az8a.xn--d1aqf.xn--p1ai/%D1%81%D0%B5%D1%80%D0%B2%D0%B8%D1%81%D1%8B/api/kn/object?sortField=obj_publ_dt&sortType=desc&place=0-6"
        yield SeleniumRequest(url=start_url, callback=self.ads_quantity, dont_filter=True, meta=self.meta)

    def ads_quantity(self, response):
        ads_quantity: str = self.get_data_from_ads(response)["total"]
        next_url = f"https://xn--80az8a.xn--d1aqf.xn--p1ai/%D1%81%D0%B5%D1%80%D0%B2%D0%B8%D1%81%D1%8B/api/kn/object?limit={ads_quantity}&sortField=obj_publ_dt&sortType=desc&place=0-6"
        yield SeleniumRequest(url=next_url, callback=self.id_ads, dont_filter=True, meta=self.meta)

    def id_ads(self, response):
        list_ads_data = self.get_data_from_ads(response)["list"]
        for item in list_ads_data:
            id_ad: str = item["objId"]
            page_url = f"https://xn--80az8a.xn--d1aqf.xn--p1ai/%D1%81%D0%B5%D1%80%D0%B2%D0%B8%D1%81%D1%8B/api/object/{id_ad}"
            yield SeleniumRequest(url=page_url, callback=self.data_ads, dont_filter=True, meta=self.meta)

    def data_ads(self, response):
        json_ad_data = self.get_data_from_ads(response)
        item = DomRfItem()

        if "nameObj" in json_ad_data:
            item["title"] = json_ad_data["nameObj"]
        else:
            item["title"] = json_ad_data["address"]

        item["address"] = json_ad_data["address"]
        item["id_ad"] = json_ad_data["id"]
        item["commissioning"] = json_ad_data["objReady100PercDt"]
        item["developer"] = json_ad_data["developer"]["devFullCleanNm"]

        item["group_companies"] = "-"
        if "developerGroupName" in json_ad_data:
            item["group_companies"] = json_ad_data["developerGroupName"]

        item["date_publication_project"] = json_ad_data["objPublDt"]

        if "objTransferPlanDt" in json_ad_data:
            item["key_issuance"] = json_ad_data["objTransferPlanDt"]

        item["average_price_per1m"] = "-"
        if "objPriceAvg" in json_ad_data:
            item["average_price_per1m"] = json_ad_data["objPriceAvg"]

        item["sale_apartments"] = "-"
        item["real_estate_class"] = json_ad_data["objLkClassDesc"]
        item["number_apartments"] = json_ad_data["objFlatCnt"]
        yield item