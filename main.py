
# https://www.zillow.com/homes/fsbo/King-County-WA/207_rid/globalrelevanceex_sort/48.167917,-120.653229,46.687131,-122.954865_rect/8_zm/0_mmm/

import csv
import urllib.parse
import urllib.request

def main():
    the_page = load_page('https://www.zillow.com/homes/fsbo/King-County-WA/207_rid/globalrelevanceex_sort/48.167917,-120.653229,46.687131,-122.954865_rect/8_zm/0_mmm/')
    pageCounter = get_page_count(the_page)
    houses = []

    links = get_links(the_page)

    # links = []
    # for p_num in range(1, pageCounter):
    #     the_page = load_page('https://www.zillow.com/homes/fsbo/King-County-WA/207_rid/globalrelevanceex_sort/48.167917,-120.653229,46.687131,-122.954865_rect/8_zm/'+ str(p_num) +'_p/0_mmm/')
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

def clean_phone(phone):
    cleaned = []
    for c in phone:
        if c.isdigit() or c in ["(", ")", "-", " "]:
            cleaned.append(c)

    return "".join(cleaned)

def get_data(page, sStr, eStr):
    start = page.find(sStr)
    if start == -1:
        return "Not Found"
    else:
        start += len(sStr)
    end = page.find(eStr, start)
    if end == -1:
        return "Not Found"
    return page[start:end]

def load_page(url):
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'
    # user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
    headers = { 'User-Agent' : user_agent }

    # data = urllib.parse.urlencode(values)
    req = urllib.request.Request(url, None, headers)
    response = urllib.request.urlopen(req)
    return str(response.read())

def get_page_count(page):
    pageCounter = 1
    startPages = page.index('<div id="search-pagination-wrapper" class="zsg-content-item">')
    endPages = page.index("</ol>")
    while page.find('<li>', startPages, endPages) != -1:
        pageCounter += 1
        startPages = page.index('</li>', startPages, endPages) + 5

    return pageCounter

def get_links(page):
    start = page.index('<ul class="photo-cards">')
    end = page.index('</ul>', start)
    links = []

    while page.find('href="', end) != -1:
        start = (page.index('href="', start) + 6)
        end = page.index('"', start)
        if page.find("homedetails", start, end) != -1:
            links.append(page[start:end])

    return links

main()
