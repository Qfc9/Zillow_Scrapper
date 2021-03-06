#!/Library/Frameworks/Python.framework/Versions/3.6/bin/python3
from scrapper import *

kingCounty = "https://www.zillow.com/homes/fsbo/King-County-WA/house,condo,mobile,townhouse_type/207_rid/1-_beds/150000-_price/592-_mp/globalrelevanceex_sort/47.989921,-120.925141,46.86958,-122.682953_rect/8_zm/"
pierceCounter = "https://www.zillow.com/homes/fsbo/Pierce-County-WA/house,condo,mobile,townhouse_type/1322_rid/1-_beds/149961-_price/592-_mp/globalrelevanceex_sort/47.62838,-121.235505,46.500282,-122.993317_rect/8_zm/"

def main():
    msg = []
    houses = []
    loadedHouses = loader()

    print("Getting King County...")
    houses += scrapper(kingCounty, loadedHouses, msg)
    print("Getting Pierce County...")
    houses += scrapper(pierceCounter, loadedHouses, msg)
    save_houses(houses)

    remove_houses(loadedHouses, msg)

    if msg:
        print("\n", len(msg), "Changes")
        print("\n".join(msg))
    else:
        print("\nNo Changes")

main()
