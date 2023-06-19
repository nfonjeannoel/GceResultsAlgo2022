import os

import scrapy
import sys
sys.path.append("../testbot")
from algos import process_data


class FixerbotSpider(scrapy.Spider):
    name = 'fixer'
    # start_urls = [
    #     "file:///C:/Users/Acer/PycharmProjects/PDFNetPython3/PDFNetPython3/Samples/Testfiles/Output/alg2020_html_output/cover.xhtml"
    # ]

    names = []
    lines = []
    pages_no = 361

    def start_requests(self):
        url = "file:///C:/Users/Acer/PycharmProjects/PDFNetPython3/PDFNetPython3/Samples/Testfiles/Output/alg2021_html_output/cover.xhtml"
        yield scrapy.Request(url, callback=self.parse)

    def parse(self, response):

        spans = response.css('span')

        centers = response.css(".fs2 ::text").getall()
        centers = "".join(centers)
        centers = centers.split("Centre")
        centers = [center.strip() for center in centers if center.strip()]
        centers = ["Centre " + c for c in centers]
        center_ind = 0

        for span in spans:
            text = span.css(' ::text').extract()
            text = [t.strip() for t in text if t.strip()]
            # text = ''.join([t.strip() for t in text if t.strip()])
            if not text:
                continue
            if text[0].lower() == "cent":
                text = centers[center_ind].strip()
                center_ind += 1
            else:
                text = " ".join(text)
            self.lines.append(text)

        names = response.css('span.f2')
        for name in names:
            text = name.css(' ::text').extract()
            text = ' '.join([t.strip() for t in text if t.strip()])
            if not text:
                continue
            self.names.append(text)

    @staticmethod
    def close(spider, reason):
        HERE = os.path.abspath(os.path.dirname(__file__))
        os.makedirs(HERE + "/output/ALG2021", exist_ok=True)

        with open("output/ALG2021/names.txt", 'w', encoding='latin-1') as f:
            for line in spider.names:
                f.write(line + "\n")

        with open("output/ALG2021/lines.txt", 'w', encoding='latin-1') as f:
            for line in spider.lines:
                f.write(line + "\n")

        # process_data(spider.lines, spider.names)
        return super().close(spider, reason)
