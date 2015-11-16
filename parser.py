# parser.py
# Generate a dict from a CSV file
# games = [{'date':date, 'opponent': opponent, 'players': [{'player': player, 'points': points, 'play':play}}] }, {...}]
import sys
import csv

import annotation

def parse_file(filename):
	with open(filename, 'r') as csvfile:
		reader = csv.reader(csvfile, delimiter=',', quotechar='|')
		
		games = []
		dates = [date for date in reader.next() if date]

		opponents = [opponent for opponent in reader.next() if opponent]
		
		for i,date in enumerate(dates):
			game = {'date' : date , 'opponent' : opponents[i], 'players' : []}
			games.append(game)

		for row in reader:
			player = row[0]
			for i,column in enumerate(row[1:]):

				if column is '-' or not column:
					points = 0
					play = False
				else:
					play = True
					points = column

				games[i]['players'].append({'player': player, 'points': points, 'play': play })

		return games

			
if __name__ == '__main__':

        if len(sys.argv) < 2:
                print("Error, missing CSV file")
        else:
                games = parse_file(sys.argv[1])

                import pprint
                pprint.pprint(games)

                influx = False
                if influx:
                	from influxdb import InfluxDBClient

	                json_game = []
	                for game in games:
	                        for player_data in game['players']:
	                                an = annotation.Annotation()
	                                an.from_data(game['date'], game['opponent'], player_data)

	                                json_game.append(an.get_json())

	                try:
	                        client = InfluxDBClient('localhost', 8086, 'root', 'root', 'orra')
	                        client.write_points(json_game)
	                except InfluxDBClientError as e:
	                        print e.content
