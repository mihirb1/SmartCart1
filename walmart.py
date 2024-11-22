from bs4 import BeautifulSoup
import requests
import pandas as pd


def get_title(soup) -> str:
    try:
        title = soup.find("span", attrs={"id": 'productTitle'}).text.strip()
    except AttributeError:
        title = ""
    return title


def get_price(soup) -> str:
    # print(soup.find("span", attrs={"id": 'alm_accordion_estimatedSubtotalForSUPW'}))
    if soup.find("span", attrs={"id": 'alm_accordion_estimatedSubtotalForSUPW'}) is not None:
        # print("entered")
        price = soup.find("span", attrs={"id": "alm_accordion_estimatedSubtotalForSUPW"}).find("span", attrs={
            "class": 'a-size-small a-color-base'}).text.strip()
        return price
    else:
        try:
            price = soup.find("span", attrs={
                "class": 'a-price aok-align-center reinventPricePriceToPayMargin priceToPay'}).find("span", attrs={
                "class": 'a-offscreen'}).text
            if price.strip() == "":
                price = '$' + soup.find("span", attrs={"class": 'a-price-whole'}).text.strip() + soup.find("span",
                                                                                                           attrs={
                                                                                                               "class": 'a-price-fraction'}).text.strip()
            return price
        except AttributeError:
            price = ""
        return price


def get_unit_price(soup) -> str:
    if soup.find("span", attrs={"id": "alm_accordion_estimatedSubtotalForSUPW"}) is not None:
        # print("entered")
        per_unit = soup.find("span", attrs={"class": 'a-price aok-align-center'}).find("span", attrs={
            "class": 'a-offscreen'}).text.strip()
        return per_unit
    else:
        try:
            per_unit = soup.find("span", attrs={"class": 'a-price a-text-price'}).find("span", attrs={
                "class": 'a-offscreen'}).text.strip()
            if per_unit == "":
                my_list = soup.find("span", attrs={"class": 'aok-offscreen'}).text.split()
                per_unit = my_list[0]
                return per_unit
        except AttributeError:
            per_unit = ""
        return per_unit


def get_unit(soup) -> str:
    unit = ""
    if soup.find("span", attrs={"id": "alm_accordion_estimatedSubtotalForSUPW"}) is not None:
        # print("entered")
        full_text = soup.find("div", attrs={"class": 'a-section a-spacing-micro a-padding-none'}).text.strip()
        without_spaces = full_text.replace(" ", "")
        index_of_dash = without_spaces.find("/")
        first_parenthesis = without_spaces.find("(")
        unit = without_spaces[index_of_dash + 1: first_parenthesis].strip()
        return unit
    else:
        try:
            if soup.find("span",
                         attrs={"class": 'a-size-mini a-color-base aok-align-center a-text-normal'}) is not None:
                #print("entered if")
                #print(soup.find("span", attrs={"class": 'a-size-mini a-color-base aok-align-center a-text-normal'}))
                find_price = soup.find("span", attrs={"class": 'a-size-mini a-color-base aok-align-center a-text-normal'}).text
                index_of_slash = find_price.find("/")
                index_of_end_parenthesis = find_price.find(")")
                unit = find_price[index_of_slash + 1:index_of_end_parenthesis].strip()
                return unit
            elif unit == "":
                # print("entered first elif")
                # print("finding unit in aok-offscreen")
                find_price = soup.find("span", attrs={"class": "a-size-mini aok-offscreen"}).text
                index_of_per = find_price.find("per")
                unit = find_price[index_of_per + 4:]
                return unit

            elif unit == "":
                # ("entered second elif")
                my_list = soup.find("span", attrs={"class": 'aok-offscreen'}).text.split()
                unit = my_list[2]
                return unit
        except AttributeError:
            # print("Attribute error")
            unit = ""
        return unit


def get_availability(soup):
    availability = ""
    try:
        if soup.find("span", attrs={"class": 'a-size-medium a-color-success'}) is not None:
            availability = soup.find("span", attrs={"class": 'a-size-medium a-color-success'}).text.strip()
            return availability
        elif soup.find("span", attrs={"class": 'a-size-medium a-color-price a-text-bold'}) is not None:
            availability = soup.find("span", attrs={"class": 'a-size-medium a-color-price a-text-bold'}).text.strip()
            return availability
        elif soup.find("span", attrs={"class": 'a-size-base a-color-price a-text-bold'}) is not None:
            availability = soup.find("span", attrs={"class": 'a-size-base a-color-price a-text-bold'}).text.strip()
            return availability
    except AttributeError:
        availability = ""
    return availability


if __name__ == '__main__':

    HEADERS = ({
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
        'Accept-Language': 'en-US, en;q=0.6'})
    URL = "https://www.walmart.com/Fresh-Fruits/b?ie=UTF8&node=16318981"

    webpage = requests.get(URL, headers=HEADERS)
    soup = BeautifulSoup(webpage.content, "html.parser")

    links = soup.find_all("a", attrs={
        'class': 'a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal'})

    # link = links[20].get('href')
    links_list = []
    for link in links:
        links_list.append(link.get('href'))
    d = {"title": [], "total price": [], "price per unit": [], "unit": [], "availability": []}

    for page in range(1, 27):  # Looping through all 26 pages
            print(f"Scraping page {page}")
            URL = f"https://www.walmart.com/s?k=Fresh+Fruits&i=grocery&rh=n%3A16318981&page={page}&c=ts&qid=1731997546&ts_id=16318981&ref=sr_pg_{page}"
            webpage = requests.get(URL, headers=HEADERS)
            soup = BeautifulSoup(webpage.content, "html.parser")

            links = soup.find_all("a", attrs={
                'class': 'a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal'})

            links_list = [link.get('href') for link in links]

            for link in links_list:
                if link.startswith("/"):
                    new_webpage = requests.get(f"https://walmart.com{link}", headers=HEADERS)
                else:
                    new_webpage = requests.get(link, headers=HEADERS)
                new_soup = BeautifulSoup(new_webpage.content, "html.parser")

                title = get_title(new_soup)
                print("product is:", title)
                d['title'].append(title)

                total_price = get_price(new_soup)
                print("total price is:", total_price)
                d['total price'].append(total_price)

                per_unit = get_unit_price(new_soup)
                print("price per unit is:", per_unit)
                d['price per unit'].append(per_unit)

                unit = get_unit(new_soup)
                print("unit is:", unit)
                d['unit'].append(unit)

                availability = get_availability(new_soup)
                print("availability is:", availability)
                d['availability'].append(availability)

                print("")


    df = pd.DataFrame(d)
    df.to_csv("walmart_products.csv", index=False)
    print("Scraping completed and data saved to walmart_products.csv")
