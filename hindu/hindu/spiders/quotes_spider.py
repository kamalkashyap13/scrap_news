import scrapy
import sqlite3
from sqlite3 import OperationalError
import datetime
import timeit

conn = sqlite3.connect("db.sqlite3")
cursor = conn.cursor()

state1 = 'SELECT * FROM news_articlesource WHERE article_publication_source_url='#+word

try:
    cursor.execute('''CREATE TABLE news_articlesource (id integer, article_website_Source text, article_publication_source_url text, article_scrapping_date date, article_category text, scrape number)''')
except OperationalError:
    None
today = str(datetime.date.today())


class QuotesSpider(scrapy.Spider):
    name = "science"

    def start_requests(self):
        start = timeit.default_timer()
        url = 'http://www.thehindu.com/sci-tech/science/?page='
        urls = ['http://www.thehindu.com/sport/']
        for i in range(1):#143
            ur = url+str(i)
            yield scrapy.Request(url=ur,callback=self.parse)
        stop = timeit.default_timer()
        self.log(stop - start)

    def parse(self, response):

        a = response.css(".Other-StoryCard h3 a::attr(href)").extract()
        b = response.css(".story-card-news a::attr(href)").extract()
        for i in range(len(a)):
            ese = state1 + '"' + a[i]+'"'
            cursor.execute(str(ese))
            result = cursor.fetchall()
            if len(result) == 0:
                ro = "INSERT INTO links VALUES ('hindu','science','%s','%s',0)" %(a[i],today)
                self.log(ro)
                cursor.execute(ro)
        for i in range(len(b)):
            ese = state1 + '"' + b[i]+'"'
            cursor.execute(str(ese))
            result = cursor.fetchall()
            if len(result) == 0:
                ro = "INSERT INTO links VALUES ('hindu','science','%s','%s',0)" %(b[i],today)
                self.log(ro)
                cursor.execute(ro)
        conn.commit()

    #scrapy crawl science
