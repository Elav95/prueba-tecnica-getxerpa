# Proyecto de Enriquecimiento de Transacciones

Este proyecto utiliza Django para enriquecer transacciones financieras mediante un API RESTful.

## Configuración del Entorno Virtual

Es recomendable utilizar un entorno virtual para aislar las dependencias del proyecto. Puedes crear uno de la siguiente manera:

```bash
python -m venv .env
```

Luego, activa el entorno virtual:

**En Windows:**
```bash
.env\Scripts\activate
```

**En Unix o MacOS:**

```bash
source .env/bin/activate
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
python manage.py runscript import_data
```

**Nota:** Al ejecutar el script import_data, se agregarán automáticamente las categorías, comercios y keywords del archivo de datos proporcionado.

## Ejecutar el Servidor

Inicia el servidor de desarrollo:

```bash
python manage.py runserver
```

El servidor estará disponible en http://127.0.0.1:8000/.

## Endpoints

### Categorías

#### Agregar Categoría - POST /api/categories/

Para agregar categorías, realiza una solicitud POST a:

```bash
http://127.0.0.1:8000/api/categories/
```

El cuerpo de la solicitud debe contener un JSON con la categoría a agregar:

```json
{
  "name": "Entretenimiento & Recreación",
  "type": "expense"
}
```

#### Obtener Lista de Categorías - GET /api/categories/

Para obtener una lista de categorias, realiza una solicitud GET a:

```bash
http://127.0.0.1:8000/api/categories/
```

Obtendrás una respuesta con un array de objetos JSON, donde cada objeto representa una categoría.

**Ejemplo de respuesta**

```json
[
    {
        "id": "79a9e1d5-176d-41c2-a592-a745cb4302d4",
        "name": "Entretenimiento & Recreación",
        "type": "expense",
        "created_at": "2023-12-31T17:30:55.138723Z",
        "updated_at": "2023-12-31T17:30:55.138723Z"
    },
    // ... otras categorías
]
```

### Comercios

#### Agregar Comercio - POST /api/merchants/

Para agregar un comercio, realiza una solicitud POST a:

```bash
http://127.0.0.1:8000/api/merchants/
```

El cuerpo de la solicitud debe contener un JSON con el comercio a agregar:

```json
{
  "merchant_name": "Pedidos Ya",
  "merchant_logo": "https://live.pystatic.com/webassets/pwa/icons/icon-384x384.png",
  "category": "0a634e4679fb4bd1a0f70fda27076a1a"
}
```

#### Obtener Lista de Comercios - GET /api/merchants/

Para obtener una lista de comercios, realiza una solicitud GET a:

```bash
http://127.0.0.1:8000/api/merchants/
```

Obtendrás una respuesta con un array de objetos JSON, donde cada objeto representa un comercio.

**Ejemplo de respuesta**

```json
[
    {
        "id": "424b4f71-d3b9-4865-84ec-b32052df1333",
        "merchant_name": "Uber",
        "merchant_logo": "https://media.wired.com/photos/592736e0f3e2356fd800bcae/master/w_1600%2Cc_limit/Uber_Logobit_Digital_black.jpg",
        "created_at": "2023-12-31T17:30:56.831919Z",
        "updated_at": "2023-12-31T17:30:56.831919Z",
        "category": "d3a36995-2900-4bf0-b1c3-8fc186b057c6"
    },
    // ... otros comercios
  ]
```

### Keywords

#### Agregar Keyword - POST /api/keywords/

Para agregar una keyword, realiza una solicitud POST a:

```bash
http://127.0.0.1:8000/api/keywords/
```

El cuerpo de la solicitud debe contener un JSON con la keyword a agregar:

```json
{
  "keyword": "pedidosya",
  "merchant": "28058183-c65d-43ce-bd71-7c05ca0ab474"
}
```

#### Obtener Lista de Keywords - GET /api/keywords/

Para obtener una lista de las keywords, realiza una solicitud GET a:

```bash
http://127.0.0.1:8000/api/keywords/
```

Obtendrás una respuesta con un array de objetos JSON, donde cada objeto representa una keyword.

**Ejemplo de respuesta**

```json
[
    {
        "id": "1b700aba-760e-4d69-9acb-95d59a9ca7a1",
        "keyword": "uber",
        "created_at": "2023-12-31T17:30:58.448915Z",
        "updated_at": "2023-12-31T17:30:58.448915Z",
        "merchant": "424b4f71-d3b9-4865-84ec-b32052df1333"
    },
    // ... otras keywords
]
```

### Transactions

#### Agregar Transaction - POST /api/transactions/

Para agregar una transacción, realiza una solicitud POST a:

```bash
http://127.0.0.1:8000/api/transactions/
```

El cuerpo de la solicitud debe contener un JSON con la transacción a agregar:

```json
{
  "amount": -230,
  "date": "2023-11-04",
  "description": "PETROBRAS 9 NTE/7 ORNTE"
}

```

Este proceso solo agrega las transacciones a la base de datos y no las enriquece. Para enriquecer transacciones existentes, utiliza el endpoint específico para ello.

#### Obtener Lista de Transacciones - GET /api/keywords/

Para obtener una lista de las transacciones, realiza una solicitud GET a:

```bash
http://127.0.0.1:8000/api/transactions/
```

Obtendrás una respuesta con un array de objetos JSON, donde cada objeto representa una transacción.

**Ejemplo de respuesta**

```json
[
    {
        "id": "bfded25b-8b69-4399-884d-c1c5e5e185d3",
        "description": "PETROBRAS 9 NTE/7 ORNTE",
        "amount": "-230.00",
        "date": "2023-11-04",
        "created_at": "2023-12-31T16:24:56.002807Z",
        "updated_at": "2023-12-31T16:24:56.002807Z"
    },
    // ... otras transacciones
]
```

### Enriquecimiento de Transacciones

#### Enriquecer transacciones - POST /api/transactions/enrich_transactions/

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

**Ejemplo de respuesta:**

```json
{
    "enriched_transactions": [
        {
            "transaction_id": "7dff1641-3265-4cbc-9088-6581ee02ed96",
            "description": "PETROBRAS 9 NTE/7 ORNTE",
            "amount": "-230.00",
            "date": "2023-11-04",
            "category_name": "Automóvil & Transporte",
            "type": "expense",
            "merchant_name": "Petrobras",
            "merchant_logo": "https://cdn.worldvectorlogo.com/logos/petrobras-8.svg",
            "keyword": "petrobras"
        },
        // ... otras transacciones enriquecidas
    ]
}
```

Cuando se envía una transacción con un ID existente, el sistema realiza múltiples verificaciones. Si la transacción aún no está registrada en la base de datos de transacciones, se crea una nueva instancia utilizando el ID proporcionado.

En el caso de una transacción existente, se verifica la coherencia de los datos con los registrados. Si la información coincide, se procede a verificar la presencia en la base de datos de transacciones enriquecidas. Si la transacción ya está enriquecida, se actualiza su instancia en la base de datos de transacciones enriquecidas con los nuevos datos. Este proceso permite enriquecer nuevamente transacciones en caso de incorporación de nuevos datos sobre comercios, categorías o keywords.

En situaciones en las que la transacción aún no está enriquecida, se realiza el enriquecimiento y se crea una nueva instancia en la base de datos de transacciones enriquecidas.

Es importante destacar que no es necesario enviar una transacción con un ID para que sea enriquecida; el sistema manejará automáticamente la asignación y verificación.

**Consideraciones:**

- El proyecto utiliza un entorno virtual para gestionar las dependencias.
Las migraciones de la base de datos deben realizarse antes de ejecutar el servidor.
- Utiliza el script import_data para cargar los datos iniciales.
- Asegúrate de que el servidor esté en ejecución antes de realizar solicitudes a la API.
