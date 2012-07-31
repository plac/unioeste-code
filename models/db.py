from gluon.tools import *

db = DAL('sqlite://storage.sqlite')

auth = Auth(db)
auth.define_tables()


db.define_table('problem',
    Field('title'),
    Field('body','text'),
    Field('created_on','datetime',default=request.now),
    Field('created_by', db.auth_user, default=auth.user_id)
    )

db.define_table('code',
    Field('problem_id', db.problem),
    Field('body','text'),
    Field('created_on', 'datetime', default=request.now),
    Field('created_by', db.auth_user, default=auth.user_id)
    )

db.define_table('comment',
    Field('code_id', db.code),
    Field('body', 'text'),
    Field('created_on','datetime', default=request.now),
    Field('created_by', db.auth_user, default=auth.user_id)
    )

db.problem.title.requires = IS_NOT_IN_DB(db, 'problem.title')
db.problem.body.requires = IS_NOT_EMPTY()
db.problem.created_by.readable = db.problem.created_by.writable = False
db.problem.created_on.readable = db.problem.created_on.writable = False

db.code.body.requires = IS_NOT_EMPTY()
db.code.problem_id.readable = db.code.problem_id.writable = False 
db.code.created_by.readable = db.code.created_by.writable = False
db.code.created_on.readable = db.code.created_on.writable = False

db.comment.body.requires = IS_NOT_EMPTY()
db.comment.code_id.readable = db.comment.code_id.writable = False
db.comment.created_by.readable = db.comment.created_by.writable = False
db.comment.created_on.readable = db.comment.created_on.writable = False

crud = Crud(db)
