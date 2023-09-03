
# NeivaNet

## Descripción

NeivaNet es un proyecto de red social centrado en la ciudad de Neiva. Esta plataforma tiene como objetivo proporcionar un espacio para quejas, comentarios y participación en servicios públicos. A través de NeivaNet, los ciudadanos pueden expresar sus opiniones y preocupaciones, así como colaborar para mejorar la comunidad.

## Instrucciones para ejecutar el proyecto

### Requisitos previos

- Python 3.11.5
- pip
- Virtualenv

### Pasos

1. **Clonar el Repositorio**

    ```bash
    git clone https://github.com/tu_usuario/NeivaNet.git
    cd NeivaNet
    ```

2. **Crear un entorno virtual y activarlo**

    ```bash
    python3 -m venv venv
    source venv/bin/activate  # En Windows use `venv\Scripts\activate`
    ```

3. **Instalar las dependencias**

    ```bash
    pip install -r requirements.txt
    ```

4. **Realizar las migraciones de la base de datos**

    ```bash
    python manage.py migrate
    ```

5. **Ejecutar el servidor de desarrollo de Django**

    ```bash
    python manage.py runserver
    ```

Ahora, abre tu navegador y navega a `http://127.0.0.1:8000/` para ver el proyecto en acción.

## Contribución

Siéntete libre de contribuir al proyecto. Para cualquier bug, pregunta o sugerencia, puedes abrir un issue.

## Licencia

MIT

