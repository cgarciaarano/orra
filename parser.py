# parser.py
# Generate a dict from a CSV file
# games = [{'date':date, 'opponent': opponent, 'result':'win' 'players': [{'player': player, 'points': points, 'play':play}}] }, {...}]
import sys
import csv
from datetime import datetime

import annotation

def parse_file(filename):
    with open(filename, 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='"')
        
        games = []
        dates = [date for date in reader.next() if date]
        result = [result for result in reader.next() if result]
        opponents = [opponent for opponent in reader.next() if opponent]
        
        for i,date in enumerate(dates):
            game = {'date' : datetime.strptime(date,'%d/%m/%Y') , 'opponent' : opponents[i], 'result' : result[i], 'players' : []}
            games.append(game)

        for row in reader:
            player = row[0]
            if not player:
                continue
            for i,column in enumerate(row[1:]):

                if column is '-' or not column:
                    points = 0
                    play = False
                else:
                    play = True
                    points = column

                games[i]['players'].append({'player': player, 'points': int(points), 'play': bool(play) })

        return games

            
if __name__ == '__main__':

        if len(sys.argv) < 2:
                print("Error, missing CSV file")
        else:
                games = parse_file(sys.argv[1])

                import pprint
                for game in games:
                    pprint.pprint(annotation.Game(game).get_json())

                influx = False
                if influx:
                    json_games = []
                    for game in games:

                        json_game = annotation.Game(game).get_influx_json()
                        json_games.extend(json_game)
                    import pprint
                    pprint.pprint(json_games)

                    try:
                            from influxdb import InfluxDBClient
                            client = InfluxDBClient('localhost', 8086, 'root', 'root', 'orra')
                            client.write_points(json_game)
                    except InfluxDBClientError as e:
                            print e.content
