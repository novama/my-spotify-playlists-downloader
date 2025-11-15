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
- **Exporta músicas curtidas** (coleção de faixas salvas).
- Opção para **dividir a exportação** em arquivos JSON individuais por playlist.
- **Combinações flexíveis de exportação** (músicas curtidas e/ou playlists).
- **Geração de relatório HTML** com design moderno e responsivo mostrando estatísticas e caminhos dos arquivos.
- Inclui **posição da faixa na playlist**, usuário que adicionou e data de adição.
- **Logging** no console e em arquivo para rastreabilidade.
- **Portável** – funciona no Windows, macOS e Linux.
- Configuração simples com dependências mínimas.

---

## Guia Passo a Passo para Começar

Siga estes passos para configurar e usar a ferramenta. Não se preocupe se você não está familiarizado com programação – vou te guiar em tudo.

### Passo 1: Verificar a Instalação do Python

Primeiro, certifique-se de ter Python instalado no seu computador.

**Verificar se o Python está instalado:**

Abra seu terminal (Prompt de Comando no Windows, Terminal no Mac/Linux) e digite:

```shell
python --version
```

Você deve ver algo como `Python 3.10.x` ou superior. Se você vir um erro ou uma versão inferior a 3.10, você precisa instalar ou atualizar o Python:

- **Baixar Python:** Visite [python.org/downloads](https://www.python.org/downloads/) e baixe Python 3.10 ou mais recente.
- **Durante a instalação:** Certifique-se de marcar a caixa que diz "Add Python to PATH" (Adicionar Python ao PATH).

### Passo 2: Configurar uma Conta de Desenvolvedor Spotify

Para acessar seus dados do Spotify, você precisa criar uma conta de desenvolvedor Spotify e obter credenciais especiais (como chaves para acessar sua conta).

**Siga este guia detalhado:** [SPOTIFY_DEVELOPER_SETUP.md](SPOTIFY_DEVELOPER_SETUP.md)

Este guia explicará:

- Criar uma conta de desenvolvedor Spotify (é grátis!)
- Criar um aplicativo no Painel do Spotify
- Obter seu **Client ID** e **Client Secret**
- Configurar a **Redirect URI**

**Importante:** Mantenha seu Client ID e Client Secret em mãos – você precisará deles nos próximos passos!

### Passo 3: Baixar o Script

#### Opção A: Baixar como ZIP (mais fácil para iniciantes)

Nesta página do repositório GitHub, vá para o topo e:

1. Clique no botão verde "Code"
2. Selecione "Download ZIP"
3. Extraia o arquivo ZIP para uma pasta no seu computador (ex. `Documentos/spotify-downloader`)

#### Opção B: Usando Git (se você tiver Git instalado)

Abra seu terminal e execute:

```shell
git clone https://github.com/novama/my_spotify_playlists_downloader.git
cd my_spotify_playlists_downloader
```

### Passo 4: Instalar as Dependências Necessárias

O script precisa de alguns pacotes Python adicionais para funcionar. Vamos instalá-los.

1. **Abra seu terminal** e navegue até a pasta onde você extraiu/clonou o script:

   ```shell
   cd caminho/para/my_spotify_playlists_downloader
   ```

   Substitua `caminho/para/` pela localização real (ex. `cd Downloads/spotify-downloader`).

2. **Instalar dependências:**

   ```shell
   pip install -r requirements.txt
   ```

   Aguarde a conclusão da instalação. Você verá mensagens indicando que os pacotes estão sendo instalados.

### Passo 5: Configurar suas Credenciais

Agora você precisa informar ao script suas credenciais do Spotify.

1. **Encontre o arquivo `.env.example`** na pasta do script.

2. **Faça uma cópia e renomeie para `.env`** (sem a parte `.example`):

   - **Windows:** Clique com o botão direito no arquivo → "Copiar" → Colar → Renomear para `.env`
   - **Mac/Linux:** No terminal, execute: `cp .env.example .env`

3. **Abra o arquivo `.env`** com um editor de texto (Bloco de Notas no Windows, TextEdit no Mac, ou qualquer editor de código).

4. **Preencha suas credenciais** do Passo 2:

   ```env
   SPOTIFY_CLIENT_ID=seu_client_id_aqui
   SPOTIFY_CLIENT_SECRET=seu_client_secret_aqui
   SPOTIFY_REDIRECT_URI=http://127.0.0.1:8000/callback
   ```

   Substitua `seu_client_id_aqui` e `seu_client_secret_aqui` pelos valores reais do seu Painel de Desenvolvedor Spotify.

   **Importante:** A `SPOTIFY_REDIRECT_URI` deve corresponder exatamente ao que você configurou nas configurações do seu aplicativo Spotify!

5. **Configurações opcionais** (você pode deixá-las padrão ou personalizá-las):

   ```env
   OUTPUT_DIR=./output
   LOG_LEVEL=INFO
   ```

6. **Salve o arquivo** e feche-o.

### Passo 6: Execute sua Primeira Exportação

Agora você está pronto para exportar suas playlists. Aqui estão alguns cenários comuns:

#### Exportação Básica: Todas as Playlists

Exporte todas as suas playlists para um único arquivo JSON:

```shell
python my_spotify_playlists_downloader.py
```

**O que acontece:**

- Uma janela do navegador será aberta pedindo para você fazer login no Spotify (apenas na primeira vez)
- Após autorizar o aplicativo, suas playlists serão exportadas
- Os arquivos serão salvos na pasta `output` (ou onde você especificou no `.env`)

#### Exportar Tudo com um Relatório Bonito

Exporte todas as playlists E músicas curtidas, com um belo relatório HTML:

```shell
python my_spotify_playlists_downloader.py --all_playlists --liked_songs --html_report
```

**O que você obtém:**

- Todas as suas playlists exportadas como arquivos JSON
- Suas músicas curtidas exportadas em um arquivo JSON separado
- Um belo relatório HTML que você pode abrir no seu navegador com estatísticas e localizações de arquivos

#### Exportar Cada Playlist como Arquivos Separados

Mantenha cada playlist em seu próprio arquivo:

```shell
python my_spotify_playlists_downloader.py --split
```

#### Exportar Apenas suas Músicas Curtidas

Exporte apenas suas faixas salvas:

```shell
python my_spotify_playlists_downloader.py --liked_songs
```

#### Exportar uma Playlist Específica

Exporte apenas uma playlist por nome:

```shell
python my_spotify_playlists_downloader.py --playlist_name "Minha Playlist Favorita"
```

Substitua `"Minha Playlist Favorita"` pelo nome real da sua playlist.

#### Início Limpo (Excluir Exportações Antigas Primeiro)

Exclua exportações antigas antes de criar novas:

```shell
python my_spotify_playlists_downloader.py --clean_output --all_playlists --html_report
```

#### O Pacote Completo (Recomendado!)

Exporte tudo com todos os recursos habilitados:

```shell
python my_spotify_playlists_downloader.py --split --all_playlists --liked_songs --html_report --clean_output
```

Isso irá:

1. Excluir arquivos de exportação antigos (início limpo)
2. Exportar cada playlist como um arquivo JSON separado
3. Exportar suas músicas curtidas
4. Gerar um belo relatório HTML
5. Mostrar exatamente onde tudo foi salvo

---

## Entendendo as Opções

Aqui está o que cada opção faz:

| Opção | O Que Faz |
|--------|-----------|
| `--split` | Cria arquivos JSON separados para cada playlist (em vez de um arquivo grande) |
| `--liked_songs` | Exporta sua coleção de músicas curtidas/salvas |
| `--all_playlists` | Exporta todas as playlists (use com `--liked_songs` para exportar tudo) |
| `--html_report` | Cria um belo relatório HTML com estatísticas e localizações de arquivos |
| `--clean_output` | Exclui arquivos JSON e HTML antigos antes de exportar novos |
| `--playlist_name "Nome"` | Exporta apenas a playlist com este nome específico |
| `--output_dir ./pasta` | Salva os arquivos em uma pasta específica |

**Dica:** Você pode combinar várias opções, apenas adicione-as uma após a outra, separadas por espaços.

---

## Notas adicionais

- Os nomes das playlists usados como nomes de arquivos são sanitizados: caracteres inválidos e emojis são removidos, mas
  acentos e maiúsculas/minúsculas originais são mantidos.
- Ao usar `--playlist_name`, o script registra o filtro normalizado e a quantidade de playlists a serem exportadas.
- Ao usar `--clean_output`, o script registra cada arquivo excluído (JSON e HTML) e confirma a limpeza da pasta.
- O comportamento padrão exporta apenas playlists. Use `--liked_songs` para músicas curtidas ou `--all_playlists` para ambos.
- Você pode usar `--liked_songs` e `--playlist_name` juntos para exportar uma playlist específica junto com suas músicas curtidas.
- O relatório HTML (`--html_report`) inclui os caminhos dos arquivos para cada playlist exportada e para as músicas curtidas.

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
