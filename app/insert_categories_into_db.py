from models.models import Category
from database.db import session


# Create categories
def create_categories():
    s = session()
    category_1 = Category('General')
    category_2 = Category('Success and Achievement')
    category_3 = Category('Self-Confidence and Self-Esteem')
    category_4 = Category('Ledearship and Entrepreneurship')
    category_5 = Category('Happiness and Positivity')
    category_6 = Category('Perseverance and Resilience')
    category_7 = Category('Dreams and Aspirations')
    category_8 = Category('Inspiration from Famous Figures')
    category_9 = Category('Fitness and Health')
    category_10 = Category('Love and Relationships')
    category_11 = Category('Mindfulness and Inner Peace')
    category_12 = Category('Personal Development and Growth')
    category_13 = Category('Creativity and Innovation')
    
    s.add_all([
        category_1, category_2, category_3, category_4,
        category_5, category_6, category_7, category_8,
        category_9, category_10, category_11, category_12,
        category_13
    ])
    
    try:
        s.commit()
        s.close()
        print('Added categories successfully!')
    except Exception as e:
        print(e)


if __name__ == '__main__':
    create_categories()
