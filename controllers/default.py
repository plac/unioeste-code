# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
## This is a samples controller
## - index is the default action of any application
## - user is required for authentication and authorization
## - download is for downloading files uploaded in the db (does streaming)
## - call exposes all registered services (none by default)
#########################################################################

def index():
    problems = db().select(db.problem.ALL, orderby = db.problem.title)
    return dict(problems=problems)

@auth.requires_login()
def Problem():
    problem = db(db.problem.id==request.args(0)).select().first() or redirect(URL('error'))
    db.code.problem_id.default = problem.id
    form = SQLFORM(db.code)
    if form.process().accepted:
        response.flash = T('Your code has been posted')
    codes = db(db.code.problem_id == problem.id).select()    
    return dict(problem=problem, codes=codes, form=form)

@auth.requires_login()
def Code():
    code = db(db.code.id == request.args(0)).select().first() or redirect(URL('error'))
    db.comment.code_id.default = code.id
    form = SQLFORM(db.comment)
    if form.process().accepted:
        response.flash = T('Your comment has been posted')
    author = db(db.auth_user.id==code.created_by).select().first()
    comments = db(db.comment.code_id == code.id).select()
    return dict(code=code,author=author,comments=comments,form=form)

@auth.requires_membership('manager')
def manageCode():
    grid = SQLFORM.smartgrid(db.code)
    return dict(grid=grid)

def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    """
    return dict(form=auth())


def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request,db)


def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    return service()


@auth.requires_signature()
def data():
    """
    http://..../[app]/default/data/tables
    http://..../[app]/default/data/create/[table]
    http://..../[app]/default/data/read/[table]/[id]
    http://..../[app]/default/data/update/[table]/[id]
    http://..../[app]/default/data/delete/[table]/[id]
    http://..../[app]/default/data/select/[table]
    http://..../[app]/default/data/search/[table]
    but URLs must be signed, i.e. linked with
      A('table',_href=URL('data/tables',user_signature=True))
    or with the signed load operator
      LOAD('default','data.load',args='tables',ajax=True,user_signature=True)
    """
    return dict(form=crud())

