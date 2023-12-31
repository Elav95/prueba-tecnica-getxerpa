# Proyecto de Enriquecimiento de Transacciones

Este proyecto utiliza Django para enriquecer transacciones financieras mediante un API RESTful.

## Configuración del Entorno Virtual

Es recomendable utilizar un entorno virtual para aislar las dependencias del proyecto. Puedes crear uno de la siguiente manera:

```bash
python -m venv venv
```

## Configuración del Entorno Virtual

Luego, activa el entorno virtual:

**En Windows:**
```bash
venv\Scripts\activate
```

## Configuración del Entorno Virtual

Luego, activa el entorno virtual:

**En Windows:**

```bash
venv\Scripts\activate
```

**En Unix o MacOS:**

```bash
source venv/bin/activate
```

## Instalación de Dependencias

Instala las dependencias del proyecto utilizando pip:

```bash
pip install -r requirements.txt
```

## Migraciones de la Base de Datos

Realiza las migraciones de la base de datos para crear las tablas necesarias:

```bash
python manage.py migrate
```

## Importar Datos

Utiliza el script de importación para cargar datos en la base de datos:

```bash
python manage.py import_data
```

## Ejecutar el Servidor

Inicia el servidor de desarrollo:

```bash
python manage.py runserver
```

El servidor estará disponible en http://127.0.0.1:8000/.

## Endpoint de Enriquecimiento de Transacciones
Para enriquecer transacciones, realiza una solicitud POST al siguiente endpoint:

```bash
http://127.0.0.1:8000/api/transactions/enrich_transactions/
```

El cuerpo de la solicitud debe contener un JSON con la lista de transacciones a enriquecer.

**Ejemplo:**

```json
{
  "transactions": [
    {
      "id": "uuid4",
      "description": "PYU *UberEats",
      "amount": -300.00,
      "date": "2023-12-01"
    },
    // ... otras transacciones
  ]
}
```

**Consideraciones:**

- Si encuentras algún problema, asegúrate de revisar la documentación y los mensajes de error.
- El proyecto utiliza un entorno virtual para gestionar las dependencias.
Las migraciones de la base de datos deben realizarse antes de ejecutar el servidor.
- Utiliza el script import_data para cargar datos iniciales.
- Asegúrate de que el servidor esté en ejecución antes de realizar solicitudes a la API.
