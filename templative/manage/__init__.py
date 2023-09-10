from os import path
import asyncclick as click

from templative.manage import componentQuantitiesProcessor, depthCalculator
from templative.manage.rules import rules

@click.command()
@click.option('--input', default="./", required=False, help='The directory of the templative project.')
async def components(input):
    """Get a list of quantities of the game in the current directory"""
    await componentQuantitiesProcessor.listComponentQuantities(input)

@click.command()
@click.option('--input', default="./", required=False, help='The directory of the templative project.')
async def depth(input):
    """Get the depth of all components"""
    await depthCalculator.calculateComponentsDepth(input)

