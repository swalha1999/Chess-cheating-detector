
# interface for mongoDB to save chess games data 

from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

class ChessGameDatabase:
    def __init__(self, mongoUrl='chess_games.db'):
        self.db_url = mongoUrl
        self.conn = None
    
    def connect(self):
        # Create a new client and connect to the server
        self.conn = MongoClient(self.db_url, server_api=ServerApi('1'))
        try:
            self.conn.admin.command('ping')
            print("Pinged your deployment. You successfully connected to MongoDB! Database:", self.conn.list_database_names())
        except Exception as e:
            print(e)

    def getGames(self):
        return self.conn["chess"]["games"]
    
    def getPlayers(self):
        return self.conn["chess"]["players"]
    
    def addPlayer(self, playerusername, accuracy, game_date):
        self.getPlayers().insert_one({"username": playerusername, "accuracy": accuracy, "date": game_date})

    def close(self):
        self.conn.close()

    def playerGames(self, player):
        return list(self.getGames().find({"$or": [{"White": player}, {"Black": player}]}))
    
    def playerGamesCount(self, player):
        return self.getGames().count_documents({"$or": [{"White": player}, {"Black": player}]})
    
    def addGame(self, game):
        #check if the game is already in the database
        if self.getGames().find_one({"hash": game["hash"]}):
            return False
        else:
            self.getGames().insert_one(game.get_headers())
            return True
    
    def saveGame(self, game):
        self.getGames().replace_one({"hash": game["hash"]}, game)
    
    def check_if_game_exist(self, game):
        return len(list(self.getGames().find_one({"hash": game.get_headers()["hash"]}))) > 0 