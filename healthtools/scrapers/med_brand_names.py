from bs4 import BeautifulSoup
from cStringIO import StringIO
from healthtools.config import AWS
import requests
import boto3
import re
import json


class MedBrandNamesScraper(object):
    def __init__(self):
        self.batch_to_scrape = None
        self.site_url = "http://rxnigeria.com/en/items?start={}"
        self.fields = ["brand_names", "active_ingredient",
                       "theraputic_class", "company_name", "id"
                       ]
        self.s3_key = "data/med_brand_names.json"
        self.retries = 0
        self.s3 = boto3.client("s3", **{
            "aws_access_key_id": AWS["aws_access_key_id"],
            "aws_secret_access_key": AWS["aws_secret_access_key"],
            "region_name": AWS["region_name"],
        })

    def scrape_site(self):
        '''
        Scrape the whole site
        '''
        self.get_total_number_of_pages()
        all_results = []
        skipped_pages = 0

        print "Running {} ".format(type(self).__name__)
        while self.batch_to_scrape >= 0:
            url = self.site_url.format(self.batch_to_scrape)
            try:
                print "Scraping batch %s" % str(self.batch_to_scrape)
                self.retries = 0
                scraped_page = self.scrape_page(url)

                if not scraped_page:
                    print "There's something wrong with the"
                    " site or the formatting of the table."
                    return

                entries = scraped_page
                all_results.extend(entries)

                print "Scraped {} entries from page {} | {}".format(
                    len(entries),
                    self.batch_to_scrape, type(self).__name__)
                self.batch_to_scrape -= 100
            except Exception as err:
                skipped_pages += 1
                print "ERROR: scrape_site() - source: {} -"
                " page: {} - {}".format(url, self.batch_to_scrape, err)
                continue

        print "| {} completed. | {} entries retrieved. | {} pages skipped.".format(type(self).__name__, len(all_results), skipped_pages)

        if all_results:
            all_results_json = json.dumps(all_results)
            self.store_data(all_results_json)
            return all_results

    def scrape_page(self, page_url):
        '''
        Get drugs from page
        '''
        try:
            soup = self.make_soup(page_url)
            # get each drug row & avoid first row that contains headers
            rows = soup.find('table', {"id": "products"}).find_all("tr")[1:]

            entries = []
            for row in rows:
                # -1 because fields/columns has extra index; id
                columns = row.find_all("td")[:len(self.fields) - 1]

                # get drug id from drug url
                drug_url = columns[0].find('a')['href']
                pattern = re.compile("id=([^&]*)")
                drug_id = int(pattern.search(drug_url).group(1))

                columns = [text.text.strip() for text in columns]
                columns.append(drug_id)
                entry = dict(zip(self.fields, columns))
                entries.append(entry)
            return entries
        except Exception as err:
            if self.retries >= 5:
                print "ERROR: Failed to scrape data from page {} -- {} -- {}".format(page_url, str(err), row)
                return err
            else:
                self.retries += 1
                self.scrape_page(page_url)

    def store_data(self, payload):
        '''
        Upload scraped data to AWS S3
        '''
        try:
            file_obj = StringIO(payload)
            self.s3.upload_fileobj(file_obj,
                                   "cfa-healthtools-ng", self.s3_key)

            print "DEBUG - archive_data() - {}".format(self.s3_key)
            return
        except Exception as err:
            print "ERROR - archive_data() - {} - {}".format(self.s3_key, str(err))

    def get_total_number_of_pages(self):
        '''
        Get the total number of pages to be scraped
        '''
        try:
            soup = self.make_soup(self.site_url.format(0))  # get first page
            anchor = soup.find("li", {"class": "pagination-end"}).find('a')
            # what number of pages looks like
            pattern = re.compile("start=([^&]*)")
            self.batch_to_scrape = int(pattern.search(
                anchor['href']).group(1))
        except Exception as err:
            print "ERROR: get_total_page_numbers() - url: {} - err: {}".\
                format(self.site_url, str(err))
            return

    def make_soup(self, url):
        '''
        Get page, make and return a BeautifulSoup object
        '''
        response = requests.get(url)  # get first page
        soup = BeautifulSoup(response.content, "html.parser")
        return soup
