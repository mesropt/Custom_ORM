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
import sqlite3
from pprint import pprint
class Field:
    '''
    This class represents a field in the database.
    It takes a field type and a default value as arguments.
    '''
    def __init__(self, field_type, default=None):
        self.field_type = field_type
        self.default = default

class Manager:
    '''
    This class represents the database table and it is responsible for
    all the operations on that table (CRUD etc.)
    '''
    def __init__(self, table_name, fields):
        self.table_name = table_name
        self.fields = fields
        self.conn = sqlite3.connect('usersdb.db')
        self.table_created = False

    def create_table(self):
        '''Create the table if it doesn't exist'''
        if self.table_created:
            return

        cursor = self.conn.cursor()
        fields_sql = ', '.join(f'{field_name} {field_def.field_type}' for field_name, field_def in self.fields.items())
        create_table_sql = f'CREATE TABLE IF NOT EXISTS {self.table_name} ({fields_sql})'
        cursor.execute(create_table_sql)
        self.conn.commit()
        self.table_created = True


    def drop_table_if_exists(self):
        ''''''
        cursor = self.conn.cursor()
        drop_sql_table_if_exists = f'DROP TABLE IF EXISTS {self.table_name}'
        cursor.execute(drop_sql_table_if_exists)
        self.conn.commit()

    def insert(self, **kwargs):
        '''Insert to the table'''
        self.create_table()
        cursor = self.conn.cursor()
        fields = ', '.join(kwargs.keys())
        placeholders = ', '.join('?' for _ in kwargs)
        insert_sql = f'INSERT INTO {self.table_name} ({fields}) VALUES ({placeholders})'
        cursor.execute(insert_sql, tuple(kwargs.values()))
        self.conn.commit()
        return cursor.lastrowid

    def delete(self, **kwargs):
        '''Delete from the table'''
        self.create_table()
        cursor = self.conn.cursor()
        conditions = ' AND '.join(f'{field} = ?' for field in kwargs)
        delete_sql = f'DELETE FROM {self.table_name} WHERE {conditions}'
        cursor.execute(delete_sql, tuple(kwargs.values()))
        self.conn.commit()

    def update(self, filters, **kwargs):
        '''Update the table'''
        self.create_table()
        cursor = self.conn.cursor()
        set_fields = ', '.join(f'{field} = ?' for field in kwargs)
        conditions = ' AND '.join(f'{field} = ?' for field in filters)
        update_sql = f'UPDATE {self.table_name} SET {set_fields} WHERE {conditions}'
        cursor.execute(update_sql, tuple(kwargs.values()) + tuple(filters.values()))
        self.conn.commit()

    def save_changes(self):
        '''Save changes to the database'''
        self.conn.close()

class BaseMeta(type):
    '''
    This metaclass takes the name of the class, its bases, and attributes
    as arguments, and returns a new class object. It moves the 'Field'
    instances out of the class attributes and puts them into a separate
    'objects' attribute.
    '''
    def __new__(meta, name, bases, attrs):
        fields = {field_name: attrs.pop(field_name) for field_name, field in list(attrs.items()) if isinstance(field, Field)}
        attrs['objects'] = Manager(name.lower(), fields)
        return super().__new__(meta, name, bases, attrs)

class BaseModel(metaclass=BaseMeta):
    '''
    This is the base class for user-defined models. It uses the 'BaseMeta'
    metaclass which means the logic in the 'BaseMeta.__new__()' method
    will be applied when user-defined models are created.
    '''
    pass


class User(BaseModel):
    '''
    This is a user-defined model class. It inherits from the 'BaseModel'
    class and defines some fields. An instance of the 'Manager' class is
    automatically assigned to the 'objects' attribute of the 'User' class.
    '''
    id = Field('INTEGER PRIMARY KEY AUTOINCREMENT')
    age = Field('INTEGER')
    first_name = Field('VARCHAR(30)', default='')
    last_name = Field('VARCHAR(30)', default='')

User.objects.drop_table_if_exists()

user1 = User.objects.insert(
    first_name='Richard',
    last_name='Dawkins',
    age=82
)
user2 = User.objects.insert(
    first_name='Neil deGrasse',
    last_name='Tyson',
    age=64)
user3 = User.objects.insert(
    first_name='Vilayanur Subramanian',
    last_name='Ramachandran',
    age=71
)
user4 = User.objects.insert(
    first_name='Peter',
    last_name='Boghossian',
    age=56
)
user5 = User.objects.insert(
    first_name='Sam',
    last_name='Harris',
    age=56
)
user6 = User.objects.insert(
    first_name='Thomas',
    last_name='Aquinas',
    age=49
)
User.objects.update({'first_name': 'Sam', 'last_name': 'Harris'}, age=999)
User.objects.delete(first_name='Thomas', last_name='Aquinas')
User.objects.save_changes()

conn = sqlite3.connect("usersdb.db")
curr = conn.cursor()
users = curr.execute('SELECT * FROM user').fetchall()
pprint(users)
