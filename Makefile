python-dependencies:
	pipenv --rm
	pipenv lock 
	pipenv sync 
	pipenv run pip freeze | sed s/=.*// > .freeze
	pipenv run pip install homebrew-pypi-poet
	pipenv run xargs poet -s < .freeze > .python-resources
	rm .freeze
	pipenv --rm 

poet-depend:
	pipenv run pip install $(package)
	pipenv run pip freeze | sed s/=.*// > .freeze
	pipenv run pip install homebrew-pypi-poet
	pipenv run xargs -t poet -s < .freeze
	rm .freeze
	pipenv --rm 

brew-dependencies:
	# Creates duplicates of main brew packages
	xargs brew deps --union < Brewfile > .brew-resources
	cat Brewfile >> .brew-resources
	sed -i -e 's|\(.*\)|depends_on "\1"|' .brew-resources
	
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

test:
	pipenv run templative	
	pipenv run templative produce -d ~/apcw-defines -c protests

undevelop:
	pipenv run python setup.py develop --uninstall
	pipenv --rm

suite: develop test undevelop

clean:
	rm -rf dist/
	rm -rf build/
	rm -rf *.egg-info/
	find . -name '*.pyc' -delete

release: clean
	pipenv run python setup.py sdist
	pipenv run twine upload dist/*b

