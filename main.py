#!/Library/Frameworks/Python.framework/Versions/3.6/bin/python3
from scrapper import *

kingCounty = "https://www.zillow.com/homes/fsbo/King-County-WA/207_rid/globalrelevanceex_sort/48.167917,-120.653229,46.687131,-122.954865_rect/8_zm/"
pierceCounter = "https://www.zillow.com/homes/fsbo/Pierce-County-WA/1322_rid/globalrelevanceex_sort/47.62838,-121.235505,46.500282,-122.993317_rect/8_zm/"


def main():
    scrapper(kingCounty)
    scrapper(pierceCounter)

main()
