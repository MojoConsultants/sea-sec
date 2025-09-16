build:
	go build -o seaseq ./cmd/sea-qa

test:
	go test ./...

run:
	./seaseq --spec tests/examples/jsonplaceholder/suite.yaml \
	         --env tests/examples/jsonplaceholder/env.json \
	         --openapi tests/examples/jsonplaceholder/openapi.json \
	         --out reports -v
