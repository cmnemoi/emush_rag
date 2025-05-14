# CHANGELOG


## v0.1.1 (2025-05-14)

### Bug Fixes

- Update CORS middleware configuration
  ([`79efcb4`](https://github.com/cmnemoi/emush_rag/commit/79efcb407c77bca0de0730f341b49d7370ceb1ff))

- Restrict allowed origins to "https://askneron.netlify.app". - Add support for OPTIONS method and
  expose headers. - Set max age for preflight requests to 3600 seconds.

### Chores

- Allow to get started more easily
  ([`31b5ded`](https://github.com/cmnemoi/emush_rag/commit/31b5ded8794331e384ae0052a64c78f1c7cfd1c6))

- Add make commands to run the API with docker compose ; - Add a make command to index new documents
  in the vector store ; - Update README.

- Remove unused dependencies
  ([`8daa35f`](https://github.com/cmnemoi/emush_rag/commit/8daa35fdfdbaffd5448aa4429882543856c1189f))

- Update dependencies
  ([`466b7c2`](https://github.com/cmnemoi/emush_rag/commit/466b7c291849003891b1f7e8038be68bee527bd4))

### Documentation

- Fix broken link in README
  ([`fe1620c`](https://github.com/cmnemoi/emush_rag/commit/fe1620c0de57b0dade148897e32a0a0ed1bd1ab3))

- Update README with missing infos about stack and corrected typos
  ([`d30dd3f`](https://github.com/cmnemoi/emush_rag/commit/d30dd3fadee683f14dd0a0445ca3685f7006ad79))

### Refactoring

- Use config class to setup rate limiting
  ([`3c6a1a1`](https://github.com/cmnemoi/emush_rag/commit/3c6a1a10d312a17b5edce77b169179a1ce822c3b))


## v0.1.0 (2025-01-09)

### Features

- Add a version endpoint
  ([`34a83f4`](https://github.com/cmnemoi/emush_rag/commit/34a83f42b43346268fca31db8ad3eb5a1c7d5187))

- Implement rate limiting and update API to enforce limits
  ([`c525c78`](https://github.com/cmnemoi/emush_rag/commit/c525c786070e59add754255e7c65fb8b195f8986))


## v0.0.1 (2025-01-08)

### Bug Fixes

- Add Traefik reverse proxy configuration for HTTPS
  ([`9fe15c4`](https://github.com/cmnemoi/emush_rag/commit/9fe15c47ce4c1b07b830f47c6c201ee4cd2b961f))

- Allow CORS requests to the API
  ([`407157b`](https://github.com/cmnemoi/emush_rag/commit/407157b00f575dce8e741fb97d4cbce784f333a6))

### Chores

- First functional endpoint ([#3](https://github.com/cmnemoi/emush_rag/pull/3),
  [`89a910b`](https://github.com/cmnemoi/emush_rag/commit/89a910b11efce81e183ec0b65e2fa6f9adbb878e))

- Fix indentation in production Docker Compose file
  ([`91a4df2`](https://github.com/cmnemoi/emush_rag/commit/91a4df27d23638cd409facf3432ecdc65cd7a94b))

- Run Chroma vector store into a container
  ([`6bbae19`](https://github.com/cmnemoi/emush_rag/commit/6bbae1951eb45bc23ef336616065260cb42ecafb))

- Update dependencies
  ([`624c863`](https://github.com/cmnemoi/emush_rag/commit/624c86323d8b129999e2fb5517370b49e6107192))

- Update production Docker Compose to use overlay network and add volume for Chroma
  ([`b412bd2`](https://github.com/cmnemoi/emush_rag/commit/b412bd2b8e019c9b288e0a91b05a47de9f584d40))

### Continuous Integration

- Add Continous Delivery to deploy the API ([#1](https://github.com/cmnemoi/emush_rag/pull/1),
  [`893c5f4`](https://github.com/cmnemoi/emush_rag/commit/893c5f4f27780be04afc2aeb1f0ded9e5bb59ee4))

* chore: Add .dockerignore file

* chore: Add basic endpoint

* chore: Add Dockerfile and update .dockerignore for containerization

* ci: Add a workflow to build API Docker image

- Add OpenAI API key environment variable to production Docker Compose file
  ([#5](https://github.com/cmnemoi/emush_rag/pull/5),
  [`5a92b88`](https://github.com/cmnemoi/emush_rag/commit/5a92b88d84b4171c6e8529bcecf54b5852050f03))

- Update deployment script to include environment variables for OpenAI API key
  ([#4](https://github.com/cmnemoi/emush_rag/pull/4),
  [`7f600fc`](https://github.com/cmnemoi/emush_rag/commit/7f600fceb80fe124392200de7ec0e5f9bb93552c))

- Update deployment script to use secrets for environment variables in API deployment
  ([`c32d8c2`](https://github.com/cmnemoi/emush_rag/commit/c32d8c281838e259a0e45fe14d171a963ddd5388))

- Update deployment workflow to launch API on the server and add docker compose file
  ([#2](https://github.com/cmnemoi/emush_rag/pull/2),
  [`34e25d0`](https://github.com/cmnemoi/emush_rag/commit/34e25d0e4ce715993b7f3568e726371c76175b61))


## v0.0.0 (2024-12-24)
