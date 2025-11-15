# Configuración de tu Cuenta de Desarrollador de Spotify

## ¿Por qué se necesita una Cuenta de Desarrollador de Spotify?

Este script utiliza la Web API de Spotify para recuperar tus listas de reproducción.  
Para acceder a la API, debes autenticarte mediante OAuth, lo que requiere:

- Un **Client ID** y **Client Secret** obtenidos desde el panel de desarrollador de Spotify.
- Un **Redirect URI** registrado para completar el flujo de autenticación de forma segura.

> **Nota:** Tu cuenta de desarrollador puede ser la misma que tu cuenta de usuario de Spotify. Crear una aplicación de
> desarrollador **no afecta** tus listas ni el uso de tu cuenta actual.

---

## Cómo crear tu Cuenta de Desarrollador de Spotify

### 1. Inicia sesión en el panel de Desarrollador de Spotify

- Ve a [developer.spotify.com/dashboard](https://developer.spotify.com/dashboard)
- Haz clic en **“Log In”** e ingresa con tus credenciales de Spotify.

---

### 2. Acepta los Términos de Desarrollador

- En tu primera visita, Spotify te pedirá aceptar los **Términos de servicio de desarrollador**.
- Léelos y acéptalos para continuar.

---

### 3. Crea una Nueva Aplicación

1. Haz clic en **“Create an App”**.
2. Ingresa un **nombre para la app** (por ejemplo, *My Playlists Exporter*).
3. Ingresa una **descripción para la app** (opcional).
4. Acepta los términos de desarrollador si se solicitan.
5. Haz clic en **“Create”**.

![Formulario de creación de app en Spotify Developer Dashboard](../images/create-app-form-in-dev-account.png)

![Ejemplo de formulario de app completado](../images/create-app-form-example.png)

---

### 4. Obtén tu Client ID y Client Secret

- Una vez creada la app, verás:
  - Tu **Client ID** (visible inmediatamente).
  - Tu **Client Secret** (haz clic en **“Show Client Secret”** para verlo).

Copia ambos valores y añádelos a tu archivo `.env`.

---

### 5. Configura tu Redirect URI

1. En el panel de tu app, haz clic en **“Edit Settings”**.
2. Bajo **Redirect URIs**, añade: <http://127.0.0.1:8000/callback> *(o el Redirect URI exacto que usarás en tu
   configuración `.env`)*.
3. Haz clic en **Save**.

![Configuración de Redirect URIs](../images/redirect-uris-capture.png)

> **Para más información:**  
> Consulta
> la [documentación oficial de Spotify sobre Redirect URIs](https://developer.spotify.com/documentation/web-api/concepts/redirect_uri)
> para detalles completos.

---

## Próximos Pasos

✅ Tu cuenta de desarrollador ya está lista.  
✅ Edita tu archivo `.env` con los valores correctos de *Client ID*, *Client Secret* y *Redirect URI*, luego ejecuta el
script para comenzar a exportar tus listas.

---

## Descargo de Responsabilidad

Tus credenciales de app de Spotify Developer son personales.  
No compartas tu Client Secret públicamente ni lo subas a control de versiones.

## Descargo de Responsabilidad de Marca Registrada

Spotify es una marca registrada de Spotify AB.  
Este proyecto **no está afiliado, patrocinado ni respaldado por Spotify** de ninguna manera.  
Todas las referencias a Spotify se hacen únicamente con fines informativos y educativos.

Cualquier captura de pantalla o imagen utilizada en esta documentación tiene únicamente fines ilustrativos para ayudar a
los usuarios a configurar su cuenta de desarrollador y no implica ninguna asociación con Spotify AB.
