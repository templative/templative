import asyncclick as click
from templative.produce import gameProducer

@click.command()
@click.option('--name', default=None, help='The component to produce.')
@click.option('-s/-c', '--simple/--complex', default=False, required=False, type=bool, help='Whether complex information is shown. Used for videos.')
@click.option('-p/-d', '--publish/--debug', default=False, required=False, type=bool, help='Where debug information is included.')
@click.option('--language', default="en", required=False, help='Target language of the output. https://developers.google.com/admin-sdk/directory/v1/languages')
@click.option('--input', default="./", required=False, help='The directory of the templative project.')
async def produce(name, simple, publish, language, input):
    """Produce the game in the current directory"""
    return await gameProducer.produceGame(input, name, simple, publish, language)
