import sys
import os

# Agrega la raíz del proyecto al path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from src.database.db import db

# Colección
edificios = db["edificios"]

# Lista de edificios a insertar
datos = [
    {
        "nombre": "Sor Juana",
        "coordenadas": [19.2331431, -98.8419580],
            "descripcion": "Planta baja: Laboratorios \nEscaleras: Baños Damas \nPlanta alta: Aulas G y Departamento de servicio social y residencias profesionales, binculacion, departamento de egresado \nEscaleras: Baños Hombres"
    },
    {
        "nombre": "Biblioteca",
        "coordenadas": [19.2332447, -98.8424854],
        "descripcion": "Planta baja: Sala de TICS, Cubículos, Encargado de biblioteca, Auditorio Secundario, Celex"
    },
    {
        "nombre": "Bicentenario",
        "coordenadas": [19.2328927, -98.8412992],
        "descripcion": "Planta baja: Jefaturas de división, enfermería, baños H/M,salones E \nPlanta alta: salones E, baños H/M  "
    },
    {
        "nombre": "Canchas",
        "coordenadas": [19.2336799, -98.8399960],
        "descripcion": "Canchas de basquetbol "
    },
    {
        "nombre": "Auditorio Principal",
        "coordenadas": [19.2334900, -98.8417448],
        "descripcion": "Auditorio donde se llevan a cabo conferencias importantes como platicas, exposiciones del FLISOL, Etc"
    },
    {
        "nombre": "Revolución",
        "coordenadas": [19.2337803, -98.8413421],
        "descripcion": "Cabinas, Baños H/M, Aulas F, cabinas de educación a distancia, Laboratorios de industrial"
    },
    {
        "nombre": "Nezahualcoyotl",
        "coordenadas": [19.2333707, -98.8404751],
        "descripcion": "Planta baja: Aulas A, Baños H/M\nPlanta alta: Aulas A, dirección general, Departamento  de finanzas, Baños H/M"
    },
    {
        "nombre": "Morelos",
        "coordenadas": [19.2329097, -98.8413290],
        "descripcion": "Máquinas para ejercitarse"
    },
    {
        "nombre": "Gymnasio",
        "coordenadas": [19.2332757, -98.8401254],
        "descripcion": "Máquinas para ejercitarse"
    },
    {
        "nombre": "Control Escolar",
        "coordenadas": [19.2327762, -98.840661],
        "descripcion": "Lugar donde puedes tramitar constancias, inscribirte, checar convocatorias de becas, etc, titulación, laboratorios de electrónica"
    },
    { 
        "nombre": "Gallineros",
        "coordenadas": [19.2329414, -98.8402746],
        "descripcion": "Conjunto de salones de planta baja catalogados como salones C"
    },
    {
        "nombre": "Cafetería",
        "coordenadas": [19.2333564, -98.8412603],
        "descripcion": "Ideal para comprar tus alimentos"
    },
    {
        "nombre": "Acts Complementarias",
        "coordenadas": [19.2335739, -98.8401059],
        "descripcion": "Puedes realizar desde actividades que amplien tu creatividad o reten tu resistencia fisica"
    }
]

# Insertar los edificios
resultado = edificios.insert_many(datos)
print(f"Edificios insertados con IDs: {resultado.inserted_ids}")