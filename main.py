from gettext import find
from lib2to3.pgen2.driver import Driver
from typing import final
from selenium import webdriver # con esto importo desde selenium el webdriver para poder usar la ruta PATH y habilitar opciones
from selenium.webdriver.common.keys import Keys # Para poder usar teclas "virtuales" dentro del codigo
from selenium.webdriver.common.by import By #  by elementos
from selenium.webdriver.support.ui import WebDriverWait # esperar que exista un elemento para buscarlo
from selenium.webdriver.support import expected_conditions as EC # lo mismo de arriba
from selenium.webdriver.chrome.options import Options 
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities # capabilities
import time

# PATH = ".\webdriver\chromedriver.exe" # Ruta de ejecucion 

# Service no se que hace exactamente. Reemplaza el PATH pero me quito un error por consola que la hace ver mas limpia. 
s = Service('.\webdriver\chromedriver.exe')

# Opciones para que no hayan errores dentro del navegador y evitar errores ssl.
options = webdriver.ChromeOptions()
options.add_argument('--allow-running-insecure-content')
options.add_argument('--ignore-certificate-errors')
options.add_argument('--ignore-ssl-errors')
options.add_argument('--disable-gpu')
options.add_experimental_option('excludeSwitches', ['enable-logging'])    # directorio de descargas agregar un doble \\ al final. No se pero me soluciono un error por consola. ej: C:\Users\Rivalyr\Downloads\\
options.add_experimental_option("prefs", {"download.default_directory":  r"C:\Users\Rivalyr\Downloads\\", "download.prompt_for_download": False,
  "download.directory_upgrade": True,
  "safebrowsing.enabled": True})

# input para buscar la cancion deseada
busqueda = input(str("Introduce el nombre de la cancion: ")) 

# Abre el navegador con las opciones puestas anteriormente.
drive = webdriver.Chrome(service=s, options=options) # executable_path=r'.\webdriver\chromedriver.exe'

# Convertidor objetivo.
drive.get ("https://getn.topsandtees.space/ZmzDgxd4wK") 

# Busca la barra de busqueda
search = drive.find_element(by=By.NAME, value="q")

# La encuentra e introduce el nombre de la cancion que se ha pedido al inicio.
search.send_keys(busqueda)
search.send_keys(Keys.RETURN) # Ejecuta un buscar

# Espera que el elemento por el TEXTO sea encontrado dentro de la pagina *para evitar fallos*
try: 
    descarga = WebDriverWait(drive, 10).until(
        EC.presence_of_element_located((By.LINK_TEXT, "Download"))
    )
    descarga.click() #Le dara click al primer boton de descargas (resultado con mas visitas o mas conocido que arroje la API de youtube)
except: 
    print ("\nAlgo ha fallado. Reinicia el script!\n")

# Espera que se cargue el archivo dentro de la pagina para proceder a su descarga
try:

    descargaencontrada = WebDriverWait(drive, 50).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, ".search-item__download"))
    )
    descargaencontrada.click()
    
    print("\nSe ha encontrado la cancion!:D")

    # Codigo de StackOverFlow para cerrar ventanas emergentes.
    # New tabs will be the last object in window_handles
    drive.switch_to.window(drive.window_handles[-1])
    # close the tab
    drive.close()
    # switch to the main window
    drive.switch_to.window(drive.window_handles[0])

    # Conseguir el nombre de la cancion  e imprimirlo como resultado
    nombre = drive.find_element(by=By.TAG_NAME, value="h1")
    print (f"\nHas descargado: {nombre.text}\n")
    time.sleep(30)
    print ("Cerrando navegador...")
    drive.quit()
except:
    time.sleep(10)
    print ("\nNo se ha podido descargar\n")
    drive.quit()
    raise