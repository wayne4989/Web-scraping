from bs4 import BeautifulSoup
from collections import OrderedDict
import requests
# data to post
data = {"action": "historical_data",
        "curr_id": "277",
        "st_date": "04/04/2016",
        "end_date": "04/08/2016",
        "interval_sec": "Daily"}

# add a user agent and specify that we are making an ajax request
head = {

        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.75 Safari/537.36",
        "X-Requested-With": "XMLHttpRequest"}

with requests.Session() as s:
    r = s.post("http://www.investing.com/instruments/HistoricalDataAjax", data=data, headers=head)
    od = OrderedDict()
    soup = BeautifulSoup(r.content, "lxml")

    table = soup.select_one("table.genTbl.closedTbl.historicalTbl")
    # cols = [th.text for th in table.select("th")][1:]
    cols = [th.text for th in table.select("th")[1:]]
    for row in table.select("tr + tr"):
        data = [td.text for td in row.select("td")]
        od[data[0]] = dict(zip(cols, data[1:]))

from pprint import pprint as pp

pp(dict(od))