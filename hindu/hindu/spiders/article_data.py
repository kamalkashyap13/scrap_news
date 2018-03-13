import scrapy
import sqlite3
from sqlite3 import OperationalError
import datetime
import timeit
import spacy

nlp = spacy.load('en')

conn = sqlite3.connect("db.sqlite3")
cursor = conn.cursor()


state1 = 'SELECT * FROM news_articlesource WHERE article_publication_source_url='
# state2 = 'INSERT INTO links VALUES ('hindu','science','%s','%s',0)'
state2 = 'SELECT url,scrape from links WHERE date='#today
state3 = 'SELECT MAX(id) from news_articlemetadata'
state4 = 'SELECT MAX(id) from news_articlecontent'
state5 = 'SELECT MAX(id) from news_wordsindex'
state6 = 'SELECT MAX(id) from news_articlewords'
state7 = 'SELECT MAX(id) from news_articlefacts'


today = str(datetime.date.today())

com1 = 'SELECT * FROM news_articlesource WHERE article_scrapping_date=="%s"' % (today)
com2 = 'SELECT * FROM news_articlesource WHERE article_publication_source_url=="%s"' % (today)

class QuotesSpider(scrapy.Spider):
    name = "speakli_content"

    def start_requests(self):
        start = timeit.default_timer()
        cursor.execute(com1)
        result = cursor.fetchall()
        #self.log(result)
        for i in range(len(result)): # 0 to 1
            url=result[i][2]
            yield scrapy.Request(url=url,callback=self.parse)

    def parse(self, response):
        cursor.execute(str(state3))
        max_result = cursor.fetchall()
        max_id = max_result[0][0]
        max_id += 1
        ur = response.url
        article_genre = response.css('.breadcrumb li a::text').extract()
        #sub_category = response.css('.article-exclusive a::text').extract()
        if len(article_genre) == 0:
            article_genre = 'default'
        else:
            article_genre = article_genre[0].strip()
        # if len(sub_category) == 0:
        #     sub_category = ''
        # else:
        #     sub_category = sub_category[0].strip()
        article_title = response.css('.title::text').extract()[2].strip()
        article_image_source_url = ur
        article_publish_date = str(today)
        paragraph = response.css("div>p::text").extract()[:-5]
        paragraph_no = str(len(paragraph))
        article_id = "SELECT * FROM news_articlesource WHERE article_publication_source_url=='%s'" % ur
        cursor.execute(article_id)
        article_id = cursor.fetchall()
        article_id = article_id[0][0]
        # self.log("11111199999999999")
        # self.log(type(article_id))
        # self.log(type(max_id))
        ro = "INSERT INTO news_articlemetadata VALUES (%d,'%s','%s','%s',%d,'%s')" % (max_id, article_title, article_image_source_url, article_publish_date, article_id, article_genre)
        #self.log(ro)
        cursor.execute(ro)
        conn.commit()
        if len(paragraph)> 0:
            for j in range(len(paragraph)):
                cursor.execute(str(state4))
                max_result = cursor.fetchall()
                max_id = max_result[0][0]
                max_id += 1
                ro = "INSERT INTO news_articlecontent VALUES (%d,%d,'%s')" % (max_id,article_id,paragraph[j])
                self.log(ro)
                cursor.execute(str(ro)) #error
                conn.commit()
                doc = nlp(paragraph[j])
                for token in doc:
                    if token.tag_ == 'NNP':
                        word = token.text
                        state = "SELECT * FROM news_wordsindex WHERE word='%s'" % (word)
                        cursor.execute(str(state))
                        result = cursor.fetchall()
                        if len(result) == 0:
                            cursor.execute(state5)
                            max_result = cursor.fetchall()
                            max_id = max_result[0][0]
                            max_id += 1
                            ro = "INSERT INTO news_wordsindex VALUES (%d,'%s')" % (max_id,word)
                            cursor.execute(ro)
                            conn.commit()
                            cursor.execute(state6)
                            max_result_news = cursor.fetchall()
                            max_id_new = max_result_news[0][0]
                            max_id_new += 1
                            ro = "INSERT INTO news_articlewords VALUES (%d,%d,%d)" % (max_id_new, article_id, max_id)
                            cursor.execute(ro)
                            conn.commit()
                        else:
                            word_id = result[0][0]
                            cursor.execute(state6)
                            max_result_news = cursor.fetchall()
                            max_id_new = max_result_news[0][0]
                            max_id_new += 1
                            ro = "INSERT INTO news_articlewords VALUES (%d,%d,%d)" % (max_id_new, article_id, word_id)
                            cursor.execute(ro)
                            conn.commit()
                    elif token.tag_ == 'CD':
                        word = token.text
                        cursor.execute(state7)
                        max_result_news = cursor.fetchall()
                        max_id_new = max_result_news[0][0]
                        max_id_new += 1
                        ro = "INSERT INTO news_articlefacts VALUES (%d,'%s',%d)" % (max_id_new, word,article_id)
                        cursor.execute(ro)
                        conn.commit()





#https://stackoverflow.com/questions/45575608/python-sqlite-operationalerror-near-s-syntax-error
#formatting issue 's and ''
#handle title

#.justIn-story a
#techcrunch
#.post-title a
# how to work on inside a parag