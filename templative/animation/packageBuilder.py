import os
from templative.gameManager import instructionsLoader
from aiofile import AIOFile
import shutil

async def createPackage(input, output):
    instructions = await instructionsLoader.loadGameInstructions(input)
    gameVersionName = instructions["name"]

    print("Creating typescript package for %s." % gameVersionName)

    newPackageDirectoryPath = os.path.join(output, gameVersionName)
    await createOrReplacePackageDirectory(newPackageDirectoryPath)
    packageNames = await createComponentPackages(input, newPackageDirectoryPath)

    mainPackageContents = await assembleMainPackageContents(gameVersionName, packageNames)
    await createFile(newPackageDirectoryPath, "package.tsx", mainPackageContents)

async def assembleMainPackageContents(gameVersionName, packageNames):
    componentPackageExports = ""
    componentPackageInclusions = ""
    for packageName in packageNames:
        packageInclusion = 'import %s from "./%s/%s"\n' % (packageName, packageName, packageName)
        componentPackageInclusions = componentPackageInclusions + packageInclusion

        packageExport = "\t%s: %s, \n" % (packageName, packageName)
        componentPackageExports = componentPackageExports + packageExport

    return "//\n// %s\n//\n\n%s\nexport default {\n%s}" % (gameVersionName, componentPackageInclusions, componentPackageExports)

async def createComponentPackages(input, newPackageDirectoryPath):
    packageNames = []
    for componentDirectoryPath in next(os.walk(input))[1]:
        componentSourceDirectoryPath = "%s/%s" % (input, componentDirectoryPath)
        packageName = await createComponentPackage(componentSourceDirectoryPath, newPackageDirectoryPath)
        packageNames.append(packageName)

    return packageNames

async def createComponentPackage(componentSourceDirectoryPath, outputDirectoryPath):
    componentInstructions = await instructionsLoader.loadComponentInstructions(componentSourceDirectoryPath)
    componentName = componentInstructions["name"]

    componentOutputDirectory = "%s/%s" % (outputDirectoryPath, componentName)
    await createOrReplacePackageDirectory(componentOutputDirectory)

    frontInstructions = componentInstructions["frontInstructions"]

    componentImageInclusions = ""
    componentPackageExports = ""
    for frontInstruction in frontInstructions:
        pieceName = frontInstruction["name"]
        filepath = frontInstruction["filepath"]
        filename = os.path.basename(filepath)

        newFilepath = os.path.join(componentOutputDirectory, filename)
        shutil.copyfile(filepath, newFilepath)

        imageInclusion = 'import %s from "./%s"\n' % (pieceName, filename)
        componentImageInclusions = componentImageInclusions + imageInclusion

        packageExport = "\t%s: %s, \n" % (pieceName, pieceName)
        componentPackageExports = componentPackageExports + packageExport

    backInstructions = componentInstructions["backInstructions"]
    backFilepath = backInstructions["filepath"]
    backFilename = os.path.basename(backFilepath)
    backNewFilepath = os.path.join(componentOutputDirectory, filename)
    shutil.copyfile(backFilepath, backNewFilepath)
    backImageInclusion = 'import back from "./%s"' % backFilename
    componentImageInclusions = componentImageInclusions + backImageInclusion

    componentPackageExports = componentPackageExports + "\tback: back, \n"

    contents = "//\n// %s\n//\n\n%s\n\nexport default {\n%s}" % (componentName, componentImageInclusions, componentPackageExports)
    await createFile(componentOutputDirectory, "%s.tsx" % componentName, contents) 
    return componentName   

async def createFile(outputDirectory, filename, contents):
    filepath = os.path.join(outputDirectory, filename)
    if os.path.exists(filepath):
        os.remove(filepath)

    async with AIOFile(filepath, "w") as file:
        await file.write(contents)

async def createOrReplacePackageDirectory(newPackageDirectoryPath):
    if os.path.exists(newPackageDirectoryPath):
        shutil.rmtree(newPackageDirectoryPath, ignore_errors=False, onerror=None)

    os.mkdir(newPackageDirectoryPath)
