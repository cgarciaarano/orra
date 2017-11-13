from datetime import datetime


class Game(object):

    def __init__(self, d=None):

        if not d:
            self.date = None
            self.opponent = ''
            self.result = None
            self.score = None
            self.opponent_score = None
            self.season = None
            self.players = []
        else:
            self.from_dict(d)

    def __str__(self):
        return '{0}'.format(self.get_json())

    def add_player(self, Player):
        self.players.append(Player)

    def from_dict(self, d):
        self.date = d.get('date')
        self.opponent = d.get('opponent')
        self.result = d.get('result')
        self.opponent_score = d.get('opponent_score')
        self.players = []

        for player in d.get('players', []):
            self.add_player(Player(player))

        # TODO: Calculate season based on date. It should be a date
        self.season = d.get('season')

    def get_influx_json(self):
        game = []
        for player in self.players:
            game.append({
                "measurement": "game",
                "tags": {
                    "opponent": self.opponent,
                    "player": player.player,
                    "result": self.result,
                    "season": self.season,
                },
                "time": self.date,
                "fields": {
                    "score": player.points
                }
            })

        self.calc_score()
        game.append({
            "measurement": "game",
            "tags": {
                "opponent": self.opponent,
                "result": self.result,
            },
            "time": self.date,
            "fields": {
                "game_score": self.score
                "opponent_score": self.opponent_score
            }
        })
        return game

    def calc_score(self):
        self.score = map(sum, [p["points"] for p in self.players])


class Player(object):

    def __init__(self, d=None):

        if not d:
            self.player = ''
            self.points = 0
        else:
            self.from_dict(d)

    def __str__(self):
        return 'Player: {0} Points: {1}'.format(self.player, self.points)

    def from_dict(self, data):
        self.player = data['player']
        self.points = data['points']
