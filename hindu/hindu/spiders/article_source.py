import scrapy
import sqlite3
from sqlite3 import OperationalError
import datetime
import timeit


#http://www.thehindu.com/sci-tech/science/?page=
conn = sqlite3.connect("db.sqlite3")
cursor = conn.cursor()

state1 = 'SELECT * FROM news_articlesource WHERE article_publication_source_url='
# state2 = 'INSERT INTO links VALUES ('hindu','science','%s','%s',0)'
state3 = 'SELECT MAX(id) from news_articlesource'

today = str(datetime.date.today())



url = 'http://www.thehindu.com/sci-tech/science/?page='
class QuotesSpider(scrapy.Spider):
    name = "speakli_src"

    def start_requests(self):
        start = timeit.default_timer()
        for i in range(1):#143
            ur = url+str(i)
            yield scrapy.Request(url=ur,callback=self.parse)
        stop = timeit.default_timer()
        self.log(stop - start)

    def parse(self, response):

        a = response.css(".Other-StoryCard h3 a::attr(href)").extract()
        b = response.css(".story-card-news a::attr(href)").extract()
        for i in range(len(a)):
            # cursor.execute(str(state3))
            ese = state1 + '"' + a[i]+'"'
            cursor.execute(str(ese))
            result = cursor.fetchall()
            if len(result) == 0:
                cursor.execute(str(state3))
                max_result = cursor.fetchall()
                max_id = max_result[0][0]
                max_id += 1
                ro = "INSERT INTO news_articlesource VALUES (%d,'hindu','%s','%s',3)" %(max_id,a[i],today)
                self.log(ro)
                cursor.execute(ro)
        for i in range(len(b)):
            ese = state1 + '"' + b[i]+'"'
            cursor.execute(str(ese))
            result = cursor.fetchall()
            if len(result) == 0:
                cursor.execute(str(state3))
                max_result = cursor.fetchall()
                max_id = max_result[0][0]
                max_id += 1
                ro = "INSERT INTO news_articlesource VALUES (%d,'hindu','%s','%s',3)" % (max_id, b[i], today)
                self.log(ro)
                cursor.execute(ro)
        conn.commit()

    #scrapy crawl science

    #handle error
    #add category



