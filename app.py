from email import contentmanager
from flask import Flask, request, Response
from flask import json

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer, ForeignKey, create_engine
from sqlalchemy.orm import relationship, backref

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


Base = declarative_base()

class ToJson():
    def to_json(self):
        return json.dumps({col.name: getattr(self, col.name) for col in self.__table__.columns})

class Foro(Base, ToJson):
    __tablename__ = 'Foro'
    id = Column(Integer, primary_key=True)
    title = Column(String(180), nullable=False)
    content = Column(String(180), nullable=False)
  
    
class Subject(Base, ToJson):
    __tablename__ = 'Subject'
    idSubject = Column(Integer, primary_key=True)
    titleSubject = Column(String(180), nullable=False)
    contentSubject = Column(String(180), nullable=False)
    Foro_idSubject = Column(Integer, ForeignKey('Foro.id'), nullable=False)
    Foro = relationship('Foro', backref=backref('Subjects', uselist=True, cascade='delete,all'))

   
class Post(Base,ToJson):
    __tablename__ = 'Post'
    id = Column(Integer, primary_key=True)
    title = Column(String(180), nullable=False)
    content = Column(String(180), nullable=False)
    Subject_id = Column(Integer, ForeignKey('Subject.id'), nullable=False)
    Subject = relationship('idSubject', backref=backref('posts',  uselist=True, cascade='delete,all'))

engine = create_engine('sqlite:///base_servido2.sqlite')

session = sessionmaker()
session.configure(bind=engine)

app = Flask(__name__)

@app.route('/createbase')
def create_base():
    Base.metadata.create_all(engine)
    return 'createbase successfully'

@app.route('/newforo', methods=['POST'])
def new_foro():
    if not 'title' in request.form:
        return Response('Nombre no especificado' , status=400)
    title = request.form['title']
    content = request.form ['content']

    if title == '':
        return Response("{'Mesanje_Error':'titulo vacio'}", statur=400, mimetype='applicatio/json')

    foronuevo = Foro(title=title, content=content)

    s = session()
    s.add(foronuevo)
    s.commit()

    return Response(str(foronuevo.id), status=201, mimetype='application/json')

@app.route('/newsubject', methods=['POST'])
def new_subject():
    if not 'titleSubject' in request.form:
        return Response('Nombre no especificado' , status=400)
    titleSubject = request.form['titleSubject']
    contentSubject = request.form ['contentSubject']
    Foro_idSubject = request.form ['ForoidSubject']
    if titleSubject == '':
        return Response("{'Mesanje_Error':'titulo vacio'}", statur=400, mimetype='applicatio/json')

    subjectnuevo = Foro(titleSubject=titleSubject, contentSubject=contentSubject, Foro_idSubject=Foro_idSubject)

    s = session()
    s.add(subjectnuevo)
    s.commit()

    return Response(str(subjectnuevo.id), status=201, mimetype='application/json')


@app.route('/api/v1/newpost', methods=['POST'])
def new_post():
    
    if not 'title' in request.form:
        return Response('Nombre no especificado' , status=400)
    title = request.form['title']
    content = request.form ['content']
    Subjectid = request.form ['Subjectid']
    
    if title == '':
        return Response("{'Mesanje_Error':'titulo vacio'}", statur=400, mimetype='application/json')

    postnuevo = Foro(titleSubject=title, contentSubject=content, Foro_idSubject=Subjectid)

    s = session()
    s.add(postnuevo)
    s.commit()

    return Response(str(postnuevo.id), status=201, mimetype='application/json')


@app.route('/getforo', methods=['GET'])
def get_foro():
    s = session()
    foros = s.query(Foro)
    return Response(json.dumps([d.to_json() for d in foros]), status=200, mimetype='application/json')

@app.route('/getsubject', methods=['GET'])
def get_subjects():    
    s = session()
    subjects = s.query(subjects)
    return Response(json.dumps([d.to_json() for d in subjects]), status=200, mimetype='application/json')

@app.route('/getPosts', methods=['GET'])
def get_posts():
    s = session()
    Posts = s.query(Posts)
    return Response(json.dumps([d.to_json() for d in Posts]), status=200, mimetype='application/json')

#los deletes

@app.route('/deletepost/<int:id>', methods=['DELETE'])
def delete_posts():

    if id == '':
        return Response("{'Mesanje_Error':'Id vacio'}", statur=400, mimetype='application/json')
            
    s = session()
    d = s.query(Post).filter(Post.id==id).one()
    s.delete()

    return Response(Status=204)

@app.route('/deletesubject/<id>', methods=['DELETE'])
def delete_subject(id):
    
    if id == '':
        return Response("{'Mesanje_Error':'Id vacio'}", statur=400, mimetype='application/json')
            
    s = session()
    d = s.query(Subject).filter(Subject.id==id).one()
    s.delete()

    return Response(Status=204)


@app.route('/updateforo', methods=['PUT'])
def update_foro():

    if title == '':
     return Response("{'Mesanje_Error':'titulo vacio'}", statur=400, mimetype='application/json')

    if content == '':
     return Response("{'Mesanje_Error':'content vacio'}", statur=400, mimetype='application/json')
        
    id = request.form['id']
    title = request.form['title']
    content = request.form['content']
    
    s = session()
    d = s.query(Foro).filter(Foro.id==id).one()
    d.title = title
    d.content = content
    s.commit()

    return Response(Status=204)