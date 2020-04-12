from app.models import User
from flask_seeder import Seeder

class UserSeeder(Seeder):
  def __init__(self, db=None):
    super().__init__(db=db)
    self.priority = 10

  def run(self):
    user = User(username='lb3', email='lb3@example.com')
    user.set_password('sml12345')
    self.db.session.add(user)
    self.db.session.commit()