from templative.lib.manage import instructionsLoader
from templative.lib.distribute.playground import getPlaygroundDirectory, writePlaygroundFile, convertToTabletopPlayground
import asyncclick as click

@click.command()
@click.option('-i', '--input', default=None, help='The directory of the produced game. Defaults to last produced directory.')
@click.option('-o', '--output', default=None, help='The Tabletop Playground packages directory. Such as "~/Library/Application Support/Epic/TabletopPlayground/Packages" or "C:\Program Files (x86)\Steam\steamapps\common\TabletopPlayground\TabletopPlayground\PersistentDownloadDir"')
async def playground(input, output):
    """Convert a produced game into a tabletop playground game"""    
    if input is None:
        input = await instructionsLoader.getLastOutputFileDirectory()

    playgroundDirectory = await getPlaygroundDirectory(output)
    if playgroundDirectory == None:
        print("Missing --output directory.")
        return
    await writePlaygroundFile(playgroundDirectory)

    return await convertToTabletopPlayground(input, playgroundDirectory)
