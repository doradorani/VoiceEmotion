formatting:
	isort . && oitnb --exclude=migrations . && flake8 --ignore=E501 --exclude=migrations