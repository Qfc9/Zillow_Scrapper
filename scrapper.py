import csv
from page_util import *

def loader():
    try:
        with open('house.csv', 'r', newline='') as csvfile:
            houseCSV = csv.reader(csvfile, delimiter='\t')
            houses = []
            ignoreHeader = True
            for row in houseCSV:
                house = {}
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
    except:
        return []

def find_house(houses, newHouse, msg):
    for idx, house in enumerate(houses):
        if house["link"] == newHouse["link"]:

            if house["price"] != newHouse["price"]:
                msg.append("Changed Price - " + house["addr1"] + house["addr2"])
            if house["phone"] != newHouse["phone"]:
                msg.append("Changed Phone Number - " + house["addr1"] + house["addr2"])
            if house["days"] != newHouse["days"]:
                msg.append("Changed Days on Zillow - " + house["addr1"] + house["addr2"])

            houses.pop(idx)
            return True
    return False

def scrapper(url, oldHouses, msg):
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
        house["days"] = get_data(the_page, 'Days on Zillow: </span><span class="hdp-fact-value">', '</span>')
        if house["days"].find(">") != -1:
            house["days"] = house["days"][house["days"].find(">") + 1:]
        if house["days"].find("<") != -1:
            house["days"] = house["days"][:house["days"].find("<")]


        if not find_house(oldHouses, house, msg):
            msg.append("New House - " + house["addr1"] + house["addr2"])
        houses.append(house)

    return houses


def save_houses(houses):
    with open('house.csv', 'w', newline='') as csvfile:
        houseCSV = csv.writer(csvfile, delimiter='\t')

        houseCSV.writerow(["Address 1", "Address 2", "Price", "Phone Number", "Days on Zillow", "URL"])
        for house in houses:
            houseCSV.writerow([house["addr1"], house["addr2"], house["price"], house["phone"], house["days"], house["link"]])
