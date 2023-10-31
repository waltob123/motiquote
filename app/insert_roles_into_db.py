from app.database.db import session
from app.models.models import Role


s = session()
user_role = Role('user')
admin_role = Role('admin')

s.add(user_role)
s.add(admin_role)
s.commit()
s.close()
