import threading
import time

import scrapy
from PyPDF2 import PdfWriter, PdfReader
import aspose.words as aw


def save_file(page_writer, ind):
    with open(f"output/outputh{ind}.pdf", "wb") as fp:
        page_writer.write(fp)

    time.sleep(2)
    # Load the PDF file
    doc = aw.Document(f"output/outputh{ind}.pdf")

    # Save the document as HTML
    doc.save(f"output/out_html{ind}.html")
    print(f"Saved file {ind}")
    time.sleep(1)


class GcebotSpider(scrapy.Spider):
    name = 'gcebot'
    pdf_path = 'ALG2022.pdf'
    lines = []
    mydic = {}
    no_lines = 0

    def start_requests(self):
        pdf_path = self.pdf_path
        reader = PdfReader(pdf_path)

        threads = []

        self.no_lines = len(reader.pages)
        for page_ind in range(len(reader.pages)):
            writer = PdfWriter()
            current_page = reader.pages[page_ind]
            writer.add_page(current_page)

            t = threading.Thread(target=save_file, args=(writer, page_ind,))
            threads.append(t)

        for t in threads:
            t.start()

        for t in threads:
            t.join()

        for i in range(len(reader.pages)):
            url = f"file:///C:/Users/Acer/PycharmProjects/GceResultsAlgo2022/gcebot/output/out_html{i}.html"
            yield scrapy.Request(url, callback=self.parse, meta={"page_ind": i, "total": len(reader.pages)})

    def parse(self, response):
        self.log(f"Parsing page {response.meta['page_ind']} of {response.meta['total']}")
        p = response.css("p")
        lines = []
        for line in p:
            text = line.css("span ::text").extract()
            text = [t.strip() for t in text if t.strip()]
            text = " ".join(text)
            lines.append(text)
        self.mydic[response.meta['page_ind']] = lines

    @staticmethod
    def close(spider, reason):
        print("save to file")
        all_data = []
        print("number of pages: ", spider.no_lines)
        for i in range(spider.no_lines):
            data = spider.mydic[i]
            all_data += data

        # print(f"all_data: {all_data}")

        with open("out_html.txt", "w") as f:
            for line in all_data:
                f.write(line + "\n")

        return super().close(spider, reason)
