import asyncclick as click
from templative.cli import create
from templative.cli.distribute import zettelkastenCommands 
from templative.cli.distribute import animationCommands
from templative.cli.distribute import gameCrafterCommands
from templative.cli.distribute import playgroundCommands
from templative.cli.distribute import printoutCommands
from templative.cli.manage import componentAnalysisCommands
from templative.cli.manage import rulesCommands
from templative.cli import produce
from templative.cli import server

@click.group()
async def cli():
    """Templative CLI"""
    pass

cli.add_command(gameCrafterCommands.upload)
cli.add_command(gameCrafterCommands.list)
cli.add_command(gameCrafterCommands.deletegames)
cli.add_command(gameCrafterCommands.stocklist)
cli.add_command(gameCrafterCommands.customlist)

cli.add_command(animationCommands.animation)

cli.add_command(create.init)
cli.add_command(server.serve)
cli.add_command(produce.produce)
cli.add_command(componentAnalysisCommands.depth)
cli.add_command(componentAnalysisCommands.components)

cli.add_command(rulesCommands.rules)
cli.add_command(create.create)
cli.add_command(zettelkastenCommands.zk)
cli.add_command(printoutCommands.printout)
cli.add_command(playgroundCommands.playground)