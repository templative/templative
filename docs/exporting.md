## Getting necessary files


## Creating a whl
- `pipenv uninstall --all`
- `pipenv install`
- `pipenv requirements > requirements.txt`
- Move these requirements to `pyproject.toml`
- `python -m pip install --upgrade build --user`
- `python -m build --outdir "../templative-electron/python/dependencies"`

## Exporting server

- `pyinstaller -y --onefile ./templative/__main__.py --hidden-import engineio.async_drivers.aiohttp --hidden-import engineio.async_aiohttp`

Do we need `--collect-all templative`?

https://www.electronforge.io/config/makers/zip
https://packaging.python.org/en/latest/tutorials/packaging-projects/#generating-distribution-archives