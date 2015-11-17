from datetime import datetime 

class Game(object):
    def __init__(self, d = None):

        if not d:
            self.date = None
            self.opponent = ''
            self.result = None
            self.players = []
        else:
            self.from_dict(d)

    def __str__(self):
        return '{0}'.format(self.get_json())

    def add_player(self, Player):
        self.players.append(Player)

    def from_dict(self, d):
        self.date = d['date']
        self.opponent = d['opponent']
        self.result = d['result']
        self.players = []

        for player in d['players']:
            self.add_player(Player(player))

    def get_influx_json(self):
        game = []
        for player in self.players:
            game.append({
                "measurement": "points",
                "tags": {
                    "opponent": self.opponent,
                    "player": player.player,
                    "play": player.play,
                    "result": self.result,
                },
                "time": self.date,
                "fields": {
                    "value": player.points
                }
            })
        return game

    def get_json(self):
        game = {
            'date': self.date,
            'opponent' : self.opponent,
            'result' : self.result,
            'players' : [],
        }

        for player in self.players:
            game['players'].append(player.get_json())

        return game

class Player(object):
    def __init__(self, d = None):

        if not d:
            self.player = ''
            self.points = 0
            self.play = False
        else:
            self.from_dict(d)

    def __str__(self):
        return 'Player: {0} Points: {1} Play: {2}'.format(self.player, self.points, self.play)

    def from_dict(self, data):
        self.player = data['player']
        self.points = data['points']
        self.play = data['play']

    def get_json(self):
        return {
            "player": self.player,
            "play": self.play,
            "points": self.points,
            }