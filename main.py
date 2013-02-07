import webapp2
from google.appengine.api import users 
from google.appengine.ext import db
import os
import jinja2
import datetime
import calendar

jinja_environment = jinja2.Environment(loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))

##def add_months(sourcedate,months):
##    month = sourcedate.month - 1 + months
##    year = sourcedate.year + month / 12
##    month = month % 12 + 1
##    day = min(sourcedate.day,calendar.monthrange(year,month)[1])
##    return datetime.date(year,month,day)

class UserTable(db.Model):
    useremail = db.Key()
    nickname = db.StringProperty() # derived from useremail
     

class ItemList(db.Model):
    itemid = db.Key()
    itemname = db.StringProperty()
    itemdescription = db.StringProperty()
    itemprice = db.FloatProperty()
    itemexpiryd = db.StringProperty()
    itemowner= db.ReferenceProperty(UserTable, required=True, collection_name='ItemList_itemowner_set')

class MessageList(db.Model):
    messageid = db.Key()
    datesent = db.DateProperty()
    content = db.StringProperty()

class SenderTable(db.Model):  #(compound key)
    messageid = db.ReferenceProperty(MessageList, required=True, collection_name='SenderTable_messageid_set')
    senderid = db.ReferenceProperty(UserTable, required=True, collection_name='SenderTable_senderid_set')

class RecipientTable(db.Model): # (compound key)
    messageid = db.ReferenceProperty(MessageList, required=True, collection_name='RecipientTable_messageid_set') 
    recipientid = db.ReferenceProperty(UserTable, required=True, collection_name='RecipientTable_senderid_set')



class MainHandler(webapp2.RequestHandler):
    '''Home page handler'''
    def get(self):
        user = users.get_current_user()
        useremail = user.email()

        if user: 
        # if logged in
        # display 'welcome, username' at top right hand corner
        # get username from email (key) using GQL

            UserTable(key_name=user.email(), nickname=user.email()).put()
            
        else:
        # if not logged in
        # display register | sign in
        
            self.redirect(users.create_login_url(self.request.uri))
        template_values = {
##            'username': nickname,
            'useremail': useremail
            }


        template = jinja_environment.get_template('index.html')
        self.response.out.write(template.render(template_values))



    # regardless of whether logged in or not
    # display home page - search bar + items


class Shop(webapp2.RequestHandler):
    '''Shop handler'''
    def get(self):
        user = users.get_current_user()
        useremail = user.email()

        if user: 
        # if logged in
        # display 'welcome, username' at top right hand corner
        # get username from email (key) using GQL

            UserTable(key_name=user.email(), nickname=user.email()).put()
            
        else:
        # if not logged in
        # display register | sign in
        
            self.redirect(users.create_login_url(self.request.uri))
        template_values = {
##            'username': nickname,
            'useremail': useremail
            }

        template = jinja_environment.get_template('shop.html')
        self.response.out.write(template.render(template_values))


class SellItem(webapp2.RequestHandler):
    '''Sell Item page handler'''
    def get(self):
        user = users.get_current_user()
        useremail = user.email()

        if user: 
        # if logged in
        # display 'welcome, username' at top right hand corner
        # get username from email (key) using GQL

            UserTable(key_name=user.email(), nickname=user.email()).put()
            
            
        else:
        # if not logged in
        # display register | sign in
        
           self.redirect(users.create_login_url(self.request.uri))

        template_values = {
            #'username': nickname,
            'useremail': useremail
            }

        template = jinja_environment.get_template('sell_item_page.html')
        self.response.out.write(template.render(template_values))

class Display(webapp2.RequestHandler):
	''' display handler'''
	def post(self):
            user = users.get_current_user()
            useremail = user.email()

            sdate = str(datetime.datetime.now().date())
            edate = sdate
            
            itemname = self.request.get('itemname')
            itemdescription = self.request.get('description')
            itemprice = float(self.request.get('price'))
            self.response.out.write(itemname)
            self.response.out.write(itemdescription)
            self.response.out.write(itemprice)
            self.response.out.write(user)

##		item = ItemList()
##            item = ItemList(itemid='I001')
##            item.itemname = itemname
##            item.itemdescription = itemdescription
##            item.itemprice = itemprice
##            item.expiryd = datetime.datetime.now().date()
##            item.put()
            ItemList(key_name=sdate, itemname=itemname,
                     itemdescription=itemdescription, itemprice=itemprice,
                     itemowner=user).put()
            

app = webapp2.WSGIApplication([('/', MainHandler),
                               ('/shop', Shop),
                               ('/sell_item_page', SellItem),
                               ('/display', Display)],
                                debug=True)


