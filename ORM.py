'''
TEAM WORK: Develop an object relational mapping (ORM) utilizing metaclasses.
You might give  a BaseModel class to users, which they must inherit from in
order to create their own table in sqlite3. The BaseModel itself might have
a metaclass (BaseMeta) that controls attribute creation and object
management(manager creation). All interactions with the table (insertion,
deletion, updating) might be performed through the manager.

EXAMPLES:
class User(BaseModel):
    id = Field('INTEGER PRIMARY KEY AUTOINCREMENT')
    age = Field('INTEGER')
    first_name = Field('VARCHAR(30)', default='')
    last_name = Field('VARCHAR(30)', default='')
user = User.objects.insert(
    first_name='John',
    last_name='Test',
    age=10
)
user2 = User.objects.insert(
    first_name='John',
    last_name='Test2',
    age=10
)
And after all save changes
user.objects.save_changes()
'''

class User(BaseModel):
    id = Field('INTEGER PRIMARY KEY AUTOINCREMENT')
    age = Field('INTEGER')
    first_name = Field('VARCHAR(30)', default='')
    last_name = Field('VARCHAR(30)', default='')
user = User.objects.insert(
    first_name='John',
    last_name='Test',
    age=10
)
user2 = User.objects.insert(
    first_name='John',
    last_name='Test2',
    age=10
)