import scrapy
import sqlite3
from sqlite3 import OperationalError
import datetime
import timeit

conn = sqlite3.connect("urls")
cursor = conn.cursor()

state1 = 'SELECT * FROM links WHERE url='#+word

try:
    cursor.execute('''CREATE TABLE links(website text, category text, url text, date text, scrape number)''')
except OperationalError:
    None
today = str(datetime.date.today())


class QuotesSpider(scrapy.Spider):
    name = "techcrunch"

    def start_requests(self):
        start = timeit.default_timer()
        urls = ['https://techcrunch.com/page/1/']
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)


    def parse(self, response):

        a = response.css(".post-title a::attr(href)").extract()
        for i in range(len(a)):
            ese = state1 + '"' + a[i]+'"'
            cursor.execute(str(ese))
            result = cursor.fetchall()
            if len(result) == 0:
                ro = "INSERT INTO links VALUES ('techcrunch','tech','%s','%s',0)" %(a[i],today)
                self.log(ro)
                cursor.execute(ro)

        conn.commit()


#alpha tweet-title
#response.css('h1::title').extract()
#response.css('.article-entry img::attr(src)').extract()
#response.css('.article-entry p::text').extract()
#https://www.washingtonpost.com/?reload=true
#procon.org
#https://www.inshorts.com/en/ajax/more_news
# a=response.css('.news-card-title a span::text').extract()
#republic




