# Simple Blob Storage com Flask

Este projeto implementa um simples blob storage usando Flask no Linux. Ele permite o upload, download e listagem de arquivos e pastas através de URLs específicas. O projeto é containerizado usando Docker.

## Funcionalidades

- **Upload de Arquivos**: Envie arquivos para o storage através de uma URL.
- **Download de Arquivos**: Baixe arquivos do storage usando um URL de download.
- **Listagem de Arquivos/Pastas**: Liste arquivos e/ou pastas com base em um prefixo de caminho, incluindo metadados como tamanho, última modificação e tipo.

## Como Executar

### Pré-requisitos

- Docker

### Construir e Executar o Container

1. Clone o repositório:
   ```bash
   git clone [URL_DO_REPOSITÓRIO]
   cd [NOME_DO_REPOSITÓRIO]
   ```

2. Construa a imagem Docker:
   ```bash
   docker build -t blob-storage-flask .
   ```

3. Execute o container:
   ```bash
   docker run -p 5000:5000 blob-storage-flask
   ```

A aplicação estará rodando em: `http://localhost:5000/`

## Uso

### Upload de Arquivos

- **URL**: POST `http://localhost:5000/upload/<path:path>`
- **Form Data**: `'file': [Arquivo a ser enviado]`

### Download de Arquivos

- **URL**: GET `http://localhost:5000/download/<path:path>`

### Listagem de Arquivos/Pastas

- **URL**: GET `http://localhost:5000/list`
- **Query Params**:
  - `path_prefix`: Prefixo do caminho para listar.
  - `files`: `true` para listar arquivos.
  - `folders`: `true` para listar pastas.

## Tecnologias Utilizadas

- Python
- Flask
- Docker