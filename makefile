python:
	isort . && oitnb --exclude=migrations . && flake8 --ignore=E501 --exclude=migrations

html:
	prettier --bracket-same-line --write --print-width 240 .