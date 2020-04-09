python-dependencies:
	pipenv --rm
	pipenv lock 
	pipenv sync 
	pipenv run pip3 freeze | sed s/=.*// > .freeze
	pipenv run pip3 install homebrew-pypi-poet
	pipenv run xargs poet -s < .freeze > .python-resources
	rm .freeze
	pipenv --rm 

poet-depend:
	pipenv run pip3 install $(package)
	pipenv run pip3 freeze | sed s/=.*// > .freeze
	pipenv run pip3 install homebrew-pypi-poet
	pipenv run xargs -t poet -s < .freeze
	rm .freeze
	pipenv --rm 

full-depend:
	pipenv run pip3 install $(package)
	pipenv run pip3 freeze | sed s/=.*// > .freeze
	pipenv run pip3 install homebrew-pypi-poet
	pipenv run poet -f $(package)
	rm .freeze
	pipenv --rm 

brew-clean:
	# brew tap beeftornado/rmtree
	brew rmtree templative
	brew rmtree imagemagick
	brew rmtree pango
	brew rmtree cairo

pip-clean:
	# pip install pip-autoremove
	pip-autoremove templative -y

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
	
pipdevelop:
	pipenv --rm
	pipenv sync 
	pipenv run python3 setup.py develop
	pipenv run pip3 install -e .

pipundevelop:
	pipenv run python3 setup.py develop --uninstall
	pipenv --rm

develop:
	python3 setup.py develop
	pip3 install -e .

undevelop:
	python3 setup.py develop --uninstall

suite: develop test undevelop

clean:
	rm -rf dist/
	rm -rf build/
	rm -rf *.egg-info/
	find . -name '*.pyc' -delete

release: clean
	pipenv run python3 setup.py sdist
	pipenv run twine upload dist/*b
	rm -fr build dist .egg requests.egg-info


