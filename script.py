from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import schedule
import random
import time
from datetime import datetime, timedelta


def iniciar_sesion():
    # Inicializar el navegador Firefox
    driver = webdriver.Firefox()

    # Abrir la página web
    driver.get('https://admin.shopify.com/login')
    input("Inicia sesión y presiona ENTER para automatizar el proceso")
    addOrder_url = driver.current_url + '/draft_orders/new'
    
    print("Inicio de sesión correcto")
    return driver, addOrder_url

def automatizar_proceso(driver, addOrder_url):
    try:        
        ("Se procede a crear una orden")
        driver.get(addOrder_url)

        # Esperar a que el botón con aria label "Browse products" esté presente y hacer clic en él
        browse_button = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//button[@aria-label="Browse products"]'))
        )
        browse_button.click()

        # Esperar a que el div con el texto "All products" esté presente y hacer clic en él
        all_products_div = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//div[text()="All products"]'))
        )
        all_products_div.click()

        time.sleep(1)
        
        # Buscar y hacer clic en el div con aria-label "Select: Producto Ganador 1"
        div_select = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//div[@aria-label="Select: Producto Ganador 1"]'))
        )
        div_select.click()

        # Encontrar todos los botones
        buttons = driver.find_elements(By.TAG_NAME, 'button')
        # Seleccionar add_button que se corresponde con la posición 21
        add_button = buttons[21]
        add_button.click()
        
        time.sleep(1)
        
        # Hacer clic en el elemento <span> con el texto "Collect payment"
        collect_payment_span = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//span[contains(text(), "Collect payment")]'))
        )
        collect_payment_span.click()

        time.sleep(1)
        
        # Hacer clic en el elemento <span> con el texto "Mark as paid"
        mark_as_paid_span = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//span[contains(text(), "Mark as paid")]'))
        )
        mark_as_paid_span.click()
        
        time.sleep(2)
        
        # Hacer clic en el elemento <span> con el texto "Create order"
        create_order_span = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//span[contains(text(), "Create order")]'))
        )
        create_order_span.click()
        print("Orden creada correctamente")
        
    except Exception as e:
        print(f"Ocurrió un error: {e}")

def ejecutar_automatizacion(driver, addOrder_url):
    current_hour = datetime.now().hour
    print(f"Inicio de la tarea a las {current_hour}")
    random_execution = random.randint(1, 4) 

    if 1 <= current_hour <= 9:  # Comprobar si está entre las 1-9 de la mañana en hora española
        if random.random() <= 0.05:  # 5% de probabilidad entre las 1-9 de la mañana
            random_execution = 1
        else:
            random_execution = 0

    print(f"Número de ejecuciones en esta hora: {random_execution}")

    for _ in range(random_execution):
        automatizar_proceso(driver, addOrder_url)
        time.sleep(random.randint(600,850))

# Programar ejecución cada hora
driver, addOrder_url = iniciar_sesion()
schedule.every().minute.do(ejecutar_automatizacion, driver, addOrder_url)

# Ejecutar el loop para mantener el programa corriendo
while True:
    schedule.run_pending()
    time.sleep(1)
