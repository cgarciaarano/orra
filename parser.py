#!/usr/bin/env python
# parser.py
# Generate a dict from a CSV file
# games = [{'date':date, 'opponent': opponent, 'result':'win' 'players': [{'player': player, 'points': points, 'play':play}}] }, {...}]
import sys
import csv
from datetime import datetime
import traceback

from influxdb import InfluxDBClient

import models


def parse_file(filename):
    with open(filename, 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='"')

        games = []
        dates = [date for date in next(reader) if date]
        result = [result for result in next(reader) if result]
        opponents = [opponent for opponent in next(reader) if opponent]

        for i, date in enumerate(dates):
            game = models.Game({'date': datetime.strptime(date, '%d/%m/%Y'), 'opponent': opponents[i], 'result': result[i], 'players': []})
            games.append(game)

        for row in reader:
            player = row[0]
            if not player:
                continue
            for i, column in enumerate(row[1:]):

                if column is '-' or not column:
                    continue
                else:
                    play = True
                    points = column

                games[i].add_player(models.Player({'player': player, 'points': int(points), 'play': bool(play)}))

        return games


if __name__ == '__main__':

    if len(sys.argv) < 2:
        print("Error, missing CSV file")
    else:
        games = parse_file(sys.argv[1])

        influx = True
        if influx:
            json_games = []
            for game in games:
                json_games.extend(game.get_influx_json())

            try:
                client = InfluxDBClient('influx', 8086, 'root', 'root', 'orra')
                client.create_database("orra")
                client.write_points(json_games)
            except:
                traceback.print_exc()
