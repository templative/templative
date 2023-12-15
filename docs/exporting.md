## Getting necessary files

- `pipenv uninstall --all`
- `pipenv install`
- `pipenv requirements > requirements.txt`
- Move these requirements to `pyproject.toml`
- `python -m pip install --upgrade build --user`
- `python -m build`
- Copy the `/dist` files to the lib folder of `templative-frontend`

https://www.electronforge.io/config/makers/zip
https://packaging.python.org/en/latest/tutorials/packaging-projects/#generating-distribution-archives