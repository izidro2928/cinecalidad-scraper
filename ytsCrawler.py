from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
from pymongo import MongoClient
from fake_useragent import UserAgent

options = Options()
ua = UserAgent()
userAgent = ua.random
print(userAgent)
options.add_argument(f'user-agent={userAgent}')

client = MongoClient('localhost')
db = client['yts_db']
col = db['yts_peliculas']

def extraer_cinecalidad():
    navegador = webdriver.Chrome(options=options)
    navegador.get("https://yts.mx/browse-movies?page=25")

    while True:
        links_pagina = navegador.find_elements_by_xpath('//a[@class="browse-movie-link"]')
        links_peliculas = []
        for link_pelicula in links_pagina:
            links_peliculas.append(link_pelicula.get_attribute('href'))
        for link in links_peliculas:
            try:
                navegador.get(link)
                # Extraemos los dsatos de TMDB
                caratula = navegador.find_element_by_xpath("//img[@class='img-responsive']").get_attribute('src')
                print(caratula)
                titulo = navegador.find_element_by_xpath("//div[@class='hidden-xs']/h1").text
                print(titulo)
                estreno = navegador.find_element_by_xpath("//div[@class='hidden-xs']/h2").text
                print(estreno)
                # Seleccionamos los caracteres a eliminar
                bad_chars = [';', ':', '!', "*", '/']
                # Cadena de texto con caracteres malos
                genero = navegador.find_element_by_xpath("//div[@class='hidden-xs']/h2[2]").text
                if genero:
                    # Recorremos los caracteres malos
                    for i in bad_chars:
                        genero = genero.replace(i, '') # Remplazamos los caracteres malos
                    # Convertimos la cadena de texto a una lista
                    generos = genero.split()
                    # Obtenemos el primer indece de la lista
                    xgenero = generos[0]
                    print(xgenero)
                else:
                    genero = []
                    print(xgenero)
                imdb = navegador.find_element_by_xpath("//span[@itemprop='ratingValue']").text
                print(imdb)
                trailer = navegador.find_element_by_xpath("//a[@id='playTrailer']").get_attribute('href')
                print(trailer)
                sinopsis = navegador.find_element_by_xpath("//div[@id='synopsis']/p[2]").text
                print(sinopsis)
                director = navegador.find_element_by_xpath("//span[@itemprop='director']/span").text
                print(director)
                rated = navegador.find_element_by_xpath("//body/div[@class='main-content']/div[@id='movie-content']/div[@id='movie-tech-specs']/div[1]/div[1]/div[4]").text
                print(rated)
                duracion = navegador.find_element_by_xpath("//body/div[@class='main-content']/div[@id='movie-content']/div[@id='movie-tech-specs']/div[1]/div[2]/div[3]").text
                print(duracion)
                magnet1 = navegador.find_element_by_xpath("//a[@class='magnet-download download-torrent magnet'][1]").get_attribute('href')
                print(magnet1)
                
                #Guardamos los datos en MongoDB
                col.update_one({
                    'titulo': titulo
                }, {
                    "$set":{
                        'caratula': caratula,
                        'titulo': titulo,
                        'estreno': estreno,
                        'genero': xgenero,
                        'imdb': imdb,
                        'trailer': trailer,
                        'sinopsis': sinopsis,
                        'director': director,
                        'rated': rated,
                        'duracion': duracion,
                        'magnet1': magnet1,
                    }
                }, upsert=True)
                navegador.back()
                time.sleep(1)
            except Exception as e:
                print(e)
                print("Hubo un error no se pudo obtener los datos!!!")
                navegador.back()
        try:
            pagina_siguiente = navegador.find_element_by_xpath("//*[contains(text(), 'Next »')]")
            pagina_siguiente.click()
            print(f"####################{pagina_siguiente}######################")
        except:
            break
extraer_cinecalidad()
