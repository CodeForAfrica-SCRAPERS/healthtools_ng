# Healthtools Nigeria

This is a suite of healthtools for Code for Nigeria. It contains a scraper that acquires medicine brand names from
http://rxnigeria.com/en/items. The scraper currently runs on morph.io.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Installing

Clone the repo from Github by running `$ git clone git@github.com:CodeForAfrica-SCRAPERS/healthtools_ng.git`

Change directory into package `$ cd healthtools_ng`

Install the dependencies by running `$ pip install requirements.txt`

You can set the required environment variables like so
```
$ export MORPH_AWS_ACCESS_KEY_ID= <aws_access_key_id>
$ export MORPH_AWS_SECRET_KEY= <aws_secret_key>
```

You can now run the scrapers `$ python scraper.py`

## Running the tests

Use nosetests to run tests (with stdout) like this:
```$ nosetests --nocapture```
