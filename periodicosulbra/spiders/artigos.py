import scrapy
import pandas as pd


class ArtigoItem(scrapy.Item):
    title = scrapy.Field()
    authors = scrapy.Field()
    summary = scrapy.Field()
    tags = scrapy.Field()
    complete_version = scrapy.Field()


class ArtigosSpider(scrapy.Spider):
    name = 'artigos'
    start_urls = ['http://www.periodicos.ulbra.br/index.php/acta/issue/archive?issuesPage=1#issues']

    def parse(self, response):
        # Nesta etapa o programa irá entrar em cada um dos artigos e irá repassar para a próxima função
        for link in response.xpath(".//div[@style='float: left; width: 100%;']"):
            yield response.follow(link.css('a::attr(href)').get(), callback=self.parse_volume_artigos)

        # Verificando a existência da próxima página
        next_page = response.css('a.next::attr(href)').get()
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)

    # Nesta etapa o programa entra em cada site de artigos e chama a função parse_artigos
    def parse_volume_artigos(self, response):
        for link in response.css('div.tocTitle a::attr(href)'):
            yield response.follow(link.get(), callback=self.parse_artigos)

    # Nesta etapa o programa entra em cada site de edição e chama a função parse_volume_artigos para cada artigo
    def parse_edicoes(self, response):
        for link in response.css('div.tocTitle a::attr(href)'):
            yield response.follow(link.get(), callback=self.parse_volume_artigos)

    # Aqui pegaremos titulo, autores, resumo, tags e o link de sua versão completa e adicionaremos em um item
    def parse_artigos(self, response):
        artigo_item = ArtigoItem()

        i = response.xpath(".//div[@id='content']")
        artigo_item['title'] = i.xpath(".//div[@id='articleTitle']//text()").get()
        artigo_item['authors'] = i.xpath(".//div[@id='authorString']//text()").get()
        artigo_item['summary'] = i.xpath(".//div[@id='articleAbstract']/div//text()").getall()
        artigo_item['tags'] = i.xpath(".//div[@id='articleSubject']/div//text()").get()
        artigo_item['complete_version'] = i.xpath(".//div[@id='articleFullText']/a")\
            .css('a::attr(href)').get()

        yield artigo_item

    def closed(self, reason):
        # Salvando no dataframe do pandas.
        df = pd.DataFrame([dict(item) for item in self.crawler.stats.get_stats('item_scraped_count')])

        # Salvando no excel, usando pandas.
        df.to_excel('artigos.xlsx', index=False)
