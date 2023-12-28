import asyncclick as click
from templative.lib.create import componentCreator
from templative.lib.stockComponentInfo import STOCK_COMPONENT_INFO

@click.group()
async def stock():
    """Create a Stock Part"""
    pass

@stock.command()
@click.option("-n", "--name", default=None, help="The name of the new component.")
@click.option("-i", "--id", default=None, help="The ID of the stockpart.")
@click.option("-i", "--input", default="./", help="The path to the Templative Project.")
async def part(name, id):
    """Create a Stock Part by ID"""

    if name == None:
        print("Missing --name or -n defining the component name.")
        return

    if id == None:
        print("Missing --id or -i defining the stock part id.")
        return

    await componentCreator.createStockComponent(name, id)

@stock.command()
async def options():
    """Show avaiable stock parts"""
    partNames = ""
    for key in STOCK_COMPONENT_INFO.keys():
        partNames = partNames + key + "\n"
    print(partNames)
