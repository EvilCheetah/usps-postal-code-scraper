'''
    Author: Eugene Moshchyn
    Description:
        The script uses the beauty of the async programming to 
        obtain Postal Code data via USPS API
'''
from dotenv import load_dotenv

from config import config
from scraper import get_postal_codes


def main():
    load_dotenv()

    config()

    data = get_postal_codes()


if __name__ == '__main__':
    try:
        main()

    except KeyboardInterrupt:
        print("Program was terminated...")
