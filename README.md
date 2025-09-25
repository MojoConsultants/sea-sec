# SEA-SEQ — Shift-Left Endpoint Assurance & Security

**SEA-SEQ** is a fast, language-agnostic **API testing and security validation runner**.
It combines **OpenAPI contract validation**, **functional tests**, **coverage tracking**, and **lightweight security checks** into one CI-ready tool.

---

## Why SEA-SEQ?

* 🔧 **Language-agnostic**: Write suites in YAML — no SDK lock-in.
* 📜 **Contract validation**: Enforce responses against OpenAPI (status, headers, body schemas).
* 📈 **Coverage reports**: Track which paths and methods in your OpenAPI spec are tested.
* ⚡ **Parallel execution**: Run scenarios concurrently; stop early with **fail-fast**.
* 🪝 **Hooks**: Plug in Go, Python, or shell scripts for token injection, scrubbing, or pentest scans.
* 🛡️ **Security checks**: Extend test steps with pentest configs (headers, ports, TLS).
* 📦 **CI-ready**: Emit JUnit, JSON, HTML, and coverage artifacts for Jenkins, CircleCI, GitHub Actions.

---

## Quickstart

### 1. Build the CLI

```bash
go build -o seaseq ./cmd/sea-qa
```

> Requires Go 1.21+ (tested with 1.22).

### 2. Define environment variables

Example: `tests/examples/jsonplaceholder/env.json`

```json
{
  "BASE_URL": "https://jsonplaceholder.typicode.com"
}
```

### 3. Write a suite

Example: `tests/examples/jsonplaceholder/suite.yaml`

```yaml
name: JSONPlaceholder — SEA-SEQ Demo
openapi: tests/examples/jsonplaceholder/openapi.json

scenarios:
  - name: List posts
    steps:
      - request:
          method: GET
          url: ${BASE_URL}/posts?userId=1
          headers: { Accept: application/json }
        expect:
          - type: status
            value: 200
          - type: contract
            value: true
```

### 4. Run

```bash
./seaseq \
  --spec tests/examples/jsonplaceholder/suite.yaml \
  --env  tests/examples/jsonplaceholder/env.json \
  --openapi tests/examples/jsonplaceholder/openapi.json \
  --out reports -v --parallel 4
```

Artifacts:

* `reports/report.html`
* `reports/results.json`
* `reports/junit.xml`
* `reports/coverage.json`

---

## Security Extensions

SEA-SEQ supports embedding lightweight pentests into your test runs.

### Example Pentest Config (`pentest.yaml`)

```yaml
targets:
  - 127.0.0.1
  - example.com
ports: [22, 80, 443]
http_checks:
  missing_headers:
    - Strict-Transport-Security
    - Content-Security-Policy
    - X-Frame-Options
```

### Example Suite with Security Hook

```yaml
name: Demo Suite with SecTest
openapi: ./openapi.yaml

scenarios:
  - name: Health check + pentest
    steps:
      - hooks:
          - when: before
            process: ["python3", "security/pentest_runner.py", "--config", "configs/pentest.yaml", "--out", "reports/sec-findings.json"]
        request:
          method: GET
          url: ${BASE_URL}/health
          headers: { Accept: application/json }
        expect:
          - { type: status, value: 200 }
          - { type: contract, value: true }
```

---

## Suite Format

* **Variables**: `${KEY}` from `--env` JSON files.
* **Timeouts**: Use `timeout_ms` (snake\_case).
* **Tag filtering**: `--include-tags smoke` / `--exclude-tags flaky`.

---

## CI/CD Examples

### GitHub Actions

`.github/workflows/seaseq.yml`

```yaml
name: SEA-SEQ

on:
  push:
    branches: [ main, master ]
  pull_request:

jobs:
  run:
    runs-on: ubuntu-latest
    env:
      SPEC: tests/examples/jsonplaceholder/suite.yaml
      OPENAPI: tests/examples/jsonplaceholder/openapi.json
      ENVFILE: tests/examples/jsonplaceholder/env.json
      OUTDIR: reports
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-go@v5
        with:
          go-version: '1.22'
      - uses: actions/cache@v4
        with:
          path: |
            ~/go/pkg/mod
            ~/.cache/go-build
          key: ${{ runner.os }}-go-${{ hashFiles('**/go.sum') }}
          restore-keys: |
            ${{ runner.os }}-go-
      - run: go build -o seaseq ./cmd/sea-qa
      - run: |
          ./seaseq \
            --spec "$SPEC" \
            --openapi "$OPENAPI" \
            --env "$ENVFILE" \
            --out "$OUTDIR" \
            --parallel 4 -v
      - if: always()
        uses: actions/upload-artifact@v4
        with:
          name: seaseq-reports
          path: reports/
```

---

### Jenkins

`Jenkinsfile`

```groovy
pipeline {
  agent any

  options {
    timestamps()
    ansiColor('xterm')
  }

  environment {
    GO111MODULE = 'on'
    GOCACHE     = "${WORKSPACE}@tmp/go-build"
    GOMODCACHE  = "${WORKSPACE}@tmp/go-mod"
    SPEC        = 'tests/examples/jsonplaceholder/suite.yaml'
    OPENAPI     = 'tests/examples/jsonplaceholder/openapi.json'
    ENVFILE     = 'tests/examples/jsonplaceholder/env.json'
    OUTDIR      = 'reports'
  }

  stages {
    stage('Checkout') { steps { checkout scm } }

    stage('Build CLI') {
      steps {
        sh 'go mod download'
        sh 'go build -o seaseq ./cmd/sea-qa'
      }
    }

    stage('Run SEA-SEQ') {
      steps {
        sh '''
          ./seaseq \
            --spec "${SPEC}" \
            --openapi "${OPENAPI}" \
            --env "${ENVFILE}" \
            --out "${OUTDIR}" \
            --parallel 4 -v
        '''
      }
    }
  }

  post {
    always {
      junit allowEmptyResults: true, testResults: 'reports/junit.xml'
      archiveArtifacts artifacts: 'reports/**', fingerprint: true
      // publishHTML plugin can display report.html:
      // publishHTML(target: [reportDir: 'reports', reportFiles: 'report.html', reportName: 'SEA-SEQ Report', keepAll: true])
    }
  }
}
```

---

### CircleCI

`.circleci/config.yml`

```yaml
version: 2.1

jobs:
  seaseq:
    docker:
      - image: cimg/go:1.22
    environment:
      SPEC: tests/examples/jsonplaceholder/suite.yaml
      OPENAPI: tests/examples/jsonplaceholder/openapi.json
      ENVFILE: tests/examples/jsonplaceholder/env.json
      OUTDIR: reports
    steps:
      - checkout
      - restore_cache:
          keys:
            - go-mod-{{ checksum "go.sum" }}
            - go-mod-
      - run: go mod download
      - save_cache:
          key: go-mod-{{ checksum "go.sum" }}
          paths: [~/go/pkg/mod]
      - run: go build -o seaseq ./cmd/sea-qa
      - run: |
          ./seaseq \
            --spec "$SPEC" \
            --openapi "$OPENAPI" \
            --env "$ENVFILE" \
            --out "$OUTDIR" \
            --parallel 4 -v
      - store_test_results: { path: reports }
      - store_artifacts: { path: reports, destination: reports }

workflows:
  seaseq:
    jobs: [seaseq]
```

---
# Site Metadata Crawler

This project includes a Python crawler that collects metadata (title, description, keywords, robots) from all pages of a given website, along with the hosting IP address. Results are saved into a CSV file for analysis or Six Sigma STTS tracking.

---


# Site Metadata Crawler

[![codecov](https://codecov.io/gh/MojoConsultants/sea-sec/branch/main/graph/badge.svg)](https://codecov.io/gh/MojoConsultants/sea-sec)


## 🚀 Setup Instructions

### 1. Clone the Repository
```bash
gh repo clone MojoConsultants/sea-sec
cd sea-sec

## Contributing

PRs welcome! Before submitting:

1. Run `go fmt ./... && go test ./...`.
2. Add/update fixtures under `tests/examples/*`.
3. Update this README if your change affects behavior.

---

## License

**Apache License 2.0** — see [`LICENSE`](LICENSE).

---


