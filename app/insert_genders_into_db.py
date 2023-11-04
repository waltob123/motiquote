from models.models import Gender
from database.db import session


def insert_genders():
    '''Insert genders into the database.'''
    male = Gender('Male')
    female = Gender('Female')
    
    s = session()
    s.add_all([male, female])
    try:
        s.commit()
    except Exception as e:
        print(e)
        s.rollback()
    s.close()
    print('Genders added successfully!')


if __name__ == '__main__':
    insert_genders()
