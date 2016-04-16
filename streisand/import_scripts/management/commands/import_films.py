# -*- coding: utf-8 -*-

from import_scripts.management.commands import MySQLCommand

from films.models import Film


BAD_IMDB_ID_FILMS = {
    13032,
    13033,
    16993,
    28369,
    10837,
    12405,
    10807,
    28368,
    28302,
    28371,
    10811,
    15048,
    16275,
    12184,
    10736,
    22427,
    29163,
    10823,
    17480,
    29179,
    10673,
    10715,
    10788,
    12023,
    10764,
    10717,
    13667,
    14092,
    10847,
    10817,
    12096,
    13658,
    10785,
    17296,
    10819,
    17227,
    19324,
    13183,
    14256,
    13637,
    22375,
    10725,
    10680,
    29001,
    13599,
    16761,
    12792,
    10692,
    10836,
    16088,
    13659,
    12592,
    11379,
    16554,
    13050,
    21595,
    10687,
    10730,
    10833,
    12370,
    13657,
    10653,
    13135,
    13747,
    10831,
    12506,
    13955,
    20884,
    17139,
    10698,
    16358,
    10832,
    12715,
    12340,
    16557,
    20321,
    10801,
    11360,
    12714,
    20843,
    14140,
    10746,
    10814,
    10666,
    10727,
    10677,
    22393,
    12066,
    14224,
    10694,
    21068,
    10794,
    10732,
    10752,
    14062,
    11089,
    10664,
    10709,
    13760,
    10780,
    16359,
    18611,
    10816,
    16439,
    12575,
    10741,
    10747,
    16516,
    10670,
    22442,
    14688,
    15849,
    13763,
    15957,
    16572,
    12228,
    15312,
    16704,
    15961,
    20742,
    20312,
    15998,
    16081,
    20815,
    22469,
    27532,
    29103,
    1390,
    15397,
}


class Command(MySQLCommand):

    SQL = """
        SELECT * FROM torrents_group
        WHERE torrents_group.ID IN (SELECT DISTINCT GroupID FROM torrents WHERE ID < 1000)
    """

    help = "Imports films from the MySQL db"

    def handle_row(self, row):

        tags = row['TagList'].strip('|').split('|')

        title = row['Name'].encode('latin-1').decode('utf-8')
        description = row['WikiBody'].encode('latin-1').decode('utf-8')
        notes = row['DoTNotes'].encode('latin-1').decode('utf-8')

        yt_id = row['YouTube']
        imdb_id = row['IMDB']

        film_id = row['ID']
        if film_id in BAD_IMDB_ID_FILMS:
            imdb_id = None

        f = Film.objects.create(
            old_id=film_id,
            title=title,
            year=row['Year'],
            imdb_id=imdb_id,
            description=description,
            moderation_notes=notes,
            poster_url=row['WikiImage'],
            trailer_url='https://www.youtube.com/watch?v={id}'.format(id=yt_id) if yt_id else '',
        )

        f.tags = tags

        print(f)
