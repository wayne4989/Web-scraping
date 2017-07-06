
################# scrapex install guide (refer to https://github.com/valen0214/scrapex) ###############
#  - easy_install https://github.com/valen0214/scrapex/archive/master.zip or
#  - pip install https://github.com/valen0214/scrapex/archive/master.zip

#######################################################################################################################

# Below is meaning of input params for search_boundingbox(sw_lat, sw_lng, ne_lat, ne_lng, zoom=11):

# (ne_lat, sw_lng) _______________________ (ne_lat, ne_lng)
#                  |                     |
#                  |                     |
#                  |                     |
#                  |                     |
#                  |                     |
# (sw_lat, sw_lng) |_____________________| (sw_lat, ne_lng)
# 
# Function search_boundingbox extracts all the rentals in certain region set by input params like above.

#######################################################################################################################

# US region: (24.543991, -126.000248) -> (49.622714, -66.937745) => means (start_lat, start_lng) -> (end_lat, end_lng)

# We split all region in US into many small regions.

# We do extraction step by step and there are two step values: lat_step, lng_step
# lat is incremented from sw_lat to ne_lat by lat_step.
# lng is incremented from sw_lng to ne_lng by lng_step.

# Like below:

# for lat in frange(start_lat, end_lat, lat_step):
#     for lng in frange(start_lng, end_lng, lng_step):
#         search_boundingbox(lat, lng, lat + lat_step, lng + lng_step)

########################################################################################################################

from scrapex import *
import time
import re
from cookielib import Cookie, CookieJar

s = Scraper(use_cache=False, retries=3, timeout=30)
logger = s.logger

lat_step = 0.005 # 0.01
lng_step = 0.005 # 0.01

# To get the rentals by page in certain region. JSON API.
search_url = "https://www.airbnb.com/search/search_results?page=%d&allow_override[]=&ne_lat=%f&ne_lng=%f&sw_lat=%f&sw_lng=%f&zoom=%d&search_by_map=true"
# To get the nightly-price, weekly-price, monthly-price. JSON API.
personalization_url = "https://www.airbnb.com/rooms/%d/personalization.json"
# To get the info from detail page
detail_url = 'https://www.airbnb.com/rooms/%d'

all_room_ids = []
def get_XCSRFToken(s):
    for cookie in s.client.opener.cj:
        if ( cookie.name == '_csrf_token' ):
            return cookie.value
    return None

def get_neighborhood(tree):
    neighborhood = None

    temp2 = tree.x("//div[contains(@class,'rich-toggle')]/@data-address")
    temp1 = tree.x("//table[@id='description_details']//td[text()[contains(.,'Neighborhood:')]]/following-sibling::td/descendant::text()")
    if temp2:
        temp = temp2.strip()
        if temp.find("(") == -1:
            neighborhood = temp
        else:
            neighborhood = temp[temp.find("(")+1:temp.find(")")]
    elif temp1:
        neighborhood = temp1.strip()
    
    if neighborhood is not None:
        neighborhood = neighborhood[:50]

    return neighborhood

def search_boundingbox(sw_lat, sw_lng, ne_lat, ne_lng, zoom=15):
    page = 1
    room_ids = []
    end = False
    while 1:
        doc = s.load_json(search_url % (page, ne_lat, ne_lng, sw_lat, sw_lng, zoom), headers={"X-Requested-With": "XMLHttpRequest"}, merge_headers=True)
        rentals = doc["results_json"]["search_results"]
        for rental in rentals:
            room_id = rental["listing"]["id"]

            # When reaches last page, json results would be duplicated. So return.
            if room_id in room_ids:
                end = True
                break
            room_ids.append(room_id)
            if room_id in all_room_ids:
                s.logger.info("Duplicated room_id -> %s" % str(room_id))
                continue
            all_room_ids.append(room_id)

            doc_detail = s.load(detail_url % room_id)

            city = doc_detail.x("//meta[@property='airbedandbreakfast:city']/@content")
            state = doc_detail.x("//meta[@property='airbedandbreakfast:region']/@content")
            bathrooms = doc_detail.x("//div[contains(text(), 'Bathrooms:')]/strong/text()")
            # minstay = doc_detail.x("//div[contains(text(), 'minimum stay')]/strong[contains(text(), 'night')]/text()")
            minstay = doc_detail.x("//div[text()[contains(., 'minimum stay')]]/strong[contains(text(), 'night')]/text()")
            if minstay:
                minstay = re.sub("[^\d]", "", minstay)
            else:
                minstay = ""
            try:
                # getting from -> "neighborhood_basic_info":{"neighborhood":"Botafogo","id":257}
                neighborhood = re.search("\{\"neighborhood\"\:\"([\w\s]*)\"\,", doc_detail.x("//script[contains(text(), '{\"neighborhood\":')]/text()"), re.M|re.I|re.S).group(1)
            except:
                neighborhood = get_neighborhood(doc_detail)
            try:
                # getting from -> "zipcode":"78669",
                zipcode = re.search("\"zipcode\"\:\"([0-9]*)\"\,", doc_detail.x("//script[contains(text(), '\"zipcode\":')]/text()"), re.M|re.I|re.S).group(1)
            except:
                zipcode = ""

            doc_personalization = s.load_json(personalization_url % room_id, headers={"X-Requested-With": "XMLHttpRequest"}, merge_headers=True)

            # for sample output.csv
            # info = ["host_name", rental["listing"]["user"]["first_name"],
            #         "room_id", rental["listing"]["id"],
            #         "host_id", rental["listing"]["user"]["id"],
            #         "room_type", rental["listing"]["room_type"],
            #         "neighborhood", neighborhood,
            #         "reviews", rental["listing"]["reviews_count"],
            #         "overall_satisfaction", rental["listing"]["star_rating"],
            #         "accommodates", rental["listing"]["person_capacity"],
            #         "bedrooms", rental["listing"]["bedrooms"],
            #         "bathrooms", bathrooms,
            #         "price", rental["pricing_quote"]["rate"]["amount"],
            #         "minstay", minstay,
            #         "latitude", rental["listing"]["lat"],
            #         "longitude", rental["listing"]["lng"],
            #         "collected", time.strftime("%m/%d/%Y %H:%M:%S", time.gmtime()),
            #         "rate_type", rental["pricing_quote"]["rate_type"],
            #         "city", city,
            #         "state", state,
            #         "search_term", "",
            #         "last_settings", "",
            #         ]

            # for sample_output_shortversion.xlsx
            info = [ "room_id", room_id,
                     "host_id", rental["listing"]["user"]["id"],
                     "host_name", rental["listing"]["user"]["first_name"],
                     "room_type", rental["listing"]["room_type"],
                     "neighborhood", neighborhood,
                     "Zipcode", zipcode,
                     "City", city,
                     "State", state,
                     "reviews", rental["listing"]["reviews_count"],
                     "accommodates", rental["listing"]["person_capacity"],
                     "bedrooms", rental["listing"]["bedrooms"],
                     "bathrooms", bathrooms,
                     "nightly-price", re.sub("[^0-9\.\,]", "", doc_personalization["nightly_price"]),
                     "weekly-price", re.sub("[^0-9\.\,]", "", doc_personalization["weekly_price"]),
                     "monthly-price", re.sub("[^0-9\.\,]", "", doc_personalization["monthly_price"]),
                     "minstay", minstay,
                     "latitude", rental["listing"]["lat"],
                     "longitude", rental["listing"]["lng"],
                     "collected", time.strftime("%m/%d/%Y %H:%M:%S", time.gmtime()) ]
            # s.logger.info(str(info))
            s.save(info, "result.csv")
        if (len(rentals) == 0) or (end == True):
            break
        page = page + 1

    s.logger.info("region: (%f, %f) - (%f, %f) => All %d rentals" % (sw_lat, sw_lng, ne_lat, ne_lng, len(room_ids)))

def frange(x, y, jump):
    while x < y:
        yield x
        x += jump

if __name__ == '__main__':

    # Toronto
    start_lat = 43.60277
    start_lng = -79.579468
    end_lat = 43.751753
    end_lng = -79.140701    
    # search_boundingbox(30.232563521038333, -98.40904556706784, 30.42629836404895, -97.92702042058346)
    # exit()
    for lat in frange(start_lat, end_lat, lat_step):
        for lng in frange(start_lng, end_lng, lng_step):
            search_boundingbox(lat, lng, lat + lat_step + 0.001, lng + lng_step + 0.001)
            # break
        # break

    start_lat = 43.60277
    start_lng = -79.579468
    end_lat = 43.751753
    end_lng = -79.140701      
    # search_boundingbox(30.232563521038333, -98.40904556706784, 30.42629836404895, -97.92702042058346)
    # exit()
    for lat in frange(start_lat, end_lat, lat_step):
        for lng in frange(start_lng, end_lng, lng_step):
            search_boundingbox(lat, lng, lat + lat_step + 0.001, lng + lng_step + 0.001)

    s.logger.info(str(len(all_room_ids)))
    # # ne_lat = 30.374195942736225
    # # ne_lng = -97.55897842839596
    # # sw_lat = 30.180332382365144
    # # sw_lng = -98.04100357488034
    # ne_lat = 30.42629836404895
    # ne_lng = -97.92702042058346
    # sw_lat = 30.232563521038333
    # sw_lng = -98.40904556706784
    # zoom = 11
# San Francisco
# (37.700866, -122.520693) -> (37.815410, -122.353151)
# (37.806730, -122.384050) -> (37.834935, -122.354525)
# US
# (24.543991, -126.000248) -> (49.622714, -66.937745)
# San Francisco -> new 
# (37.702845, -122.523603) -> (37.814131, -122.356233)
# (37.805587, -122.383527) -> (37.835148, -122.356576)

# San Francisco -> merge
# (37.700866, -122.523603) -> (37.815410, -122.353151)
# (37.805587, -122.384050) -> (37.835148, -122.354525)