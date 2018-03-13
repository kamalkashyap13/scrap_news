import scrapy
import sqlite3
from sqlite3 import OperationalError
import datetime
import timeit

conn = sqlite3.connect("urls")
cursor = conn.cursor()

state1 = 'SELECT * FROM links WHERE url='  # +word

try:
    cursor.execute('''CREATE TABLE links(website text, category text, url text, date text, scrape number)''')
except OperationalError:
    None
today = str(datetime.date.today())


class QuotesSpider(scrapy.Spider):
    name = "sports"

    def start_requests(self):
        start = timeit.default_timer()
        # urls = ['http://www.thehindu.com/sci-tech/science/?page=1']
        url = 'http://www.thehindu.com/sport/?page='
        urls = ['http://www.thehindu.com/sport/']
        # for url in urls:
        #    yield scrapy.Request(url=url, callback=self.parse)
        for i in range(14):#1578
            ur = url + str(i)
            yield scrapy.Request(url=ur, callback=self.parse)
        stop = timeit.default_timer()
        self.log(stop - start)

    def parse(self, response):

        a = response.css(".Other-StoryCard h3 a::attr(href)").extract()
        b = response.css(".story-card-news a::attr(href)").extract()
        for i in range(len(a)):
            ese = state1 + '"' + a[i] + '"'
            cursor.execute(str(ese))
            result = cursor.fetchall()
            if len(result) == 0:
                ro = "INSERT INTO links VALUES ('hindu','sports','%s','%s',0)" % (a[i], today)
                self.log(ro)
                cursor.execute(ro)
        for i in range(len(b)):
            ese = state1 + '"' + b[i] + '"'
            cursor.execute(str(ese))
            result = cursor.fetchall()
            if len(result) == 0:
                ro = "INSERT INTO links VALUES ('hindu','sports','%s','%s',0)" % (b[i], today)
                self.log(ro)
                cursor.execute(ro)
        conn.commit()