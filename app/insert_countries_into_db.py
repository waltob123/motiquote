import json
import os
from models.models import Country
from database.db import session


def insert_countries():
    '''Inserts countries into the database.'''
    if os.path.exists('countries.json'):
        with open('countries.json') as f:
            countries = json.load(f)
        s = session()
        for country in countries:
            c = Country(country=country.get('name'), code=country.get('code'))
            s.add(c)
        try:
            s.commit()
        except Exception as e:
            print(e)
            s.rollback()
        s.close()
        print('Countries added successfully!')
    else:
        print('countries.json not found!')


if __name__ == '__main__':
    insert_countries()
