# Setting up your Spotify Developer Account

## Why is a Spotify Developer Account needed?

This script uses Spotify’s Web API to retrieve your playlists.  
To use the API, you must authenticate via OAuth, which requires:

- A **Client ID** and **Client Secret** from Spotify Developer Dashboard.
- A registered **Redirect URI** to complete the authentication flow securely.

> **Note:** Your Spotify Developer account can be the same as your existing Spotify user account. Creating a developer
> account does NOT affect your current playlists or music usage.

---

## How to create your Spotify Developer account

### 1. Log in to the Spotify Developer Dashboard

- Go to [developer.spotify.com/dashboard](https://developer.spotify.com/dashboard)
- Click **Log In** and enter your existing Spotify credentials.

---

### 2. Accept the Developer Terms

- On your first visit, Spotify will ask you to accept the **Developer Terms of Service**.
- Read and accept to continue.

---

### 3. Create a new application

1. Click **“Create an App”**.
2. Enter an **App Name** (e.g. *My Playlists Exporter*).
3. Enter an **App Description** (optional).
4. Accept the Developer Terms if prompted.
5. Click **Create**.

![Spotify Developer Dashboard - Create App Form](../images/create-app-form-in-dev-account.png)

![Example Create App Form Filled](../images/create-app-form-example.png)

---

### 4. Get your Client ID and Client Secret

- Once your app is created, you will see:
  - **Client ID** (visible immediately)
  - **Client Secret** (click **“Show Client Secret”** to view)

Copy both values to your `.env` file.

---

### 5. Configure Redirect URI

1. In your app dashboard, click **“Edit Settings”**.
2. Under **Redirect URIs**, add: <http://127.0.0.1:8000/callback> *(or the exact Redirect URI you will use in your .env
   configuration)*
3. Click **Save**.

![Redirect URIs Configuration](../images/redirect-uris-capture.png)

> **For more information:**  
>
See [Spotify’s official documentation on Redirect URIs](https://developer.spotify.com/documentation/web-api/concepts/redirect_uri)
for detailed guidelines.

---

## Next steps

✅ Your Developer account is now ready.  
✅ Edit your `.env` file to include the correct *Client ID*, *Client Secret*, and *Redirect URI* values, then run the
script to begin exporting your playlists.

---

## Disclaimer

Your Spotify Developer app credentials are personal.  
Do **not** share your Client Secret publicly or commit it to version control.

## Trademark disclaimer

Spotify is a registered trademark of Spotify AB.  
This project is **not affiliated with, sponsored, or endorsed by Spotify** in any way.  
All references to Spotify are made solely for informational and educational purposes.

Any screenshots or images used in this documentation are for illustrative purposes only to assist users in setting up
their Developer account and do not imply any association with Spotify AB.
