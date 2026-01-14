.PHONY: setup run test clean

setup:
	python3 -m venv venv
	. venv/bin/activate && pip install -r requirements.txt

run:
	. venv/bin/activate && uvicorn app.main:app --reload

test:
	. venv/bin/activate && pytest

clean:
	rm -rf venv
	rm -f employees.db
	rm -rf __pycache__
