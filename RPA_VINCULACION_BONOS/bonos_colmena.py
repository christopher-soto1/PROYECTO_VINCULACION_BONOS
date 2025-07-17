from openpyxl import load_workbook
from openpyxl import Workbook


import unittest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import TimeoutException
import os
import shutil
import time
import requests
from datetime import datetime, timedelta
import json
import logging
import re
import pandas as pd
import numpy as np
import csv
#import PyPDF2
import sys
import io

#FORMATEO DE XLS -> XLSX
import xlrd
import openpyxl
from datetime import datetime

import requests
import traceback

# VARIABLES GLOBALES
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
timeout_sesion = 30
# VARIABLES GLOBALES





#----------------------------------------------------# CREDENCIALES #----------------------------------------------------#
def obtener_credencialesDeAcceso(usuario):
    try:
        # Obtener la ruta del directorio actual (donde se encuentra el script Python)
        directorio_actual = os.path.dirname(os.path.abspath(__file__))
        # Ruta al archivo JSON
        ruta_archivo = os.path.join(directorio_actual, 'usuarios.json')
        print(ruta_archivo)

        with open(ruta_archivo, 'r', encoding='utf-8') as archivo:
            datos = json.load(archivo)

            # Imprimir los datos leídos (opcional, puedes eliminarlo si no necesitas ver los datos)
            # print(datos)

            # Obtener la lista de usuarios
            usuario_credenciales = datos.get(usuario, [])

            if usuario_credenciales:
                # Extraer los valores de cada objeto dentro de la lista
                credenciales = []  # Lista para almacenar las credenciales
                for usuario in usuario_credenciales:
                    usuario_isapre = usuario['usuario']
                    contrasena = usuario['pass']
                    url = usuario['url']
                    # Guardar las credenciales en el formato que desees (como un diccionario)
                    credenciales.append({
                        'usuario': usuario_isapre,
                        'contrasena': contrasena,
                        'url': url,
                        'directorio_actual': directorio_actual
                    })
                return credenciales
            else:
                print(f"No se encontraron datos para '{usuario}'.")
                return None  # Si no se encontraron usuarios, devolver None
            
    except FileNotFoundError:
        print(f"El archivo {ruta_archivo} no fue encontrado obtener_credencialesDeAcceso.")
        return None
    except json.JSONDecodeError:
        print(f"El archivo {ruta_archivo} no es un archivo JSON válido obtener_credencialesDeAcceso.")
        return None
    except Exception as e:
        #log_exception(f"Error obtener_credencialesDeAcceso: {e}")  # Registrar la excepción en el archivo de log
        print(f"Ocurrió un error: {e}")
        return None
#----------------------------------------------------# CREDENCIALES #----------------------------------------------------#


def colmena(timeout_sesion):
    driver = None
    tiempo_espera = timeout_sesion
    usuario = "usuarioColmena"
    try:
        credenciales = obtener_credencialesDeAcceso(usuario)
        if credenciales:
            usuarioColmena = credenciales[0]['usuario']
            contrasenaColmena = credenciales[0]['contrasena']
            url = credenciales[0]['url']
            directorio_actual = credenciales[0]['directorio_actual']

            # Crear subcarpeta Colmena
            fecha_hoy = datetime.now().strftime("%d-%m-%Y")
            base_dir = directorio_actual
            carpeta_fecha = os.path.join(base_dir, 'respaldos\\'+fecha_hoy)
            carpeta_Colmena = os.path.join(carpeta_fecha, "Colmena")
            os.makedirs(carpeta_Colmena, exist_ok=True)
            print(f"Ruta creada: {carpeta_Colmena}")

            # Configura las preferencias de descarga de Chrome
            chrome_prefs = {
                "download.default_directory": carpeta_Colmena,   # Directorio donde se guardarán los archivos descargados
                "download.prompt_for_download": False,        # Evita la ventana emergente de confirmación
                "download.directory_upgrade": True,           # Permite que se cambie el directorio
                "safebrowsing.enabled": True                  # Habilita la navegación segura (puede ayudar a evitar la descarga de archivos peligrosos)
            }

            # Configura el navegador (en este caso, Chrome) NEW
            options = webdriver.ChromeOptions()
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            options.add_experimental_option("prefs", chrome_prefs)  # Aplica las preferencias de descarga
            # options.add_argument("--headless")  # Si deseas que el navegador se ejecute en modo sin cabeza (sin GUI)
            options.add_argument("--disable-extensions")  # Desactiva las extensiones para mejorar la velocidad y evitar interferencias
            options.add_argument("--disable-software-rasterizer")  # Desactiva el uso de software para la aceleración gráfica (mejora el rendimiento)

            #php
            options.add_argument("--window-size=1920,1080")
            options.add_argument("--disable-gpu")

            #TEST TIMER
            #options.set_capability("pageLoadStrategy", "normal")  # Puede usar 'eager' si es más rápido
            

            # Inicia el navegador con las opciones especificadas
            driver = webdriver.Chrome(options=options)
            driver.maximize_window()

            try:
                driver.set_page_load_timeout(tiempo_espera)
                driver.get(url)
                print("Página cargada exitosamente.")
                time.sleep(5)

            except TimeoutException as te:
                print(f"Ocurrió un error: Timeout al intentar cargar {url}, se esperaron {tiempo_espera}")
                driver.quit()
                raise te
            except Exception as e:
                print(f"Ocurrió un error inesperado: {e}, se esperaron {tiempo_espera}")
                driver.quit()
                raise e
            
            # Esperar a que esté visible el campo de usuario
            input_usuario = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "CustLoginID"))
            )
            input_usuario.clear()
            input_usuario.send_keys(usuarioColmena)
            print("Usuario Colmena ingresado correctamente.")
            time.sleep(2)

            # Esperar a que esté visible el campo de contraseña
            input_password = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "SignonPasswd"))
            )
            input_password.clear()
            input_password.send_keys(contrasenaColmena)
            print("Contraseña Colmena ingresada correctamente.")
            time.sleep(2)
            

            # Esperar a que el botón de ingresar esté presente y sea clickeable
            boton_ingresar = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.NAME, "Submit"))
            )
            boton_ingresar.click()
            print("Botón 'Ingresar' presionado correctamente.")
            time.sleep(7)

            # Esperar que el frame esté disponible y cambiar a él
            WebDriverWait(driver, 10).until(
                EC.frame_to_be_available_and_switch_to_it((By.NAME, "menuFrame"))
            )

            # Esperar que el enlace 'Emitir Bono' esté presente y clickeable
            boton_emitir_bono = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//a[contains(text(), "Emitir Bono")]'))
            )

            # Hacer clic en el enlace
            boton_emitir_bono.click()
            print("Botón 'Emitir Bono' clickeado correctamente.")
            time.sleep(2)

            # Volver al contexto principal si necesitas interactuar con otros frames
            driver.switch_to.default_content()


        else:
            #log_exception(f"No se encontraron credenciales para {usuario}")
            print("No se encontraron credenciales.")

    except Exception as e:
        #log_exception(f"Error banco_chile: {e}")  # Registrar la excepción en el archivo de log
        print(f"Ocurrió un error: {e}")
    finally:
        if driver is not None:
            driver.quit()


colmena(40)


# -----------------------------------------------------------------------------
# INICIO PROCESO
# -----------------------------------------------------------------------------