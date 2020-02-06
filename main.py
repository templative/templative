import click
import tcgClient

@click.command()
def createTemplate():
    print(tcgClient.login())

if __name__ == '__main__':
    createTemplate()