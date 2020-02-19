import client

def getGames():
    sessionID = client.login()
    # print(client.getGames(sessionID))