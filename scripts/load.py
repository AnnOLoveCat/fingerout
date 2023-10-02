import csv
import os
from fingerlinebot.models import Ministry_Interior,News,Links

def run():
    # file = open(r"data\NPA_LineID.csv",encoding="utf-8")
    # file = open(r"data\NPA_165.csv",encoding="utf-8")
    file = open(r"data\NPA_link.csv",encoding="utf-8")
    read_file = csv.reader(file)

    #optional
    Links.objects.all().delete()
    # Ministry_Interior.objects.all().delete()
    # News.objects.all().delete()

    count = 1

    for read in read_file:
        if count == 1:
            pass
        else:
            print(read)
            Links.objects.create(description=read[1],web_link=read[2],domain_name=read[3],build_time=read[4])
            # Ministry_Interior.objects.create(line_id=read[1],inform_date=read[2])
            # News.objects.create(news_title=read[1],post_time=read[2],news_content=read[3])
        count += 1
    