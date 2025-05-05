all: generate-openapi

generate-openapi:
	source ./.venv/bin/activate && \
	python3 -c "from src.app.app import application; import json; open('openapi.json', 'w').write(json.dumps(application.openapi(), indent=2, ensure_ascii=False))" && \
	python3 -c "from src.app.app import application; import yaml; open('openapi.yaml', 'w').write(yaml.dump(application.openapi(), allow_unicode=True))"
	openapi-generator generate \
      -i openapi.json \
      -g python \
      -o api_client \
      --additional-properties=packageName=linter_api_client,setEnsureAsciiToFalse=true
