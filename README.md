# Tyrus Card Pipeline

Define the cards you’d like created, use the CLI, and purchase the game off of the Game Crafter. Cards are assembled from svg templates.

## Install

### To Keep
`pip install .`

### To Develop
`python setup.py develop`

## Usage

- Create an account on the (Game Crafter)["https://www.thegamecrafter.com]
- Get an api key from the (Game Crafter)[https://www.thegamecrafter.com/account/apikeys]
- Add the THEGAMECRAFTER_PUBLIC_KEY, THEGAMECRAFTER_USERNAME, and THEGAMECRAFTER_PASSWORD to your env vars
- Clone and cd into `tyrus-pipeline-cli`
- `pip install .` to add `tyruspipeline` to your path.
- Clone and cd into `apcw-defines`
- `tyruspipeline produce -u` to create a version of the game and upload it. Remove `-u` to simple produce the game without uploading it.

Use `tyruspipeline --help` for more info.