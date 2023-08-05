from datetime import datetime
from django.db.utils import IntegrityError
import json
from multiprocessing import Process, Queue, Event
import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from scrapy.signalmanager import dispatcher
import sys


from .models import Author, Quote, Tag


class QuotesAuthorsSpider(scrapy.Spider):
    name = 'quotes_authors'
    allowed_domains = ['quotes.toscrape.com']
    start_urls = ['http://quotes.toscrape.com']

    author_map = {}

    def parse(self, response):
        for quote in response.xpath("/html//div[@class='quote']"):

            quotext = quote.xpath("span[@class='text']/text()").get()
            if quotext.startswith('“'):
                quotext = quotext[1:]
            if quotext.endswith('”'):
                quotext = quotext[0:len(quotext)-1]
            yield {
                "tags": quote.xpath("div[@class='tags']/a/text()").extract(),
                "author": quote.xpath("span/small/text()").get(),
                "quote": quotext,
            }

            author = quote.xpath("span/small/text()").get()
            author_link = quote.xpath("span/a/@href").get()
            if author_link in self.author_map.keys():
                continue
            self.author_map[author] = author_link


        next_link = response.xpath("//li[@class='next']/a/@href").get()
        if next_link:
            yield scrapy.Request(url=self.start_urls[0] + next_link)

        for author_as_key, about in self.author_map.items():
            yield scrapy.Request(url=self.start_urls[0] + about,
                    callback=self.parse_about,
                    cb_kwargs={"author_as_key": author_as_key})

    def parse_about(self, response, author_as_key):
        author = response.xpath("/html//div[@class='author-details']")
        yield {                        # "Alexandre Dumas fils"!="Alexandre Dumas-fils"
            "fullname": author_as_key, # author.xpath("h3/text()").get().strip()
            "born_date":
                author.xpath("p/span[@class='author-born-date']/text()")
                            .get().strip(),
            "born_location":
                author.xpath("p/span[@class='author-born-location']/text()")
                            .get().strip(),
            "description":
                author.xpath("div[@class='author-description']/text()")
                            .get().strip()
        }


def do_scrapy_content():

    print("[#] In do_scrapy_content()")


    def run_spider_process(result_queue, event):


        def crawler_results(signal, sender, item, response, spider):
            # print(f"Receive {item}")
            result_queue.put(item)

        dispatcher.connect(crawler_results, signal=scrapy.signals.item_scraped)
        settings = get_project_settings()
        settings["LOG_ENABLED"] = False


        print("[#] In run_spider_process(): calling CrawlerProcess()")
        process = CrawlerProcess(settings=settings)
        print("[#] In run_spider_process(): calling process.crawl())")
        process.crawl(QuotesAuthorsSpider)
        print("[#] In run_spider_process(): calling process.start()")
        process.start()
        print("[#] In run_spider_process(): after process.start() - data ready")
        event.set()
        sys.exit(0)

    result_queue = Queue()
    event = Event()
    spider_process = Process(target=run_spider_process, args=(result_queue, event))
    print("[#] In do_scrapy_content(): starting process...")
    spider_process.start()
    print("[#] In do_scrapy_content(): process started!")
    # spider_process.join() # Wait for the spider process to finish
    event.wait()
    print("[#] In do_scrapy_content(): data ready to receive.")

    # Retrieve the scraping results from the queue in the main process
    author_list = []
    quote_list = []
    while not result_queue.empty():
        item = result_queue.get()
        if "quote" in item.keys():
            quote_list.append(item)
        else:
            author_list.append(item)

    author_map = {}
    for a in author_list:
        fullname = a["fullname"]       # August 14, 1945
        born_date = datetime.strptime(a["born_date"], "%B %d, %Y").strftime("%Y-%m-%d")
        author, iscreated = Author.objects.get_or_create(fullname=fullname,
                            defaults={
                                "born_date": born_date,
                                "born_location": a["born_location"],
                                "description": a["description"],
                            })
        author_map[fullname] = author
        if iscreated:
            print(f"[A] New author '{fullname}'")


    tag_map = {}
    for q in quote_list:
        fullname = q["author"]
        tag_list = []
        for t in q["tags"]:
            if not t in tag_map.keys():
                tag, iscreated = Tag.objects.get_or_create(name=t)
                tag_map[t] = tag
                if iscreated:
                    print(f"[T] New tag '{t}'")
            tag_list.append(tag_map[t])

        oq = Quote()
        oq.author = author_map[fullname]
        oq.quote = q["quote"]
        try:
            oq.save()
            print(f"[Q] New quote of {fullname}: {oq}")
            for tag in tag_list:
                oq.tags.add(tag)
        except IntegrityError:
            "duplicate key value violates unique constraint"
            pass
