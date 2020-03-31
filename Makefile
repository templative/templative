python-dependencies:
	pipenv --rm
	pipenv lock 
	pipenv sync 
	pipenv run pip freeze | sed s/=.*// > .freeze
	pipenv run pip install homebrew-pypi-poet
	pipenv run xargs poet -s < .freeze > .python-resources
	rm .freeze
	pipenv --rm 

brew-dependencies:
	xargs brew deps --union < Brewfile > .brew-resources
	sed -i -e 's|\(.*\)|depends on "\1"|' .brew-resources
	
dependencies: brew-dependencies python-dependencies

	cat .brew-resources > .resources
	cat .python-resources >> .resources

	rm .brew-resources
	rm .python-resources

	echo "Created .resources for homebrew file"
	
develop:
	pipenv --rm
	pipenv sync 
	pipenv run python setup.py develop
	pipenv run pip install -e .

undevelop:
	pipenv run python setup.py develop --uninstall
	pipenv --rm

clean:
	rm -rf dist/
	rm -rf build/
	rm -rf *.egg-info/
	find . -name '*.pyc' -delete

release: clean
	pipenv run python setup.py sdist
	pipenv run twine upload dist/*b