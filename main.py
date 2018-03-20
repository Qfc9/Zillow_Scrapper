#!/Library/Frameworks/Python.framework/Versions/3.6/bin/python3
import csv
from page_util import *

kingCounty = "https://www.zillow.com/homes/fsbo/King-County-WA/207_rid/globalrelevanceex_sort/48.167917,-120.653229,46.687131,-122.954865_rect/8_zm/"
pierceCounter = "https://www.zillow.com/homes/fsbo/Pierce-County-WA/1322_rid/globalrelevanceex_sort/47.62838,-121.235505,46.500282,-122.993317_rect/8_zm/"


def main():
    the_page = load_page(paginate_url(kingCounty, 1))
    pageCounter = get_page_count(the_page)
    houses = []

    links = get_links(the_page)

    # links = []
    # for p_num in range(1, pageCounter):
    #     the_page = load_page(paginate_url(kingCounty, p_num))
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

        houseCSV.writerow(["addr1", "addr2", "price", "phone", "days", "link"])
        for house in houses:
            houseCSV.writerow([house["addr1"], house["addr2"], house["price"], house["phone"], house["days"], house["link"]])


main()
