import urllib.parse
import urllib.request
import ssl

context = ssl._create_unverified_context()

def paginate_url(url, idx):
    return "".join([url, str(idx), "/0_mmm/"])

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
    response = urllib.request.urlopen(req, context=context)
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