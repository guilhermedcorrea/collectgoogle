Preencha a planilha conforme o modelo em excelfiles/eans e excelfiles/urls
Execute o arquivo url_collector.py antes verifique se o caminho da planilha com os eans e o chromedriver.exe estao corretos
ao final o codigo ira coletar as urls referentes aos eans e ira fazer um insert nas tabelas UrlsBase


Depois execute o arquivo collect_precos.py siga os mesmos passos acima, verifique o caminho do excel e do chromedriver.exe ao final ele ira criar um arquivo com os nomes dos concorrentes, urls dos anuncios, urls google e os preços e fara um insert na tabela MonitoramentoPrecos


Pode ser necessario fazer algum ajuste, pois o google sempre altera algo no layout do html de suas paginas.

Tome cuidado com a velocidade com que as pesquisas de coleta de urls são realizadas, pois se exagerar o google começara a forçar captchas


