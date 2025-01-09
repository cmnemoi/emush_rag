# Ask NERON API

[![Continuous Integration](https://github.com/cmnemoi/emush_rag/actions/workflows/continuous_integration.yaml/badge.svg)](https://github.com/cmnemoi/emush_rag/actions/workflows/continuous_integration.yaml)
[![Continuous Delivery](https://github.com/cmnemoi/emush_rag/actions/workflows/create_github_release.yaml/badge.svg)](https://github.com/cmnemoi/emush_rag/actions/workflows/create_github_release.yaml)
[![codecov](https://codecov.io/gh/cmnemoi/emush_rag/graph/badge.svg?token=FLAARH38AG)](https://codecov.io/gh/cmnemoi/emush_rag)

A RAG-based API to answer questions about [eMush](https:/emush.eternaltwin.org/) using curated data.

Stack: 
- [FastAPI](https://fastapi.tiangolo.com/) for the API ;
- [Chroma](https://www.trychroma.com/) for the vector database allowing document retrieval ;
- [Docker Swarm](https://docs.docker.com/engine/swarm/) for deployment on a self-managed [Digital Ocean server](https://www.digitalocean.com/products/droplets/) : https://askneron.com/docs

# Contributing

## Prerequisites

- [curl](https://curl.se/)
- [Docker Compose](https://docs.docker.com/compose/install/)
- [make](https://www.gnu.org/software/make/)
- [uv](https://docs.astral.sh/uv/getting-started/installation/)

## Installation

- Run the following command: `curl -sSL https://raw.githubusercontent.com/cmnemoi/emush_rag/main/clone-and-install | bash`
- Add an OpenAI API key to the `.env` file.

## Usage

You can now ask questions to the API by running the following command:

```bash
curl -X POST "http://askneron.localhost/api/questions" \
     -H "Content-Type: application/json" \
     -d '{
           "question": "Do mycoalarms detect spore extraction?",
           "chat_history": []
         }'
```

Or by accessing the API Swagger at http://askneron.localhost/docs.

## Indexing new documents

To improve the answer of the RAG model, you can new documents by putting them in the `data` directory and then running the following command:

```bash
make index-documents
```

## Development

- Lint code with `make lint`.
- Run tests with `make test`.

# License

The source code of this repository is licensed under the [AGPL-3.0-or-later License](LICENSE).