# build dist
python setup.py sdist

# test on test pypi
twine upload --repository-url https://test.pypi.org/legacy/ dist/caddiepy-0.1.1.tar.gz

# upload to pypi
twine upload dist/caddiepy-0.1.1.tar.gz