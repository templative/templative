import asyncclick as click
from templative import gameManager

@click.command()
@click.option("-n", "--name", default=None, help="The name of the new component.")
@click.option("-i", "--id", default=None, help="The ID of the stockpart.")
async def stockpart(name, id):
    """Create a Stock Part by ID"""

    if name == None:
        print("Missing --name or -n defining the component name.")
        return

    if id == None:
        print("Missing --id or -i defining the stock part id.")
        return

    await gameManager.createStockComponent(name, id)
