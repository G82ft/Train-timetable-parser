# Train-timetable-parser
This is a parser for train timetables. It uses data from the site tutu.ru.

***WARNING: it is only suitable for electric trains and only for St. Petersburg stations.***

You can get timetable in two ways:
  - Run the script with two command line arguments: first is the ID of the departure station and the second os the ID of the arrival station.
  - Run the script without command line arguments. You will be prompted to enter the name of the departure and arrival stations. If there are several options, you will be prompted to choose one.

In any case, you will get the formatted time table with departure and arrival time and price in RUB. Also, you will get a JSON file.

All station IDs are in the stations.json file.
