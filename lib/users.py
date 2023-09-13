#!/bin/env python

import os

from vlib.odict import odict
from vlib import db

class Users(object):
    '''Preside over Users data'''

    def getCurrentUser(self):
        '''Return an instantiated User Object
           of the current user
        '''
        # get username from nginx env
        username = os.getenv('REMOTE_USER')

        # or get username from unix env
        if not username:
            username = os.getenv('USER')

        return User(username)

class UserError(Exception): pass

class User(object):
    '''Preside over User record data

       Usage:
     
          from Users import User
          user = User('dlink')  # or User(1)
          print user.email
    '''
    def __init__(self, username):
        self.db = db.getInstance()

        if isinstance(username, int):
            sql = 'select * from users where id = %s'
        else:
            sql = 'select * from users where username = %s'
        results = self.db.query(sql, params=(username,))
        if not results:
            raise UserError('Unknown user: %s' % username)

        data = odict(results[0])
        data.fullname = '%s %s' % (data.first_name, data.last_name)
        self.__dict__.update(data)

    def __repr__(self):
        return f'<User:{self.username}>'

    # @lazyproperty
    # def access(self):
    #     '''Return users access list'''

    #     sql = '''
    #        select a.code as access
    #        from   users u
    #               join role_access ra on ra.role_id = u.role_id
    #               join access a on ra.access_id = a.id
    #        where  u.id = %s and
    #               u.active = 1 and
    #               a.active = 1
    #        '''
    #     results = self.db.query(sql, params=(self.id,))
    #     return [r['access'] for r in results]

    # def has_access(self, access_name):
    #     '''Return True or False if this user has the given access'''

    #     # debug:
    #     #print '<p>%s: %s</p>' % (access_name, access_name in self.access)

    #     if access_name in self.access:
    #         return True
    #     return False
