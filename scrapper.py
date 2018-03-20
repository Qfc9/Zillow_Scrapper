import csv
from page_util import *

def loader():
    with open('house.csv', 'r', newline='') as csvfile:
        houseCSV = csv.reader(csvfile, delimiter='\t')
        houses = []
        house = {}
        ignoreHeader = True
        for row in houseCSV:
            if ignoreHeader:
                ignoreHeader = False
                continue
            house["addr1"] = row[0]
            house["addr2"] = row[1]
            house["price"] = row[2]
            house["phone"] = row[3]
            house["days"] = row[4]
            house["link"] = row[5]
            houses.append(house)
        return houses

def scrapper(url):
    the_page = load_page(paginate_url(url, 1))
    pageCounter = get_page_count(the_page)
    houses = []

    links = get_links(the_page)

    # links = []
    # for p_num in range(1, pageCounter):
    #     the_page = load_page(paginate_url(url, p_num))
    #     links += get_links(the_page)

    for idx, link in enumerate(links):
        print(idx + 1, "of", len(links))
        house = {}
        house["link"] = 'https://www.zillow.com' + link
        the_page = load_page(house["link"])
        house["addr1"] = get_data(the_page, 'class="zsg-content-header addr">  <h1 class="notranslate">', ' <span')
        house["addr2"] = get_data(the_page, '<span class="zsg-h2 addr_city">', '</span>')
        house["price"] = get_data(the_page, 'class="main-row  home-summary-row">   <span class=""> ', ' <span class="value-suffix">')
        house["phone"] = clean_phone(get_data(the_page, 'Property Owner</span>            <span class="snl phone">', '</span>'))
        house["days"] = get_data(the_page, 'Days on Zillow</p>', 'Days')
        if house["days"].find(">") != -1:
            house["days"] = house["days"][house["days"].find(">") + 1:]
        if house["days"].find("<") != -1:
            house["days"] = house["days"][:house["days"].find("<")]

        houses.append(house)

    for house in houses:
        print(house["addr1"])
        print(house["addr2"])
        print(house["price"])
        print(house["phone"])
        print(house["days"])

    with open('house.csv', 'w', newline='') as csvfile:
        houseCSV = csv.writer(csvfile, delimiter='\t')

        houseCSV.writerow(["Address 1", "Address 2", "Price", "Phone Number", "Days on Zillow", "URL"])
        for house in houses:
            houseCSV.writerow([house["addr1"], house["addr2"], house["price"], house["phone"], house["days"], house["link"]])