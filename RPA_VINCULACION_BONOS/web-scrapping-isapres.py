
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




def setup_logger():
    # Obtener la fecha actual para crear un directorio específico
    fecha_actual = datetime.now().strftime('%Y-%m-%d')
    # Directorio donde se guardarán los logs, con carpeta por fecha
    log_dir = os.path.join('logs', fecha_actual)

    # Crear el directorio si no existe
    os.makedirs(log_dir, exist_ok=True)

    # Nombre del archivo de log
    log_file = os.path.join(log_dir, 'errores.log')

    # Configurar el logger
    logging.basicConfig(
        filename=log_file,
        level=logging.ERROR,
        format='%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )



def log_exception(e):
    #Configurar el logger antes de ejecutar el resto del código
    setup_logger()
    logging.error(f"Ocurrió un error: {e}")




# Función para registrar el inicio del proceso
def log_inicio(param_isapre):
  
    carpeta_isapre = os.path.join(os.path.dirname(__file__), param_isapre)  # Ruta del archivo de log
    nombre_archivo = os.path.join(os.path.dirname(__file__), param_isapre+'\\LogProceso.log')  # Ruta del archivo de log
    fecha_inicio = datetime.now()  # Obtener fecha y hora actuales

     # Crear la carpeta si no existe
    if not os.path.exists(carpeta_isapre):
        try:
            os.makedirs(carpeta_isapre)
        except Exception as e:
            error_trace = traceback.format_exc()
            log_exception(
                f"\n❌ Ocurrió un error al crear la carpeta '{param_isapre}': {e}\n{error_trace}"
            )
    

    # Verificar si el archivo de log existe, si no, crearlo
    if not os.path.exists(nombre_archivo):
        with open(nombre_archivo, 'w'):  # Crea el archivo vacío si no existe
            pass

    # Escribir el inicio del log
     # Escribir el inicio del log con el tipo de banco y previsión
    texto_inicio = f"******************LOG PROCESO ROBOT**************************\nFecha Inicio: {fecha_inicio.strftime('%Y-%m-%d %H:%M:%S')}\n"
    texto_inicio += f"Nombre Isapre: {param_isapre}\n"
    texto_inicio += f"Proceso: Descarga de bonos\n"

    # a : PARA ESCRIBIR EN EL CONTENIDO 
    # W: PARA RESCRIBIR EL CONTENIDO
    try:
       with open(nombre_archivo, 'w', encoding='utf-8') as file:  # Abrir el archivo en modo append con codificación UTF-8
            file.write(texto_inicio)
    except Exception as e:
        print(f"Error al escribir en el archivo de log: {e}")



# Función para registrar el final del proceso
def log_final(param_isapre):
    nombre_archivo = os.path.join(os.path.dirname(__file__), param_isapre+'\\LogProceso.log') 
    fecha_fin = datetime.now()  # Obtener fecha y hora actuales

    # Escribir el final del log
    texto_final = f"Fecha Fin: {fecha_fin.strftime('%Y-%m-%d %H:%M:%S')}\n*************************************************************\n"
    try:
        with open(nombre_archivo, 'a', encoding='utf-8') as file:
            file.write(texto_final)
    except Exception as e:
        print(f"Error al escribir en el archivo de log: {e}")



# Función para registrar mensajes generales en el log
def registro_log(texto,param_isapre):
    # log_file = os.path.join(os.path.dirname(__file__), 'LogProceso.log')  # Ruta del archivo de log
    log_file = os.path.join(os.path.dirname(__file__), param_isapre+'\\LogProceso.log')  # Ruta del archivo de log

    # Verificar si el archivo de log existe, si no, crearlo
    if not os.path.exists(log_file):
        with open(log_file, 'w'):  # Crea el archivo vacío si no existe
            pass

    # Agregar la marca de tiempo
    texto_con_timestamp = f"{datetime.now().strftime('%Y-%m-%d')} {texto}"

    try:
     with open(log_file, 'a', encoding='utf-8') as file:
        file.write(texto_con_timestamp + '\n')
    except Exception as e:
        print(f"Error al escribir en el archivo de log: {e}")



#----------------------------------------------------# CREDENCIALES #----------------------------------------------------#
def obtener_credencialesDeAcceso(usuario):
    try:
        # Obtener la ruta del directorio actual (donde se encuentra el script Python)
        directorio_actual = os.path.dirname(os.path.abspath(__file__))
        # Ruta al archivo JSON
        ruta_archivo = os.path.join(directorio_actual, 'usuarios.json')
        # print(ruta_archivo)

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

#----------------------------------------------------# BANMEDICA Y VIDA3 #----------------------------------------------------# #UNIFICACION
def descargar_bonos_salud(institucion, timeout_sesion):
    driver = None
    tiempo_espera = timeout_sesion

    usuario_key = "usuarioBanmedica" if institucion.lower() == "banmedica" else "usuarioVida3"
    id_boton_buscar = "ctl00_ctl00_ContentPlaceHolderHome_ContentPlaceHolderBonosPAM_ImageButtonBuscar" if institucion.lower() == "banmedica" else "ctl00_ctl00_ContentPlaceHolderHome_ContentPlaceHolderBonosPAM_ImageButtonBuscarV"
    id_boton_imprimir = "ImageButton2" if institucion.lower() == "banmedica" else "ctl00_ctl00_ContentPlaceHolderHome_ContentPlaceHolderBonosPAM_ImageButton3"

    try:
        credenciales = obtener_credencialesDeAcceso(usuario_key)
        if not credenciales:
            print("No se encontraron credenciales.")
            return

        usuario = credenciales[0]['usuario']
        contrasena = credenciales[0]['contrasena']
        url = credenciales[0]['url']
        directorio_actual = credenciales[0]['directorio_actual']

        fecha_hoy = datetime.now().strftime("%d-%m-%Y")
        base_dir = directorio_actual
        carpeta_fecha = os.path.join(base_dir, 'respaldos\\'+fecha_hoy)
        

        carpeta_destino_base = carpeta_fecha
        if institucion.lower() == "banmedica":
            carpeta_destino_base = os.path.join(carpeta_fecha, "Banmedica")
            os.makedirs(carpeta_destino_base, exist_ok=True)
            # print(f"📁 Carpeta Banmédica creada: {carpeta_destino_base}")

        options = webdriver.ChromeOptions()
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-extensions")
        options.add_argument("--window-size=1920,1080")
        options.add_argument("--disable-gpu")
        options.add_experimental_option("prefs", {})  # sin descargas hasta después

        driver = webdriver.Chrome(options=options)
        driver.maximize_window()
        driver.set_page_load_timeout(tiempo_espera)
        driver.get(url)
        time.sleep(3)


        # ---------- Ingreso de credenciales ---------- #UNIFICACION

        #Ingreso de rut #UNIFICACION
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "rut"))).send_keys(usuario)
        time.sleep(1.5)

        #Ingreso de contrasena #UNIFICACION
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "current-password"))).send_keys(contrasena)
        time.sleep(1.5)

        #Click boton ingresar #UNIFICACION
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(translate(text(),'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'),'ingresar')]"))).click()
        time.sleep(6)
        # ---------- Ingreso de credenciales ---------- #UNIFICACION

        #Identificar select y seleccionar institucion 93915000-5 #UNIFICACION
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "cboSeleccionHolding"))).click()
        Select(driver.find_element(By.ID, "cboSeleccionHolding")).select_by_value("93915000|93915000")
        time.sleep(4)

        #Seleccion de boton "Programas medicos" #UNIFICACION
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "btnSeleccionar"))).click()
        time.sleep(4)

        #Seleccion de boton "Emision de bonos PAM" #UNIFICACION
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "menu2"))).click()
        time.sleep(4)

        #Seleccion de boton "Por fecha" #UNIFICACION
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "ctl00_ctl00_ContentPlaceHolderHome_modMenu_wucMenuLateral_treMenut0"))).click()
        time.sleep(4)

        #Seleccion de boton "Por fecha" #UNIFICACION
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "ctl00_ctl00_ContentPlaceHolderHome_ContentPlaceHolderBonosPAM_RadioButtonList1_0"))).click()
        time.sleep(4)

        # Asignar rango de fechas para la búsqueda bonos
        #fecha_str = datetime.now().strftime("%d/%m/%Y") # fecha hoy 
        #fecha_ayer = datetime.now() - timedelta(days=1) # fecha ayer
        #fecha_str = fecha_ayer.strftime("%d/%m/%Y")
        fecha_str = '10/07/2025'
        driver.find_element(By.ID, "ctl00_ctl00_ContentPlaceHolderHome_ContentPlaceHolderBonosPAM_TextBoxFechaInicio").clear()
        driver.find_element(By.ID, "ctl00_ctl00_ContentPlaceHolderHome_ContentPlaceHolderBonosPAM_TextBoxFechaInicio").send_keys(fecha_str)
        driver.find_element(By.ID, "ctl00_ctl00_ContentPlaceHolderHome_ContentPlaceHolderBonosPAM_TextBoxFechaTermino").clear()
        driver.find_element(By.ID, "ctl00_ctl00_ContentPlaceHolderHome_ContentPlaceHolderBonosPAM_TextBoxFechaTermino").send_keys(fecha_str)

        #Buscar registros 
        WebDriverWait(driver, tiempo_espera).until(EC.element_to_be_clickable((By.ID, id_boton_buscar))).click()
        time.sleep(5)

        tabla = WebDriverWait(driver, tiempo_espera).until(EC.presence_of_element_located((By.ID, "ctl00_ctl00_ContentPlaceHolderHome_ContentPlaceHolderBonosPAM_GridViewBonosyReembolsosPAM")))
        texto_td = tabla.find_element(By.TAG_NAME, "td").text.strip()
        if "No se encuentran Bonos por emitir" in texto_td:
            # raise TimeoutException("No se encuentran Bonos por emitir.")
            mensaje_log = f"No se encuentran Bonos por emitir en isapre {institucion}"
            registro_log(mensaje_log,institucion) 
            return {"estado": False, "mensaje": mensaje_log}
            

        # Recolectar TODOS los pacientes
        filas = tabla.find_elements(By.XPATH, ".//tbody/tr[position()>1]")
        # Inicialmente vacío
        df_total_pacientes = pd.DataFrame()
        df_total_bonos = pd.DataFrame()
        pacientes = []
        for fila in filas:
            cols = fila.find_elements(By.TAG_NAME, "td")
            pacientes.append({
                "folio_pam": cols[0].text.strip(),
                #"num_cuenta": cols[1].text.strip(), #UNIFICACION
                "rut_afiliado": cols[2].text.strip(),
                #"rut_paciente": cols[3].text.strip(), #UNIFICACION
                #"nombre_paciente": cols[4].text.strip(), #UNIFICACION
                "monto_facturado": cols[5].text.strip(),
                "monto_bonificado": cols[6].text.strip()
            })

        for detalle_paciente in pacientes:
            try:
                folio_pam = detalle_paciente["folio_pam"]
                carpeta_folio = os.path.join(carpeta_destino_base, folio_pam)
                os.makedirs(carpeta_folio, exist_ok=True)

                driver.execute_cdp_cmd("Page.setDownloadBehavior", {
                    "behavior": "allow",
                    "downloadPath": carpeta_folio
                })

                url_detalle = f"https://prestadores.isaprebanmedica.cl/Pagos/DetBonosPam.aspx?folio={folio_pam}"
                driver.execute_script(f"window.open('{url_detalle}');")
                driver.switch_to.window(driver.window_handles[-1])
                time.sleep(3)

                tabla_detalle = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "GridViewBonosyReembolsosPAM")))
                filas_detalle = tabla_detalle.find_elements(By.XPATH, ".//tbody/tr[position()>1]")

                detalle_bono = []
                for fila_detalle in filas_detalle:
                    cols = fila_detalle.find_elements(By.TAG_NAME, "td")
                    detalle_bono.append({
                        "folio_colilla": cols[0].text.strip(),
                        "folio_interno": cols[1].text.strip(),
                        "fecha_recepcion": cols[2].text.strip(),
                        #"rut_beneficiario": cols[3].text.strip(), #UNIFICACION
                        #"nombre_beneficiario": cols[4].text.strip(), #UNIFICACION
                        "monto_prestacion": cols[5].text.strip(),
                        "monto_ayuda": cols[6].text.strip()
                    })

                df_detalle_bono = pd.DataFrame(detalle_bono)
                # Acumular sin reiniciar
                df_total_bonos = pd.concat([df_total_bonos, df_detalle_bono], ignore_index=True)
                # print(f"\n📋 DETALLE BONO folio {folio_pam}:")
                # print(df_detalle_bono)
               
                WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, id_boton_imprimir))).click()
                # print("📥 Botón de imprimir presionado.")
                time.sleep(10)

                driver.close()
                driver.switch_to.window(driver.window_handles[0])
                time.sleep(2)

                # Validar Estado PAM si es Banmédica
                if institucion.lower() == "banmedica":
                    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "ctl00_ctl00_ContentPlaceHolderHome_modMenu_wucMenuLateral_treMenut4"))).click()
                    time.sleep(2)
                    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "ctl00_ctl00_ContentPlaceHolderHome_modMenu_wucMenuLateral_treMenut6"))).click()
                    time.sleep(3)

                    WebDriverWait(driver, 10).until(EC.frame_to_be_available_and_switch_to_it((By.ID, "EstadoPAM")))
                    time.sleep(1)
                    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "btnLimpiarFiltros"))).click()
                    time.sleep(1.5)
                    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "folioPam"))).clear()
                    driver.find_element(By.ID, "folioPam").send_keys(folio_pam)
                    time.sleep(1)
                    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "btnBuscarSolicitud"))).click()
                    time.sleep(5)

                    tabla_estado = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "tablefolio")))
                    filas_resultado = tabla_estado.find_elements(By.XPATH, ".//tbody/tr[not(contains(@class, 'footable-detail-row'))]")
                    if filas_resultado:
                        primera_fila = filas_resultado[0]
                        primera_fila.click()
                        time.sleep(2)
                        fila_detalle = primera_fila.find_element(By.XPATH, "following-sibling::tr[contains(@class, 'footable-detail-row')]")
                        tabla_detalle = fila_detalle.find_element(By.XPATH, ".//table[contains(@class, 'footable-details')]")
                        filas_info = tabla_detalle.find_elements(By.TAG_NAME, "tr")
                        for fila_info in filas_info:
                            columnas = fila_info.find_elements(By.TAG_NAME, "td")
                            if "Fecha Ingreso" in fila_info.text and columnas:
                                detalle_paciente["fecha_ingreso_estado_pam"] = columnas[0].text.strip()
                                break

                    driver.switch_to.default_content()

                df_paciente = pd.DataFrame([detalle_paciente])
                df_total_pacientes = pd.concat([df_total_pacientes, df_paciente], ignore_index=True)
                # print("\n🧾 PACIENTE ORIGINAL:")
                # print(df_paciente)

               

            except Exception as e:
                # print(f"⚠️ Error procesando folio {detalle_paciente.get('folio_pam', 'desconocido')}: {e}")
                folio = detalle_paciente.get('folio_pam', 'desconocido')
                error_trace = traceback.format_exc()
                log_exception(f"\n❌ Ocurrió un error procesando folio {folio}: {e}\n{error_trace}")
                if len(driver.window_handles) > 1:
                    driver.close()
                    driver.switch_to.window(driver.window_handles[0])

        mensaje_log = f"Detalles pacientes:\n{df_total_pacientes}"
        registro_log(mensaje_log,institucion)
        mensaje_log = f"Detalles bonos:\n{df_total_bonos}"
        registro_log(mensaje_log,institucion)
        return {"estado": True, "data_paciente": df_total_pacientes, "data_bonos":df_total_bonos}
    except Exception as e:
        # print(f"❌ Ocurrió un error: {e}") #log
        error_trace = traceback.format_exc()
        log_exception(f"\n❌ Ocurrió un error Isapre: : {e}\n{error_trace}") 
        return {"estado": False, "error": str(e)}
       
    finally:
        if driver is not None:
            driver.quit()
       
#----------------------------------------------------# BANMEDICA Y VIDA3 #----------------------------------------------------# #UNIFICACION




#----------------------------------------------------# MAIN #----------------------------------------------------#
def ejecutar_con_reintentos_bonos(max_reintentos, param_isapre):
    # base_dir = r"C:\xampp\htdocs\robot-bonos\proyectopy\respaldos"
    base_dir = os.path.dirname(os.path.abspath(__file__))
    intento = 1

    while intento <= max_reintentos:
        try:
            # print(f"\n🌀 Intento {intento} de {max_reintentos}")

            # Eliminar carpeta diaria si existe
            fecha_hoy = datetime.now().strftime("%d-%m-%Y")
            carpeta_diaria = os.path.join(base_dir, 'respaldos\\'+fecha_hoy)

            if os.path.exists(carpeta_diaria):
                try:
                    shutil.rmtree(carpeta_diaria)
                    # print(f"🗑️ Carpeta eliminada correctamente: {carpeta_diaria}")
                except Exception as e:
                    # print(f"⚠️ Error al eliminar carpeta {carpeta_diaria}: {e}")
                    raise e

            # Crear carpeta diaria nuevamente
            try:
                os.makedirs(carpeta_diaria)
                # print(f"📁 Carpeta creada: {carpeta_diaria}")
            except Exception as e:
                # print(f"⚠️ Error al crear carpeta {carpeta_diaria}: {e}")
                raise e
                

            # Ejecutar flujo Banmedica
            respuesta = descargar_bonos_salud(param_isapre, timeout_sesion=40)
            estado = respuesta["estado"]
            if (estado !=False):
                # print(respuesta)
                df_data_paciente = respuesta["data_paciente"]
                df_data_bonos = respuesta["data_bonos"]
                
                arreglo_paciente = df_data_paciente.to_dict(orient='records')
                arreglo_bonos = df_data_bonos.to_dict(orient='records')               
                # Retornar el diccionario con ambos arreglos
                print({"arreglo_paciente": arreglo_paciente, "arreglo_bonos": arreglo_bonos})
                log_final(param_isapre)
                return
            
            else:
                print({"error": f"Al descargar los bonos de la isapre: {param_isapre}"})
                log_final(param_isapre)
                return

        except Exception as e:
            error_trace = traceback.format_exc()
            mensaje_error = f"\n❌ Error en intento {intento}: {e}\n{error_trace}"
            log_exception(mensaje_error)
            respuesta2 = {"error": mensaje_error}
            print({"error": respuesta2["error"]})
            intento += 1
            time.sleep(5)


#----------------------------------------------------# MAIN #----------------------------------------------------#


#param_isapre = sys.argv[1]
param_isapre = "Banmedica"
log_inicio(param_isapre)
ejecutar_con_reintentos_bonos(1, param_isapre)



# def saludar(nombre, apellido):
#     print(f"¡Hola {nombre} {apellido}! Esto es una prueba de saludo.")

# def despedir(nombre, apellido):
#     print(f"¡Adiós {nombre} {apellido}! Esto fue todo.")


# def main():
#     if len(sys.argv) < 2:
#         print("Parámetros insuficientes")
#         sys.exit(1)

#     funcion = sys.argv[1]
#     nombre = sys.argv[2]
#     apellido = sys.argv[3]

#     if funcion == "saludar":
#         saludar(nombre, apellido)

#     elif funcion == "despedir":
#         despedir(nombre, apellido)

#     elif funcion == "ejecutar_con_reintentos_bonos":
#         ejecutar_con_reintentos_bonos(4)
#     else:
#         print(f"Función '{funcion}' no reconocida.")

# if __name__ == "__main__":
#     main()














#banmedica(usuario, timeout_sesion)
#vida3(usuario, timeout_sesion)
#colmena(timeout_sesion)

# ------------- PARA VALIDAR RETURN DE CREDENCIALES -------------

#credenciales = obtener_credencialesDeAcceso(usuario)
#
#if credenciales:
#    print("Credenciales encontradas:")
#    for c in credenciales:
#        print(f"Usuario: {c['usuario']}")
#        print(f"Contraseña: {c['contrasena']}")
#        print(f"URL: {c['url']}")
#        print(f"Directorio actual: {c['directorio_actual']}")
#        print("-" * 40)
#else:
#    print("No se encontraron credenciales.")

# ------------- PARA VALIDAR RETURN DE CREDENCIALES -------------
















