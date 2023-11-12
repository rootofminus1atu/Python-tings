from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker, relationship

import os
from dotenv import load_dotenv
load_dotenv()


DB_USERNAME = 'postgres'
DB_PASSWORD = os.getenv('DB_PASS') 
DB_HOST = 'localhost'
DB_PORT = '5432'
DB_NAME = 'atuoverflowtest'

db_url = f'postgresql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'

engine = create_engine(db_url)



Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String)
    posts = relationship('Post', back_populates='user')

class Post(Base):
    __tablename__ = 'posts'
    id = Column(Integer, primary_key=True)
    title = Column(String)
    content = Column(String)
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship('User', back_populates='posts')

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()



# Create a user with posts
user = User(username='john_doe', posts=[Post(title='Post 1', content='Content 1'), Post(title='Post 2', content='Content 2')])
session.add(user)
session.commit()

# Query a user and their posts
queried_user = session.query(User).filter_by(username='john_doe').first()
print(queried_user.username)
for post in queried_user.posts:
    print(post.title, post.content)



another = User()