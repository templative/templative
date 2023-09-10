import asyncclick as click
from templative import manage, produce, create
from templative.distribute import playground, zettelkasten, printout, gameCrafter, animation 
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
cli.add_command(animation.shear)

cli.add_command(create.init)
cli.add_command(produce.produce)
cli.add_command(manage.depth)
cli.add_command(manage.components)

cli.add_command(manage.rules)
cli.add_command(create.create)
cli.add_command(zettelkasten.zk)
cli.add_command(printout.printout)
cli.add_command(playground.playground)