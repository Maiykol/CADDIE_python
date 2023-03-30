# build dist
python setup.py sdist

# test on test pypi
python3 -m twine upload --repository-url https://test.pypi.org/legacy/ dist/caddiepy-0.2.5.tar.gz

# upload to pypi
python3 -m twine upload dist/caddiepy-0.2.5.tar.gz