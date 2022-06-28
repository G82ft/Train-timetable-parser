# Train-timetable-parser
This is a parser for train timetables. It uses data from the site tutu.ru.

***WARNING: it is only suitable for electric trains.***

You can get timetable in two ways:

- Run the script with two command line arguments: first is the name of the departure station and the second is the name
  of the arrival station.
- Run the script without command line arguments. You will be prompted to enter the name of the departure and arrival
  stations.

In any case, you will receive a formatted timetable for today (without departed trains) with departure and arrival times
and price in RUB. Also, you will get a JSON file.
