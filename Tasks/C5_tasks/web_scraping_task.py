import argparse
import os
import random
import time
import wget
from datetime import date

import lxml
import pandas as pd
import requests
from bs4 import BeautifulSoup


def get_product_image_url(webpage_content):
    """Function used to fetch the product image URL"""
    try:
        image_src_div = webpage_content.find("div", attrs={"class": "npi_image"})

        image_tags = image_src_div.find_all("img")
        if len(image_tags) > 1:
            image_src_url = image_tags[-1].get("src").strip()
        else:
            image_src_url = image_tags[0].get("src").strip()
        split_url = image_src_url.split("&")[0] + "&height=600&width=600&extend=white"
        image_src_url = split_url
    except Exception as error:
        print("The product image link could not be found!")
        print(f"Error: {error}")
        image_src_url = ""

    return image_src_url


def get_product_title(webpage_content):
    """Function used to fetch the product title"""
    try:
        # Get the div tag that contains the product title
        title_div = webpage_content.find("div", attrs={"class": "npi_name"})
        title = title_div.find("h2").text

        # Get the title as a string value
        title_string = title.strip()

    except AttributeError as error:
        print("The title of product could not be found!")
        print(f"Error: {error}")
        title_string = ""

    return title_string


def get_product_price(webpage_content):
    """Function used to fetch the product price"""
    try:
        # Get the div that contains the product price
        price_div = webpage_content.find("div", attrs={"class": "price_block_list"})
        product_price = price_div.find("span", attrs={"class": "real_price"}).text.strip()

    except AttributeError as error:
        print("The product price could not be found!")
        print(f"Error: {error}")
        product_price = ""

    return product_price


def get_product_stock(webpage_content):
    """Function used to fetch the current product stock"""
    try:
        # Get the div element that contains the current stock information
        product_stock_div = webpage_content.find("div", attrs={"class": "stoc_produs"})
        product_stock = product_stock_div.find("span").text.strip()

    except AttributeError as error:
        print("The product current stock could not be determined!")
        print(f"Error: {error}")
        product_stock = "Check on the site"

    return product_stock


def get_product_link(webpage_content):
    """Function used to fetch the product URL"""
    try:
        # Get the div that contains the product URL
        product_link_div = webpage_content.find("div", attrs={"class": "npi_name"})
        product_link = "https://www.evomag.ro" + product_link_div.find("a").get("href").strip()
    except AttributeError as error:
        print("The product link could not be found!")
        print(f"Error: {error}")
        product_link = ""

    return product_link


def webscrape_products_information(user_agents, product_category):
    """This function is used to scrape all the information about the products"""
    collected_data = []

    for page_number in range(1, 150):

        # Header of the requests
        headers = ({"User-Agent": user_agents[random.randint(0, len(user_agents) - 1)],
                    "Accept-Language": "en,ro-RO;q=0.9,ro;q=0.8,en-US;q=0.7"})

        # Select the appropriate category link based on user input
        if product_category == "video_card":
            URL = "https://www.evomag.ro/componente-pc-gaming-placi-video/filtru/pagina:{}".format(page_number)
            image_prefix = "video_card"
            storage_location = "Placi_video\\"
        elif product_category == "laptop":
            URL = "https://www.evomag.ro/portabile-laptopuri-notebook/filtru/pagina:{}".format(page_number)
            image_prefix = "laptop"
            storage_location = "Laptop\\"
        else:
            print("Invalid argument! Please use one of the available options!")

        # Show the current page scraped
        print(f"\n Page: {page_number}")

        # HTTP request to obtain the content of the web page
        webpage = requests.get(URL, headers=headers)
        time.sleep(2)

        # BS4S Object with all the content on the webpage
        soup = BeautifulSoup(webpage.content, "lxml")

        # Get the products listed on the page
        listed_content = soup.find("div", attrs={"class": "product_grid"})

        # To receive the required information, select all product cards
        all_product_cards = listed_content.find_all("div", attrs={"class": "nice_product_container"})

        # Display the number of products from the page to ensure the scraper works properly
        print("#################################")
        print(len(all_product_cards))
        print("#################################")

        # Go back over every product card and retrieve the data
        for product_card in all_product_cards:
            collected_data.append(
                [get_product_title(product_card),
                 get_product_price(product_card),
                 get_product_stock(product_card).replace("î", "i"),
                 get_product_link(product_card),
                 get_product_image_url(product_card),
                 date.today(),
                 "evoMAG"]
            )

        # Verify if the last page of products has been reached; if so, the data will be stored
        try:
            next_page_exists = soup.find("div",
                                         attrs={
                                             "class": "pagination"
                                         }).find("li",
                                                 attrs={
                                                     "class": "next hidden"
                                                 })
            if next_page_exists is not None:
                print("\n----------------------------------------------------")
                print(f"Scraper reached last page for {product_category}. Scraping process COMPLETE!")
                print("----------------------------------------------------\n")
                break
            # Debug log
            # print(next_page_exists)
        except AttributeError:
            print("----------------------------------------------------")
            print(f"Scraper reached last page for {product_category}. Scraping process COMPLETE!")
            print("----------------------------------------------------")
            break

        time.sleep(5)

    return collected_data


def store_products_data(data, product_category):
    """This function is used to store the information for each product category"""
    products_df = pd.DataFrame(data,
                               columns=["Product Name",
                                        "Price",
                                        "Stock",
                                        "Product URL",
                                        "Product Image URL",
                                        "Date",
                                        "Store Name"])

    current_directory = os.getcwd()

    # Choose which file will hold the information for the selected product category
    if product_category == "video_card":
        save_directory = current_directory + "/video_card.csv"
        products_df.to_csv(save_directory, index=False)
    elif product_category == "laptop":
        save_directory = current_directory + "/laptop_data.csv"
        products_df.to_csv(save_directory, index=False)
    else:
        print("When choosing the place to save the product information, an error occurred.")


def read_stored_information(product_category):
    """This function will display the product information
    gathered from the in the console in a tabular format."""
    current_directory = os.getcwd()

    # Select the file to be shown according to the specified product category.
    if product_category == "video_card":
        display_file_path = current_directory + "/video_card.csv"
        stored_products_df = pd.read_csv(display_file_path)
        print(stored_products_df)
    elif product_category == "laptop":
        display_file_path = current_directory + "/laptop_data.csv"
        stored_products_df = pd.read_csv(display_file_path)
        print(stored_products_df)
    else:
        print("Unfortunately, there is no file for the category you specified.")
    return


def append_product_information(saved_category, added_category, user_agent_list):
    """This function is used to append product data to an existing category."""

    print(f"Starting to collect information from the {added_category} category.")
    added_products_data = webscrape_products_information(user_agent_list, added_category)

    # Get current working directory
    current_directory = os.getcwd()

    # Load the saved category file
    if saved_category == "video_card":
        file_path = current_directory + "/video_card.csv"
        stored_products_df = pd.read_csv(file_path)
    elif saved_category == "laptop":
        file_path = current_directory + "/laptop_data.csv"
        stored_products_df = pd.read_csv(file_path)
    else:
        print("The given category does not exits.")

    # Combine the two sets of information into a list
    combined_product_data = stored_products_df.to_numpy().tolist() + added_products_data

    store_products_data(combined_product_data, saved_category)


if __name__ == "__main__":
    """
    This is a script to fetch information from evoMAG online store.
    To run this script you need to follow this examples:
    python web_scraping_task.py -c video_card
    python web_scraping_task.py -d video_card
    python web_scraping_task.py -a laptop video_card
    """
    webscrape_products_data = []

    # User agent list to get around website bot security
    user_agent_list = [
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko; Google Web Preview) Chrome/27.0.1453 Safari/537.36",
        "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; HPNTDF)",
        "Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; msn OptimizedIE8;ENUS; rv:11.0) like Gecko",
        "Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3",
        "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.7.5) Gecko/20041107 Firefox/1.0",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.31 (KHTML, like Gecko) Chrome/26.2.9999.797 Safari/537.31",
        "Mozilla/5.0 (X11; Linux x86_64; rv:27.0) Gecko/20100101 Firefox/27.0",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_8) AppleWebKit/534.59.10 (KHTML, like Gecko) Version/5.1.9 Safari/534.59.8 Java/1.7.0_45",
        "Mozilla/5.0 (Linux; U; Android 4.0.3; en-us; HTC_PH39100/3.26.502.56 Build/IML74K) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30",
        "Mozilla/5.0 (Windows NT 6.2; WOW64; rv:16.0.1) Gecko/20121011 Firefox/16.0.1",
        "Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; Win64; x64; Trident/6.0; MAAU)",
        "Mozilla/4.0 (Windows; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 2.0.50727)",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1599.101 Safari/537.36",
        "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.4 (KHTML, like Gecko) Chrome/22.0.1229.79 Safari/537.4",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:2.0b11pre) Gecko/20110126 Firefox/4.0b11pre",
        "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10.6; en-US; rv:1.9.2.14) Gecko/20110218 AlexaToolbar/alxf-2.0 Firefox/3.6.14",
        "Mozilla/5.0 (Windows; U; Windows NT 5.0; de; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.95 Safari/537.11",
        "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.1; .NET CLR 1.1.4322; Alexa Toolbar)",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.34 Safari/537.36",
        "Mozilla/5.0 (X11; Linux i686) AppleWebKit/535.1 (KHTML, like Gecko) Ubuntu/11.04 Chromium/14.0.835.202 Chrome/14.0.835.202 Safari/535.1",
        "Mozilla/5.0 (Windows NT 6.2; Win64; x64; rv:16.0.1) Gecko/20121011 Firefox/16.0.1",
        "Opera/9.80 (Windows NT 6.1; WOW64; MRA 6.0 (build 5998)) Presto/2.12.388 Version/12.10",
        "Mozilla/5.0 (Windows NT 6.1; rv:2.0b10pre) Gecko/20110113 Firefox/4.0b10pre",
        "Mozilla/5.0 (iPad; U; CPU OS 4_3_3 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8J2 Safari/6533.18.5",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.2; WOW64; Trident/6.0; .NET4.0E; .NET4.0C; .NET CLR 3.5.30729; .NET CLR 2.0.50727; .NET CLR 3.0.30729; HPDTDFJS; InfoPath.3)",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/6.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; ms-office)",
        "Mozilla/5.0 (Linux; U; Android 4.1.2; en-us; SAMSUNG-SGH-I497 Build/JZO54K) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Safari/534.30",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_5) AppleWebKit/537.73.11 (KHTML, like Gecko) Version/6.1.1 Safari/537.73.11",
        "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.91 Safari/537.11",
        "Opera/9.80 (Windows NT 6.1; WOW64; U; Edition Next; Edition Yx; ru) Presto/2.11.310 Version/12.50",
        "Mozilla/5.0 (Windows NT 6.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.63 Safari/537.36",
        "Mozilla/5.0 (Windows NT 5.2; rv:26.0) Gecko/20100101 Firefox/26.0",
        "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1700.72 Safari/537.36",
        "Mozilla/5.0 (Windows NT 5.1; rv:26.0) Gecko/20100101 Firefox/26.0 SeaMonkey/2.23",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1700.72 Safari/537.36",
        "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1700.41 Safari/537.36",
        "Mozilla/5.0 (Macintosh; U; Intel Mac OS X; en-gb) AppleWebKit/523.10.6 (KHTML, like Gecko) Version/3.0.4 Safari/523.10.6",
        "Mozilla/5.0 (Linux; U; Android 4.2.2; en-us; SM-T310 Build/JDQ39) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Safari/534.30",
    ]

    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--category",
                        help="Choose which category from the site will be scanned.",
                        choices=["video_card", "laptop"])
    parser.add_argument("-d", "--display",
                        help="If a file containing the gathered data exists, select which product category to display "
                             "it for.",
                        choices=["video_card", "laptop"])
    parser.add_argument("-a", "--append",
                        help="Select which product category will be added to the current product category data that "
                             "has been gathered.",
                        choices=["video_card", "laptop"],
                        nargs=2)
    args = parser.parse_args()

    if args.category is not None and args.display is None and args.append is None:
        # Show the chosen category
        print(f"Starting scraping process.\n Selecting {args.category} URL...")
        webscrape_products_data = webscrape_products_information(user_agent_list, args.category)

        print("\n----------------------------------------------------")
        print(f"Total number of products for {args.category} category: {len(webscrape_products_data)}")
        print("----------------------------------------------------\n")

        # Save all the data that was scraped
        print(f"Saving {args.category} collected data...")
        store_products_data(webscrape_products_data, args.category)
    elif args.display is not None and args.category is None and args.append is None:
        read_stored_information(args.display)
    elif args.append is not None and args.category is None and args.display is None:
        append_product_information(args.append[0], args.append[1], user_agent_list)
    else:
        print("Please use only one argument!")
