from routes.corrections_routes import *
#from routes.objects_routes import *
#from routes.users_routes import *
import pytest
import requests

HOST = "http://localhost:8000"


"""#Corrections
def test_get_corrections_success():
    url = f"{HOST}/corrections/"
    response = requests.get(url)
    assert response.status_code == 200, "Test 1: Obtención de historial de correcciones exitosa falló." 

def test_get_corrections_empty_database():
    url = f"{HOST}/corrections/"
    response = requests.get(url)
    assert response.status_code == 404, "Test 2: Obtención de historial de correcciones con base de datos vacía falló."

"""

"""
#USER CORRECTIONS

def test_get_corrections_user_valid():
    user = "asanchez2017"  
    url = f"{HOST}/corrections/{user}"
    response = requests.get(url)
    assert response.status_code == 200, "Test 1: Obtención de historial de correcciones de usuario válido falló."

def test_get_corrections_user_no_records():
    user = "mcaceres2017"  
    url = f"{HOST}/corrections/{user}"
    response = requests.get(url)
    assert response.status_code == 404, "Test 2: Obtención de historial de correcciones de usuario sin registros falló."
    

def test_get_corrections_user_nonexistent():
    user = "marcianito2023"  
    url = f"{HOST}/corrections/{user}"
    response = requests.get(url)
    assert response.status_code == 404, "Test 3: Obtención de historial de correcciones de usuario inexistente falló."


def test_get_corrections_server_error():
    user = "asanchez2017"  
    url = f"{HOST}/corrections/{user}"
    response = requests.get(url)
    assert response.status_code == 500, "Test 4: Manejo de errores en servidor al obtener historial de correcciones falló."
"""

#CREATE CORRECTION

def test_post_correction_success():
    # Reemplaza con datos válidos para crear una corrección
    correction_data = {
        "oid": "ZTF18aaqlcen",
        "user": "asanchez2017",
        "pid":"1",
        "label": "Concluyent"
    }
    url = f"{HOST}/corrections/"
    response = requests.post(url, json=correction_data)
    assert response.status_code == 200, "Test 8: Creación de corrección exitosa falló."
