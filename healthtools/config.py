import os

AWS = {
    "aws_access_key_id": os.getenv("MORPH_AWS_ACCESS_KEY_ID"),
    "aws_secret_access_key": os.getenv("MORPH_AWS_SECRET_KEY"),
    "region_name": "eu-west-1",

}

TEST_DIR = os.getcwd() + "/healthtools/tests"
