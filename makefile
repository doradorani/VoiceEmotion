python:
	isort . && oitnb --exclude=migrations . && flake8 --ignore=E501 --exclude=migrations

html:
	prettier --bracket-same-line --write --print-width 240 .

backend:
	cd backend; python app.py

django:
	@echo "Not yet finished"
