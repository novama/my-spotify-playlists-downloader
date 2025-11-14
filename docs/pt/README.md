# My Spotify Playlists Downloader

Exporta as informações das suas playlists do Spotify para arquivos JSON, para backup, análise ou migração.

---

## Descrição

`my_spotify_playlists_downloader.py` é um script Python de linha de comando desenvolvido para ajudar você a exportar e
fazer backup das suas playlists do Spotify. Ele se conecta à sua conta Spotify via OAuth e recupera todas as suas
playlists junto com metadados detalhados de cada faixa. Você pode exportar as playlists como um único arquivo JSON
consolidado ou como arquivos JSON individuais por playlist.

Este script é ideal para:

- Fazer backup dos dados da sua biblioteca musical.
- Preparar a migração para outro serviço de música.
- Analisar suas playlists para uso pessoal ou pesquisa.
- Aprender como integrar com a Web API do Spotify usando Python.

O projeto é publicado sob a licença MIT e destinado a uso educacional e pessoal.

---

## Funcionalidades

- Exporta **todas as playlists e metadados das faixas**, incluindo nome, artistas, álbum, data de lançamento e mais.
- Opção para **dividir a exportação** em arquivos JSON individuais por playlist.
- Inclui **posição da faixa na playlist**, usuário que adicionou e data de adição.
- **Logging** no console e em arquivo para rastreabilidade.
- **Portável** – funciona no Windows, macOS e Linux.
- Configuração simples com dependências mínimas.

---

## Requisitos

- Python 3.10 ou superior
- Uma [conta de desenvolvedor Spotify](SPOTIFY_DEVELOPER_SETUP.md) para criar um aplicativo e obter seu Client ID e
  Client Secret

Instale as dependências com:

```shell
pip install -r requirements.txt
```

---

## Configuração

1. **Clone o repositório**

    ```shell
    git clone https://github.com/yourusername/my_spotify_playlists_downloader.git
    cd my_spotify_playlists_downloader
    ```

2. **Crie seu arquivo `.env`**

   Copia el ejemplo proporcionado:

    ```shell
    cp .env.example .env
    ```

3. **Edite `.env` e defina suas variáveis**

   Mínimo necessário:

    - `SPOTIFY_CLIENT_ID`
    - `SPOTIFY_CLIENT_SECRET`
    - `SPOTIFY_REDIRECT_URI` (deve ser exatamente igual ao configurado no seu app Spotify,
      ex. <http://127.0.0.1:8000/callback>)

   Variáveis opcionais:

    - `OUTPUT_DIR`: Diretório onde os arquivos exportados serão salvos (default: ./playlists)
    - `OUTPUT_PREFIX_SPLIT`: Prefixo para arquivos exportados no modo dividido
    - `OUTPUT_PREFIX_SINGLE`: Prefixo para o arquivo único exportado
    - `LOG_DIR`: Diretório onde os logs serão armazenados (default: localização do script)
    - `LOG_LEVEL`: Nível de logging (default: INFO)

### Configuração da Conta de Desenvolvedor Spotify

Este script requer uma conta de desenvolvedor Spotify e credenciais de aplicativo registradas.
Veja [SPOTIFY_DEVELOPER_SETUP.md](SPOTIFY_DEVELOPER_SETUP.md) para instruções detalhadas.

---

## Uso

### Exportar todas as playlists para um único arquivo JSON (padrão)

```shell
python my_spotify_playlists_downloader.py
```

### Exportar cada playlist como um arquivo JSON individual

```shell
python my_spotify_playlists_downloader.py --split
```

### Especificar um diretório de saída customizado

```shell
python my_spotify_playlists_downloader.py --output_dir ./my_exports
```

### Exportar apenas uma playlist específica pelo nome

```shell
python my_spotify_playlists_downloader.py --playlist_name "Nome da minha playlist"
```

- O script exportará apenas a playlist cujo nome coincida (sem diferenciar maiúsculas/minúsculas, normalizado) com o
  valor fornecido.
- Se não houver correspondência, um erro será registrado e nenhum arquivo será exportado.

### Limpar a pasta de saída antes de exportar

```shell
python my_spotify_playlists_downloader.py --clean_output
```

- Todos os arquivos JSON na pasta de saída serão excluídos antes de exportar novas playlists.
- Útil para evitar misturar exportações antigas e novas.

### Combinar opções

Você pode combinar essas opções conforme necessário. Por exemplo, para limpar a pasta de saída e exportar apenas uma
playlist específica como arquivo individual:

```shell
python my_spotify_playlists_downloader.py --split --playlist_name "Nome da minha playlist" --clean_output
```

---

## Notas adicionais

- Os nomes das playlists usados como nomes de arquivos são sanitizados: caracteres inválidos e emojis são removidos, mas
  acentos e maiúsculas/minúsculas originais são mantidos.
- Ao usar --playlist_name, o script registra o filtro normalizado e a quantidade de playlists a serem exportadas.
- Ao usar --clean_output, o script registra cada arquivo excluído e confirma a limpeza da pasta.

---

## Exemplo de Saída

Cada objeto de playlist exportada inclui:

- Nome da playlist, ID, nome de exibição e username do proprietário, descrição, snapshot_id
- Lista de faixas com:
  - Posição na playlist
  - Nome da faixa, artistas, álbum, data de lançamento
  - URL do Spotify
  - Data de adição à playlist e usuário que adicionou

---

## Aviso

Este script é fornecido apenas para fins educacionais.
Use-o de forma responsável com sua própria conta Spotify.
O autor não assume qualquer responsabilidade por uso indevido ou perda de dados causada pelo seu uso.
O código é limpo e livre de componentes maliciosos.

## Aviso de marca registrada

Spotify é uma marca registrada da Spotify AB.
Este projeto **não é afiliado, patrocinado ou endossado pelo Spotify** de nenhuma forma.
Todas as referências ao Spotify são feitas apenas para fins informativos e educacionais.

Qualquer captura de tela ou imagem usada nesta documentação tem caráter meramente ilustrativo para auxiliar os usuários
na configuração de sua conta de desenvolvedor e não implica qualquer associação com a Spotify AB.

---

## Licença

Este projeto está licenciado sob a [Licença MIT](../../LICENSE).
