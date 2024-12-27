import scrapy
import csv

class BioooSpider(scrapy.Spider):
    name = 'biooospider'

    start_urls = [
        'https://encyklopedie.biooo.cz/vyhledat-slozeni/ciste-prirodni-latky/',
        'https://encyklopedie.biooo.cz/vyhledat-slozeni/derivaty-prirodnich-latek/',
        'https://encyklopedie.biooo.cz/vyhledat-slozeni/chemicke-latky-bez-negativnich-ucinku-na-zdravi/',
        'https://encyklopedie.biooo.cz/vyhledat-slozeni/chemicke-latky-potencialne-zdravi-skodlive/',
        'https://encyklopedie.biooo.cz/vyhledat-slozeni/nebezpecne-latky/',
        'https://encyklopedie.biooo.cz/vyhledat-slozeni/nezaraditelne-latky/',
    ]

    def parse(self, response):
        links = response.css(
            'a[href^="https://encyklopedie.biooo.cz/vyhledat-slozeni/"][title]:not([title="Vyhledat složení"]):not([title="Vyhledat kosmetickou složku"])')

        for link in links:
            href = link.attrib['href']
            title = link.attrib['title']
            text = link.css('::text').get()

            yield scrapy.Request(
                url=href,
                callback=self.parse_detail,
                meta={
                    'link_title': title,
                    'link_text': text
                }
            )

    def parse_detail(self, response):
        page_title = response.css('h1::text').get()

        other_names = response.css("strong::text").get()

        if other_names:
            other_names = other_names.strip()
            if not other_names:
                other_names = None

        description = response.css('p::text').getall()

        full_description = ' '.join([text.strip().replace('\u00A0', ' ') for text in description if text.strip()])

        res_data = {
            'page_url': response.url,
            'page_title': page_title,
            'other_names': other_names,
            'description': full_description
        }

        with open('biooo_output.csv', 'a', encoding='utf-8', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(
                [res_data['page_url'], res_data['page_title'], res_data['other_names'], res_data['description']])

        yield res_data