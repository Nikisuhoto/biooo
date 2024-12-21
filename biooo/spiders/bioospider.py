import scrapy


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

        description = response.css('p::text').getall()

        full_description = ' '.join([text.strip() for text in description if text.strip()])

        # Резултата
        yield {
            'page_url': response.url,
            'page_title': page_title,
            'description': full_description,
            # 'details': details,
            # 'subsections': subsections,
            # 'link_title': link_title,
            # 'link_text': link_text
        }
