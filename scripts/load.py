import csv
import os
from fingerlinebot.models import Ministry_Interior

def run():
    file = open(r"data\NPA_LineID.csv",encoding="utf-8")
    read_file = csv.reader(file)

    #optional
    Ministry_Interior.objects.all().delete()

    count = 1

    for MI in read_file:
        if count == 1:
            pass
        else:
            print(MI)
            Ministry_Interior.objects.create(line_id=MI[1],inform_date=MI[2])
        count += 1
    