import os

import scrapy
import sys
sys.path.append("../testbot")
from algos import process_data


class TestbotSpider(scrapy.Spider):
    name = 'testbot'
    # start_urls = [
    #     "file:///C:/Users/Acer/PycharmProjects/PDFNetPython3/PDFNetPython3/Samples/Testfiles/Output/alg2020_html_output/cover.xhtml"
    # ]

    names = []
    lines = []
    pages_no = 408

    def start_requests(self):
        url = "file:///C:/Users/Acer/PycharmProjects/PDFNetPython3/PDFNetPython3/Samples/Testfiles/Output/alg2022_html_output/cover.xhtml"
        yield scrapy.Request(url, callback=self.parse)
        url = "file:///C:/Users/Acer/PycharmProjects/PDFNetPython3/PDFNetPython3/Samples/Testfiles/Output/alg2022_html_output/page{}.xhtml"
        # This could cause an error. Change %3d to the number of decimal places in the page number.
        numbers = ["%03d" % i for i in range(2, self.pages_no + 1)]
        for number in numbers:
            yield scrapy.Request(url.format(number), callback=self.parse)

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

        names = response.css('span.f3')
        for name in names:
            text = name.css(' ::text').extract()
            text = ' '.join([t.strip() for t in text if t.strip()])
            if not text:
                continue
            self.names.append(text)

    @staticmethod
    def close(spider, reason):
        HERE = os.path.abspath(os.path.dirname(__file__))
        os.makedirs(HERE + "/output/ALG2022", exist_ok=True)

        with open("output/ALG2022/names.txt", 'w', encoding='utf-8') as f:
            for line in spider.names:
                f.write(line + "\n")

        with open("output/ALG2022/lines.txt", 'w', encoding='utf-8') as f:
            for line in spider.lines:
                f.write(line + "\n")

        # process_data(spider.lines, spider.names)
        return super().close(spider, reason)
