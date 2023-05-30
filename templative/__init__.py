import asyncclick as click
import os, sys
from templative import gameManager, playground, zettelkasten, printout, rules, commands, gameCrafter, animation
import distutils.spawn

if distutils.spawn.find_executable("inkscape") == None:
    print("Missing inkscape.")
    exit() 

@click.group()
async def cli():
    """Templative CLI"""
    pass


cli.add_command(gameCrafter.upload)
cli.add_command(gameCrafter.list)
cli.add_command(gameCrafter.deletegames)

cli.add_command(animation.animation)

cli.add_command(gameManager.init)
cli.add_command(gameManager.produce)
cli.add_command(gameManager.depth)
cli.add_command(gameManager.components)

cli.add_command(rules.rules)
cli.add_command(commands.create)
cli.add_command(zettelkasten.zk)
cli.add_command(printout.printout)
cli.add_command(playground.playground)