from datetime import datetime 

class Annotation(object):
    def __init__(self):

        self.date = None
        self.opponent = ''
        self.player = ''
        self.points = 0
        self.play = False

    def __str__(self):
        return '{0}'.format(self.get_json())

    def get_json(self):
        return {
                "measurement": "points",
                "tags": {
                    "opponent": self.opponent,
                    "player": self.player,
                    "play": self.play
                },
                "time": self.date,
                "fields": {
                    "value": self.points
                }
            }

    def from_dict(self, date, opponent, data):
        self.date = date
        self.opponent = opponent
        self.player = data['player']
        self.points = data['points']
        self.play = data['play']