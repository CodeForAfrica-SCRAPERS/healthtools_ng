from healthtools.scrapers.med_brand_names import MedBrandNamesScraper


if __name__ == "__main__":
    med_brand_names_scraper = MedBrandNamesScraper()
    med_brand_names_scraper.scrape_site()
