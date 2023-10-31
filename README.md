# Simple Blob Storage com Flask

Este projeto implementa um simples blob storage usando Flask no Linux. Ele permite o upload, download e listagem de arquivos e pastas através de URLs específicas. O projeto é containerizado usando Docker e Docker Compose.

## Funcionalidades

- **Upload de Arquivos**: Envie arquivos para o storage através de uma URL.
- **Download de Arquivos**: Baixe arquivos do storage usando um URL de download.
- **Listagem de Arquivos/Pastas**: Liste arquivos e/ou pastas com base em um prefixo de caminho, incluindo metadados como tamanho, última modificação e tipo.

## Como Executar

### Pré-requisitos

- Docker e Docker Compose

### Construir e Executar o Container com Docker Compose

1. Clone o repositório:
   ```bash
   git clone [URL_DO_REPOSITÓRIO]
   cd [NOME_DO_REPOSITÓRIO]
   ```

2. Use o Docker Compose para construir e executar o container:
   ```bash
   docker-compose up --build
   ```

A aplicação estará rodando em: `http://localhost:5000/`

## Uso

### Upload de Arquivos

- **URL**: POST `http://localhost:5000/upload`
- **Form Data**: `'file': [Arquivo a ser enviado]`
- **Query Params**:
  - `folder_path`: Caminho da pasta onde o arquivo será salvo.

### Download de Arquivos

- **URL**: GET `http://localhost:5000/get-file`
- **Query Params**:
  - `file_path`: Caminho do arquivo para download.

### Listagem de Arquivos/Pastas

- **URL**: GET `http://localhost:5000/list`
- **Query Params**:
  - `path_prefix`: Prefixo do caminho para listar.
  - `files`: `true` para listar arquivos.
  - `folders`: `true` para listar pastas.

## Tecnologias Utilizadas

- Python
- Flask
- Docker e Docker Compose
