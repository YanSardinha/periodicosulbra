
import scrapy
import pandas as pd


title_list = []
authors_list = []
summary_list = []
tags_list = []
complete_version_list = []


class ArtigosSpider(scrapy.Spider):
    name = 'artigos'
    start_urls = ['http://www.periodicos.ulbra.br/index.php/acta/issue/archive?issuesPage=1#issues']
    
    def parse(self, response):
        #Nesta etapa o programa irá entrará em cada um dos artigos e irá repassar para a próxima função
        for link in response.xpath(".//div[@style='float: left; width: 100%;']").css('a::attr(href)'):
            yield response.follow(link.get(), callback=self.parse_volume_artigos)
            
        #Nessa etapa o programa pegar os site onde estarãos as edições
        for i in range(2, 6):
            proxima_pagina = 'http://www.periodicos.ulbra.br/index.php/acta/issue/archive?issuesPage={}'.format(i)
            if proxima_pagina: 
                yield response.follow(proxima_pagina, callback=self.parse)            
        
    #Nessa etapa o programa entra em cada site de artigos e chama a função parse_artigos(fiquei sem 
    # criatividade pro nome da função)
    def parse_volume_artigos(self, response):
        for link in response.css('div.tocTitle a::attr(href)'):
            yield response.follow(link.get(), callback=self.parse_artigos)

    # Aqui pegaremos titulo, autores, resumo, tags e o link de sua versão complete e colocarem nas 
    # listas já criadas anteriormente.  
    def parse_artigos(self, response):
        for i in response.xpath(".//div[@id='content']"):   
            title = i.xpath(".//div[@id='articleTitle']//text()").get(),
            authors = i.xpath(".//div[@id='authorString']//text()").get(),
            summary = i.xpath(".//div[@id='articleAbstract']/div//text()").getall(),
            tags = i.xpath(".//div[@id='articleSubject']/div//text()").get(),
            complete_version = i.xpath(".//div[@id='articleFullText']/a").css('a::attr(href)').get()

            title_list.append(title)
            authors_list.append(authors)
            summary_list.append(summary)
            tags_list.append(tags)
            complete_version_list.append(complete_version)

        #Salvando no dataframe do pandas.
        df = pd.DataFrame({
            'Titles': title_list,
            'Authors': authors_list,
            'Summary': summary_list,
            'Tags': tags_list,
            'Complete Version': complete_version_list
        })

        #Salvando no excel, usando pandas.
        df.to_excel('artigos.xlsx', index=False)