run:
	python src/main.py
env:
	conda env export > environment.yml
	pip freeze > requirements.txt
