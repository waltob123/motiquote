from database.db import session
from models.models import Role


# create roles
def create_roles():
    s = session()
    user_role = Role('user')
    admin_role = Role('admin')

    s.add_all([user_role, admin_role])
    
    try:
        s.commit()
        s.close()
        print('Roles added successfully')
    except Exception as e:
        print(e)


if __name__ == '__main__':
    create_roles()
