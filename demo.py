from google.appengine.ext import ndb
import webapp2
import json


	
class Boat(ndb.Model):
	id = ndb.StringProperty()	#This should be automatically generated by your API and should probably be a string
	name = ndb.StringProperty(required=True) #The name of the boat, a String
	type = ndb.StringProperty() #The type of the boat, power boat, sailboat, catamaran, etc. A string. 
	length = ndb.IntegerProperty() #The length of the boat
	at_sea = ndb.BooleanProperty() #A boolean indicating if the boat is at sea or not
	

class Slip(ndb.Model):
	id = ndb.StringProperty() #A string generated by your API
	number = ndb.IntegerProperty(required=True) #The the slip number, essentially the human understandable identifier
	current_boat = ndb.StringProperty() #The id of the current boat, null if empty
	arrival_date = ndb.StringProperty() #A string indicating the date the boat arrived in the slip
	
	
class BoatHandler(webapp2.RequestHandler):
	def post(self):		#add
		parent_key = ndb.Key(Boat, "parent_boat")
		boat_data = json.loads(self.request.body)	
		new_boat = Boat(name=boat_data['name'], type=boat_data['type'], length=boat_data['length'], at_sea=True, parent=parent_key)
		new_boat.put()
		new_boat.id = new_boat.key.urlsafe()
		new_boat.put()
		boat_dict = new_boat.to_dict()
		boat_dict['self'] = '/boat/' + new_boat.key.urlsafe()
		self.response.write(json.dumps(boat_dict))
	#end add
	
	def delete(self, id=None): #delete
		if id:
			try:
				s = Slip.query(Slip.current_boat == id).get()
			except: pass
			if (s):
				s.current_boat = None
				s.arrival_date = None
				s.put()
			
			b = ndb.Key(urlsafe=id).get()
			b_d = b.to_dict()
			b_d['self'] = "/boat/" + id
			self.response.write("Deleted: ")
			self.response.write(json.dumps(b_d))
			b.key.delete()
	
	#end delete 
	
	def get(self, id=None):	#view
		if id:
			b = ndb.Key(urlsafe=id).get()
			b_d = b.to_dict()
			b_d['self'] = "/boat/" + id
			self.response.write(json.dumps(b_d))
		else:				#view all
			all_boats = Boat.query().fetch()
			boats_obj = []
						
			for i in range (len(all_boats)):
				cur_obj = {}
				cur_obj['self'] = "/boat/" + all_boats[i].key.urlsafe()		
				cur_obj['id'] = all_boats[i].id		
				cur_obj['name'] = all_boats[i].name
				cur_obj['length'] = all_boats[i].length
				cur_obj['type'] = all_boats[i].type
				cur_obj['at_sea'] = all_boats[i].at_sea
				boats_obj.append(cur_obj)
				#self.response.write(cur_obj)
			self.response.write(boats_obj)
			#self.response.write(boats_obj[0]["self"])
			'''
			boats_obj.append('[')
			for i in range (len(all_boats)):
				cur_obj = '{"self": "/boat/'
				
				try:
					cur_obj += all_boats[i].key.urlsafe()
				except: pass
				
				cur_obj += '", "name": '
				try:
					cur_obj += '"' + all_boats[i].name + '", '
				except: cur_obj += 'null, '
				
				cur_obj += '"length": '
				try:
					cur_obj += '"' + all_boats[i].length + '", '
				except: cur_obj += 'null, '
				
				cur_obj += '"type": '
				try:
					cur_obj += '"' + all_boats[i].type + '", '
				except: cur_obj += 'null, '
				
				cur_obj += '"at_sea": '
				if all_boats[i].at_sea:
					cur_obj += 'true'
				else:
					cur_obj += 'false'
				cur_obj += '}'
				
				if i != len(all_boats) - 1:
					cur_obj += ', '
					
				boats_obj.append(cur_obj)
			
			boats_obj.append(']')
			for obj in boats_obj:	
				self.response.write(obj)
			'''
	#end view
	
	def patch(self, id=None):		#modify
		if id:
			b = ndb.Key(urlsafe=id).get()
			boat_data = json.loads(self.request.body)
			try: 
				boat_data['name']
				b.name = boat_data['name']
			except: pass
			try:
				boat_data['type']
				b.type = boat_data['type']
			except: pass	
			try:
				boat_data['length']
				b.length = boat_data['length']
			except: pass	
			try:
				boat_data['at_sea']
				b.at_sea = boat_data['at_sea']
			except: pass	
			b.put()
			b_d = b.to_dict()
			b_d['self'] = "/boat/" + id
			self.response.write(json.dumps(b_d))
	#end modify	
	
	def put(self, id=None):		#replace
		if id:
			parent_key = ndb.Key(Boat, "parent_boat")
			b = ndb.Key(urlsafe=id).get()
			boat_data = json.loads(self.request.body)
			try: 
				boat_data['name']
				b.name = boat_data['name']
			except: self.abort(400)
			try:
				boat_data['type']
				b.type = boat_data['type']
			except: b.type=None
			try:
				boat_data['length']
				b.length = boat_data['length']
			except: b.length=None	
			try:
				boat_data['at_sea']
				b.at_sea = boat_data['at_sea']
			except: None	
			b.put()
			b_d = b.to_dict()
			b_d['self'] = "/boat/" + id
			self.response.write(json.dumps(b_d))
	#end replace		
			
#end BoatHandler			
			
class SlipHandler(webapp2.RequestHandler):
	def post(self):		#add
		parent_key = ndb.Key(Slip, "parent_slip")
		slip_data = json.loads(self.request.body)
		new_slip = Slip(number=slip_data['number'], parent=parent_key)
		new_slip.put()
		new_slip.id = new_slip.key.urlsafe()
		new_slip.put()
		slip_dict = new_slip.to_dict()
		slip_dict['self'] = '/slip/' + new_slip.key.urlsafe()
		self.response.write(json.dumps(slip_dict))
	#end add
	
	def delete(self, id=None): #delete
		if id:
			s = ndb.Key(urlsafe=id).get()
			if s.current_boat == None:
				s_d = s.to_dict()
				s_d['self'] = "/slip/" + id
				self.response.write("Deleted: ")
				self.response.write(json.dumps(s_d))
				s.key.delete()
			else:
				b = ndb.Key(urlsafe=s.current_boat).get()
				b.at_sea = True
				b.put()
				s_d = s.to_dict()
				s_d['self'] = "/slip/" + id
				self.response.write("Deleted: ")
				self.response.write(json.dumps(s_d))
				s.key.delete()
	
	#end delete 
	
	def get(self, id=None):	#view
		if id:
			s = ndb.Key(urlsafe=id).get()
			s_d = s.to_dict()
			s_d['self'] = "/slip/" + id
			self.response.write(json.dumps(s_d))
		else:				#view all
			all_slips = Slip.query().fetch()
			slips_obj = []
						
			for i in range (len(all_slips)):
				cur_obj = {}
				cur_obj['self'] = "/slip/" + all_slips[i].key.urlsafe()	
				cur_obj['id'] = all_slips[i].id
				cur_obj['number'] = all_slips[i].number
				cur_obj['current_boat'] = all_slips[i].current_boat
				cur_obj['arrival_date'] = all_slips[i].arrival_date
				slips_obj.append(cur_obj)
				#self.response.write(cur_obj)
			self.response.write(slips_obj)
			#self.response.write(boats_obj[0]["self"])	
		
	#end view	

	def patch(self, id=None):		#modify
		if id:
			s = ndb.Key(urlsafe=id).get()
			slip_data = json.loads(self.request.body)
			try: 
				slip_data['number']
				s.number = slip_data['number']
			except: pass
			try:
				slip_data['current_boat']
				s.current_boat = slip_data['current_boat']
			except: pass	
			try:
				slip_data['arrival_date']
				s.arrival_date = slip_data['arrival_date']
			except: pass	
			
			s.put()
			s_d = s.to_dict()
			s_d['self'] = "/slip/" + id
			self.response.write(json.dumps(s_d))
	#end modify		
	
	def put(self, id=None):		#replace
		if id:
			parent_key = ndb.Key(Slip, "parent_slip")
			s = ndb.Key(urlsafe=id).get()
			slip_data = json.loads(self.request.body)
			try: 
				slip_data['number']
				s.number = slip_data['number']
			except: self.abort(400)
			try:
				slip_data['current_boat']
				s.current_boat = slip_data['current_boat']
			except: s.current_boat=None
			try:
				slip_data['arrival_date']
				s.arrival_date = slip_data['arrival_date']
			except: s.arrival_date=None	
	
			s.put()
			s_d = s.to_dict()
			s_d['self'] = "/slip/" + id
			self.response.write(json.dumps(s_d))
	#end replace		
#end SlipHandler
		
class Arr_Dep_Handler(webapp2.RequestHandler):		#Arrival/Departure Handler
	def put(self, id=None):	#Arrive
		if id:
			s = ndb.Key(urlsafe=id).get()
			boat_data = json.loads(self.request.body)
			if s.current_boat == None:
				
				try:
					s.current_boat = boat_data['boat_id']
				except: self.abort(400)
				try:
					s.arrival_date = boat_data['arrival_date']
				except: self.abort(400)
			
				b = ndb.Key(urlsafe=s.current_boat).get()
				b.at_sea=False
				b.put()
					
				s.put()
				s_d = s.to_dict()
				s_d['self'] = "/slip/" + id
				self.response.write(json.dumps(s_d))
				
			
			else: self.abort(403)
	#end Arrive
	
	def delete(self, id=None):	#Departure
		if id:
			s = ndb.Key(urlsafe=id).get()
			if s.current_boat == None:
				self.response.write("No Boat in this Slip")
			else:
				b = ndb.Key(urlsafe=s.current_boat).get()
				b.at_sea = True
				b.put()
				
				s.current_boat = None
				s.arrival_date = None
				s.put()
				s_d = s.to_dict()
				s_d['self'] = "/slip/" + id
				self.response.write("Removed Boat from Slip: ")
				self.response.write(json.dumps(s_d))
	
	#end Depart
		
#end Arrival/Departure Handler		

	
class MainPage(webapp2.RequestHandler):
    def get(self):
        self.response.write("Boat/Slip main page")

		
allowed_methods = webapp2.WSGIApplication.allowed_methods
new_allowed_methods = allowed_methods.union(('PATCH',))
webapp2.WSGIApplication.allowed_methods = new_allowed_methods
app = webapp2.WSGIApplication([
    ('/', MainPage),
	('/slip/(.*)/boat', Arr_Dep_Handler),
	('/boat', BoatHandler),
	('/boat/(.*)', BoatHandler), 
	('/slip', SlipHandler),
	('/slip/(.*)', SlipHandler),
], debug=True)

