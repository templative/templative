from os import path, makedirs
import csv
from hashlib import md5

from googletrans import Translator
translator = Translator()

def translateText(text, destinationLanguageCode):
    response = translator.translate(text, src="en", dest=destinationLanguageCode)
    return response.text

def getTranslation(gameRootDirectory, text, destinationLanguageCode):
    if not hasExistingLanguageTranslationCache(gameRootDirectory, destinationLanguageCode):
        createLangaugeTranslationCache(gameRootDirectory, destinationLanguageCode)
    
    translationDictionary = loadTranslationDictionary(gameRootDirectory, destinationLanguageCode)
    if not text in translationDictionary:
        translation = translateText(text, destinationLanguageCode)
        if translation == None:
            return None
        translationDictionary[text] = translation
        writeTranslationDictionary(gameRootDirectory, destinationLanguageCode, translationDictionary)
    return translationDictionary[text]

def loadTranslationDictionary(gameRootDirectory, destinationLanguageCode):
    translationCacheFilepath = path.join(gameRootDirectory, "translations", destinationLanguageCode, "%s.csv" % destinationLanguageCode)
    if not path.exists(translationCacheFilepath):
        createLangaugeTranslationCache(gameRootDirectory, destinationLanguageCode)

    translationDictionary = {}
    with open(translationCacheFilepath, encoding='utf-8') as translationCacheFile:
        data = csv.DictReader(translationCacheFile, delimiter=',', quotechar='"')
        for item in data:
            translationDictionary[item["english"]] = item["translation"]
    return translationDictionary

def writeTranslationDictionary(gameRootDirectory, destinationLanguageCode, translationDictionary):
    translationCacheFilepath = path.join(gameRootDirectory, "translations", destinationLanguageCode, "%s.csv" % destinationLanguageCode)
    with open(translationCacheFilepath, "w", encoding='utf-8') as translationCacheFile: 
        translationCacheFile.write("english,translation\n")
        for key in translationDictionary:
            translationCacheFile.write("\"%s\",\"%s\"\n" % (key, translationDictionary[key]))
    
def createTranslationFolder(gameRootDirectory):
    translationDirectoryPath = path.join(gameRootDirectory, "translations")
    if path.exists(translationDirectoryPath):
        return
    makedirs(translationDirectoryPath)

def hasTranslationFolder(gameRootDirectory):
    translationDirectoryPath = path.join(gameRootDirectory, "translations")
    return path.exists(translationDirectoryPath)

def hasExistingLanguageTranslationCache(gameRootDirectory, destinationLanguageCode):
    return path.exists(path.join(gameRootDirectory, "translations", destinationLanguageCode))

def createLanguageTranslationCacheFolder(gameRootDirectory, destinationLanguageCode):
    makedirs(path.join(gameRootDirectory, "translations", destinationLanguageCode))

def createLangaugeTranslationCache(gameRootDirectory, destinationLanguageCode):
    if not hasTranslationFolder(gameRootDirectory):
        createTranslationFolder(gameRootDirectory)
    
    if not hasExistingLanguageTranslationCache(gameRootDirectory, destinationLanguageCode):
        createLanguageTranslationCacheFolder(gameRootDirectory, destinationLanguageCode)

    translationCacheFilepath = path.join(gameRootDirectory, "translations", destinationLanguageCode, "%s.csv" % destinationLanguageCode)
    
    with open(translationCacheFilepath, 'w') as translationCacheFile:
        translationCacheFile.write("english,translation\n")