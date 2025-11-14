# Configurando sua Conta de Desenvolvedor Spotify

## Por que é necessário ter uma Conta de Desenvolvedor Spotify?

Este script usa a Web API do Spotify para recuperar suas playlists.  
Para acessar a API, você deve autenticar via OAuth, o que requer:

- Um **Client ID** e **Client Secret** do painel de desenvolvedor Spotify.
- Um **Redirect URI** registrado para completar o fluxo de autenticação com segurança.

> **Nota:** Sua conta de desenvolvedor pode ser a mesma conta Spotify que você já utiliza. Criar um app de desenvolvedor
**não afeta** suas playlists ou uso atual do Spotify.

---

## Como Criar sua Conta de Desenvolvedor Spotify

### 1. Faça login no painel de desenvolvedor Spotify

- Acesse [developer.spotify.com/dashboard](https://developer.spotify.com/dashboard)
- Clique em **“Log In”** e entre com suas credenciais Spotify.

---

### 2. Aceite os Termos de Desenvolvedor

- Na primeira visita, o Spotify pedirá que você aceite os **Termos de Serviço de Desenvolvedor**.
- Leia e aceite para continuar.

---

### 3. Crie um Novo Aplicativo

1. Clique em **“Create an App”**.
2. Insira um **nome para o app** (ex: *My Playlists Exporter*).
3. Insira uma **descrição para o app** (opcional).
4. Aceite os termos de desenvolvedor se solicitado.
5. Clique em **“Create”**.

![Formulário de criação de app no painel Spotify Developer](../images/create-app-form-in-dev-account.png)

![Exemplo de formulário de app preenchido](../images/create-app-form-example.png)

---

### 4. Obtenha seu Client ID e Client Secret

- Após criar o app, você verá:
  - **Client ID** (visível imediatamente)
  - **Client Secret** (clique em **“Show Client Secret”** para visualizar)

Copie ambos e adicione ao seu arquivo `.env`.

---

### 5. Configure seu Redirect URI

1. No painel do app, clique em **“Edit Settings”**.
2. Em **Redirect URIs**, adicione: <http://127.0.0.1:8000/callback> *(ou o Redirect URI exato configurado no seu `.env`)*.
3. Clique em **Save**.

![Configuração de Redirect URIs](../images/redirect-uris-capture.png)

> **Para mais informações:**  
> Veja
>
a [documentação oficial do Spotify sobre Redirect URIs](https://developer.spotify.com/documentation/web-api/concepts/redirect_uri)
> para detalhes completos.

---

## Próximos Passos

✅ Sua conta de desenvolvedor está pronta.  
✅ Edite seu arquivo `.env` com os valores corretos de *Client ID*, *Client Secret* e *Redirect URI*, então execute o
script para começar a exportar suas playlists.

---

## Aviso

Suas credenciais de app Spotify Developer são pessoais.  
Não compartilhe seu Client Secret publicamente nem o submeta ao controle de versão.

## Aviso de marca registrada

Spotify é uma marca registrada da Spotify AB.  
Este projeto **não é afiliado, patrocinado ou endossado pelo Spotify** de nenhuma forma.  
Todas as referências ao Spotify são feitas apenas para fins informativos e educacionais.

Qualquer captura de tela ou imagem usada nesta documentação tem caráter meramente ilustrativo para auxiliar os usuários
na configuração de sua conta de desenvolvedor e não implica qualquer associação com a Spotify AB.
