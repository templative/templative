import asyncclick as click
import os, sys
from templative import gameManager, playground, zettelkasten, printout, rules, commands, gameCrafter, animation

def find_executable(executable):
    """Tries to find 'executable' in the directories listed in 'path'.

    A string listing directories separated by 'os.pathsep'; defaults to
    os.environ['PATH'].  Returns the complete filename or None if not found.
    """
    _, ext = os.path.splitext(executable)
    if (sys.platform == 'win32') and (ext != '.exe'):
        executable = executable + '.exe'

    if os.path.isfile(executable):
        return executable

    path = os.environ.get('PATH', None)
    if path is None:
        try:
            path = os.confstr("CS_PATH")
        except (AttributeError, ValueError):
            # os.confstr() or CS_PATH is not available
            path = os.defpath
        
    return None

if not find_executable("inkscape"):
    print("Install inkscape.")
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