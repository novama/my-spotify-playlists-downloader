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
- **Generación de reporte HTML** con diseño moderno y responsivo.
- Incluye la **posición de la pista en la lista**, usuario que la agregó y fecha de adición.
- **Registro de logs** tanto en consola como en archivo para trazabilidad.
- **Portable**: funciona en Windows, macOS y Linux.
- Configuración simple con dependencias mínimas.

---

## Requisitos

- Python 3.10 o superior
- Una [cuenta de desarrollador de Spotify](SPOTIFY_DEVELOPER_SETUP.md) para crear una aplicación y obtener tu Client ID
  y Client Secret

Instala las dependencias con:

```shell
pip install -r requirements.txt
```

---

## Configuración

1. **Clona el repositorio**

    ```shell
    git clone https://github.com/yourusername/my_spotify_playlists_downloader.git
    cd my_spotify_playlists_downloader
    ```

2. **Crea tu archivo `.env`**

   Copia el ejemplo proporcionado:

    ```shell
    cp .env.example .env
    ```

3. **Edita `.env` y configura tus variables**

   Mínimo requerido:

    - `SPOTIFY_CLIENT_ID`
    - `SPOTIFY_CLIENT_SECRET`
    - `SPOTIFY_REDIRECT_URI` (debe coincidir exactamente con la configuración de tu app en Spotify, por
      ejemplo <http://127.0.0.1:8000/callback>)

   Variables opcionales:

    - `OUTPUT_DIR`: Directorio donde se guardarán los archivos exportados (default: ./playlists)
    - `OUTPUT_PREFIX_SPLIT`: Prefijo para archivos en modo dividido
    - `OUTPUT_PREFIX_SINGLE`: Prefijo para el archivo único exportado
    - `LOG_DIR`: Directorio donde se almacenarán los logs (default: ubicación del script)
    - `LOG_LEVEL`: Nivel de log (default: INFO, puede ser DEBUG, INFO, WARNING, ERROR, CRITICAL)

### Configuración de Cuenta de Desarrollador de Spotify

Este script requiere una cuenta de desarrollador de Spotify y credenciales de aplicación registradas.
Consulta [SPOTIFY_DEVELOPER_SETUP.md](SPOTIFY_DEVELOPER_SETUP.md) para instrucciones detalladas.

---

## Uso

### Exportar todas las listas a un solo archivo JSON (por defecto)

```shell
python my_spotify_playlists_downloader.py
```

### Exportar cada lista como un archivo JSON individual

```shell
python my_spotify_playlists_downloader.py --split
```

### Especificar un directorio de salida personalizado

```shell
python my_spotify_playlists_downloader.py --output_dir ./my_exports
```

### Exportar solo una lista específica por nombre

```shell
python my_spotify_playlists_downloader.py --playlist_name "Nombre de mi playlist"
```

- El script exportará únicamente la lista cuyo nombre coincida (sin distinguir mayúsculas/minúsculas, normalizado) con
  el valor proporcionado.
- Si no hay coincidencias, se registrará un error y no se exportará ningún archivo.

### Exportar solo canciones favoritas (sin listas de reproducción)

```shell
python my_spotify_playlists_downloader.py --liked_songs
```

- Exporta tu colección de pistas guardadas (canciones favoritas) a un archivo JSON dedicado.
- Por defecto, el script exporta listas de reproducción. Usa esta bandera para exportar solo canciones favoritas.

### Exportar listas de reproducción y canciones favoritas

```shell
python my_spotify_playlists_downloader.py --all_playlists
```

- Exporta tanto tus listas de reproducción como tus canciones favoritas.
- Equivalente a usar `--liked_songs` sin especificar `--playlist_name`.

### Generar reporte HTML

```shell
python my_spotify_playlists_downloader.py --html_report
```

- Genera un reporte HTML profesional y responsivo con resumen de toda la exportación.
- Incluye estadísticas, recuentos de listas/pistas, y rutas de archivos exportados.
- El reporte se guarda en el directorio de salida como `SpotifyExportReport_YYYYMMDD_HHMMSS.html`.

### Limpiar el directorio de salida antes de exportar

```shell
python my_spotify_playlists_downloader.py --clean_output
```

- Todos los archivos JSON y HTML en el directorio de salida serán eliminados antes de exportar.
- Útil para evitar mezclar exportaciones antiguas y nuevas.

### Ejemplos combinados

**Exportar todo con reporte HTML:**

```shell
python my_spotify_playlists_downloader.py --split --all_playlists --html_report
```

**Limpiar, exportar solo canciones favoritas con reporte:**

```shell
python my_spotify_playlists_downloader.py --liked_songs --html_report --clean_output
```

**Exportar lista específica como archivo dividido con limpieza:**

```shell
python my_spotify_playlists_downloader.py --split --playlist_name "Mi Playlist" --clean_output
```

**Exportar todo en archivos divididos con reporte HTML después de limpiar:**

```shell
python my_spotify_playlists_downloader.py --split --all_playlists --html_report --clean_output
```

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
