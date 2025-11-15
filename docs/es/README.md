# My Spotify Playlists Downloader

Exporta la información de tus listas de reproducción de Spotify a archivos JSON para respaldo, análisis o migración.

---

## Descripción

`my_spotify_playlists_downloader.py` es un script de línea de comandos en Python diseñado para ayudarte a exportar y
respaldar tus listas de reproducción de Spotify. Se conecta a tu cuenta de Spotify mediante OAuth y recupera todas tus
listas junto con metadatos detallados de cada pista. Puedes exportarlas como un solo archivo JSON consolidado o como
archivos JSON individuales por lista de reproducción.

Este script es ideal para:

- Respaldar los datos de tu biblioteca musical.
- Prepararte para migrar a otro servicio de música.
- Analizar tus listas de reproducción con fines personales o de investigación.
- Aprender a integrar la Web API de Spotify usando Python.

El proyecto se publica bajo la licencia MIT y está destinado para uso educativo y personal.

---

## Funcionalidades

- Exporta **todas las listas de reproducción y metadatos de pistas**, incluyendo nombre, artistas, álbum, fecha de
  lanzamiento y más.
- **Exporta canciones favoritas** (colección de pistas guardadas).
- Opción para **dividir la exportación** en archivos JSON individuales por lista.
- **Combinaciones flexibles de exportación** (canciones favoritas y/o listas de reproducción).
- **Generación de reporte HTML** con diseño moderno y responsivo mostrando estadísticas y rutas de archivos.
- Incluye la **posición de la pista en la lista**, usuario que la agregó y fecha de adición.
- **Registro de logs** tanto en consola como en archivo para trazabilidad.
- **Portable**: funciona en Windows, macOS y Linux.
- Configuración simple con dependencias mínimas.

---

## Guía Paso a Paso para Comenzar

Sigue estos pasos para configurar y usar la herramienta. No te preocupes si no estás familiarizado con programación – te guiaré en todo.

### Paso 1: Verificar la Instalación de Python

Primero, asegúrate de tener Python instalado en tu computadora.

**Verificar si Python está instalado:**

Abre tu terminal (Símbolo del sistema en Windows, Terminal en Mac/Linux) y escribe:

```shell
python --version
```

Deberías ver algo como `Python 3.10.x` o superior. Si ves un error o una versión inferior a 3.10, necesitas instalar o actualizar Python:

- **Descargar Python:** Visita [python.org/downloads](https://www.python.org/downloads/) y descarga Python 3.10 o más reciente.
- **Durante la instalación:** Asegúrate de marcar la casilla que dice "Add Python to PATH" (Agregar Python al PATH).

### Paso 2: Configurar una Cuenta de Desarrollador de Spotify

Para acceder a tus datos de Spotify, necesitas crear una cuenta de desarrollador de Spotify y obtener credenciales especiales (como llaves para acceder a tu cuenta).

**Sigue esta guía detallada:** [SPOTIFY_DEVELOPER_SETUP.md](SPOTIFY_DEVELOPER_SETUP.md)

Esta guía te explicará:

- Crear una cuenta de desarrollador de Spotify (¡es gratis!)
- Crear una aplicación en el Panel de Spotify
- Obtener tu **Client ID** y **Client Secret**
- Configurar la **Redirect URI**

**Importante:** ¡Guarda tu Client ID y Client Secret a mano – los necesitarás en los siguientes pasos!

### Paso 3: Descargar el Script

#### Opción A: Descargar como ZIP (más fácil para principiantes)

En esta página del repositorio de GitHub, ve a la parte superior y:

1. Haz clic en el botón verde "Code"
2. Selecciona "Download ZIP"
3. Extrae el archivo ZIP en una carpeta de tu computadora (ej. `Documentos/spotify-downloader`)

#### Opción B: Usando Git (si tienes Git instalado)

Abre tu terminal y ejecuta:

```shell
git clone https://github.com/novama/my_spotify_playlists_downloader.git
cd my_spotify_playlists_downloader
```

### Paso 4: Instalar las Dependencias Necesarias

El script necesita algunos paquetes adicionales de Python para funcionar. Vamos a instalarlos.

1. **Abre tu terminal** y navega a la carpeta donde extrajiste/clonaste el script:

   ```shell
   cd ruta/a/my_spotify_playlists_downloader
   ```

   Reemplaza `ruta/a/` con la ubicación real (ej. `cd Descargas/spotify-downloader`).

2. **Instalar dependencias:**

   ```shell
   pip install -r requirements.txt
   ```

   Espera a que se complete la instalación. Verás mensajes indicando que los paquetes se están instalando.

### Paso 5: Configurar tus Credenciales

Ahora necesitas indicarle al script tus credenciales de Spotify.

1. **Encuentra el archivo `.env.example`** en la carpeta del script.

2. **Haz una copia y renómbrala a `.env`** (sin la parte `.example`):

   - **Windows:** Clic derecho en el archivo → "Copiar" → Pegar → Renombrar a `.env`
   - **Mac/Linux:** En la terminal, ejecuta: `cp .env.example .env`

3. **Abre el archivo `.env`** con un editor de texto (Bloc de notas en Windows, TextEdit en Mac, o cualquier editor de código).

4. **Completa tus credenciales** del Paso 2:

   ```env
   SPOTIFY_CLIENT_ID=tu_client_id_aqui
   SPOTIFY_CLIENT_SECRET=tu_client_secret_aqui
   SPOTIFY_REDIRECT_URI=http://127.0.0.1:8000/callback
   ```

   Reemplaza `tu_client_id_aqui` y `tu_client_secret_aqui` con los valores reales de tu Panel de Desarrollador de Spotify.

   **Importante:** ¡La `SPOTIFY_REDIRECT_URI` debe coincidir exactamente con lo que configuraste en tu aplicación de Spotify!

5. **Configuraciones opcionales** (puedes dejarlas por defecto o personalizarlas):

   ```env
   OUTPUT_DIR=./output
   LOG_LEVEL=INFO
   ```

6. **Guarda el archivo** y ciérralo.

### Paso 6: Ejecuta tu Primera Exportación

Ahora estás listo para exportar tus listas de reproducción. Aquí hay algunos escenarios comunes:

#### Exportación Básica: Todas las Listas

Exporta todas tus listas de reproducción a un solo archivo JSON:

```shell
python my_spotify_playlists_downloader.py
```

**Qué sucede:**

- Se abrirá una ventana del navegador pidiéndote que inicies sesión en Spotify (solo la primera vez)
- Después de autorizar la aplicación, tus listas de reproducción serán exportadas
- Los archivos se guardarán en la carpeta `output` (o donde lo hayas especificado en `.env`)

#### Exportar Todo con un Reporte Bonito

Exporta todas las listas Y canciones favoritas, con un hermoso reporte HTML:

```shell
python my_spotify_playlists_downloader.py --all_playlists --liked_songs --html_report
```

**Lo que obtienes:**

- Todas tus listas de reproducción exportadas como archivos JSON
- Tus canciones favoritas exportadas en un archivo JSON separado
- Un bonito reporte HTML que puedes abrir en tu navegador con estadísticas y ubicaciones de archivos

#### Exportar Cada Lista como Archivos Separados

Mantén cada lista en su propio archivo:

```shell
python my_spotify_playlists_downloader.py --split
```

#### Exportar Solo tus Canciones Favoritas

Solo exporta tus pistas guardadas:

```shell
python my_spotify_playlists_downloader.py --liked_songs
```

#### Exportar una Lista Específica

Solo exporta una lista de reproducción por nombre:

```shell
python my_spotify_playlists_downloader.py --playlist_name "Mi Lista Favorita"
```

Reemplaza `"Mi Lista Favorita"` con el nombre real de tu lista de reproducción.

#### Comienzo Limpio (Eliminar Exportaciones Antiguas Primero)

Elimina las exportaciones antiguas antes de crear nuevas:

```shell
python my_spotify_playlists_downloader.py --clean_output --all_playlists --html_report
```

#### El Paquete Completo (¡Recomendado!)

Exporta todo con todas las características habilitadas:

```shell
python my_spotify_playlists_downloader.py --split --all_playlists --liked_songs --html_report --clean_output
```

Esto hará:

1. Eliminar archivos de exportación antiguos (comienzo limpio)
2. Exportar cada lista como un archivo JSON separado
3. Exportar tus canciones favoritas
4. Generar un hermoso reporte HTML
5. Mostrarte exactamente dónde se guardó todo

---

## Entendiendo las Opciones

Esto es lo que hace cada opción:

| Opción | Qué Hace |
|--------|----------|
| `--split` | Crea archivos JSON separados para cada lista (en lugar de un archivo grande) |
| `--liked_songs` | Exporta tu colección de canciones favoritas/guardadas |
| `--all_playlists` | Exporta todas las listas (úsalo con `--liked_songs` para exportar todo) |
| `--html_report` | Crea un hermoso reporte HTML con estadísticas y ubicaciones de archivos |
| `--clean_output` | Elimina archivos JSON y HTML antiguos antes de exportar nuevos |
| `--playlist_name "Nombre"` | Solo exporta la lista con este nombre específico |
| `--output_dir ./carpeta` | Guarda los archivos en una carpeta específica |

**Consejo:** Puedes combinar múltiples opciones, solo agrégalas una tras otra, separadas por espacios.

---

## Notas adicionales

- Los nombres de las listas usados como nombre de archivo son saneados: se eliminan caracteres inválidos y emojis, pero
  se conservan los acentos y el formato original.
- Al usar `--playlist_name`, el script registra el filtro normalizado y la cantidad de listas a exportar.
- Al usar `--clean_output`, el script registra cada archivo eliminado (JSON y HTML) y confirma la limpieza del directorio.
- El comportamiento por defecto exporta solo listas de reproducción. Usa `--liked_songs` para canciones favoritas o `--all_playlists` para ambos.
- Puedes usar `--liked_songs` y `--playlist_name` juntos para exportar una lista específica junto con tus canciones favoritas.
- El reporte HTML (`--html_report`) incluye las rutas de los archivos para cada lista exportada y para las canciones favoritas.

---

## Ejemplo de Salida

Cada objeto de lista exportada incluye:

- Nombre de la lista, ID, nombre visible y username del propietario, descripción, snapshot_id
- Lista de pistas con:
  - Posición en la lista
  - Nombre de la pista, artistas, álbum, fecha de lanzamiento
  - URL en Spotify
  - Fecha de adición a la lista y usuario que la agregó

---

## Descargo de Responsabilidad

Este script se proporciona únicamente con fines educativos.
Úsalo de manera responsable con tu propia cuenta de Spotify.
El autor no asume ninguna responsabilidad por mal uso o pérdida de datos causada por su uso.
El código es limpio y está libre de componentes maliciosos.

## Descargo de Responsabilidad de Marca Registrada

Spotify es una marca registrada de Spotify AB.
Este proyecto **no está afiliado, patrocinado ni respaldado por Spotify** de ninguna manera.
Todas las referencias a Spotify se hacen únicamente con fines informativos y educativos.

Cualquier captura de pantalla o imagen utilizada en esta documentación tiene únicamente fines ilustrativos para ayudar a
los usuarios a configurar su cuenta de desarrollador y no implica ninguna asociación con Spotify AB.

---

## Licencia

Este proyecto está licenciado bajo la [Licencia MIT](../../LICENSE).
