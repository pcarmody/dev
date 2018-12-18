import csv

with open('bandplan.csv', 'rb') as csvfile:
  xxx = csv.reader(csvfile, delimiter=',', quotechar='"')
  for row in xxx:
    print '| '.join(row)
