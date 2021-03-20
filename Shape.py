import math
class Shape:
	
	default_mass=1
	default_thita=0
	default_speedx=0
	default_speedy=0
	
	class equation:
		def init(self,coefficients,value):
			self.coefficients=coefficients
			self.value=value
	
	def dist(point0,point1):#calculate distance between points
		dist=0;
		square=lambda x:x*x
		for i in range(point0):
			dist+=square(point0[i]-point1[i])
		return math.sqrt(dist)
	
	def set_collision_radius(self):#calculate collision radius
		self.collision_radius=0
		for i in self.hit_points:
			self.collision_radius=max(self.collision_radius,dist(i,COM))
	
	def init(self,points=[[0,0],[0,1],[1,0]],masses=[default_mass,default_mass,default_mass],Thita=[default_thita],velocity=[default_speedx,default_speedy],connections=[[1,2],[2,0],[0,1]],hitbox_accuracy):
		dimension_error=0
		if(not type(points)==list):
			dimension_error=1
		elif(not type(masses)==list):
			dimension_error=2
		elif(not type(Thita)==list):
			dimension_error=3
		elif(not type(connections)==list):
			dimension_error=4
		elif(not len(points)==len(masses)):
			dimension_error=5
		elif(not len(points[0])==len(velocity)):
			dimension_error=6
		elif(not len(points[0])==len(Thita)-1):
			dimension_error=7
		elif(not len(points)==len(connections)):
			dimension_error=8
		else:
			for i in points:
				if(not type(i)==list):
					dimension_error=9
					break
				if(len(i)==len(points[0])):
					dimension_error=10
					break
				for j in i:
					if(not(type(j)==float or type(j)==int)):
						dimension_error=11
						break
				if(dimension_error):
					break
			if(not dimension_error):
				for i in masses:
					if(not (type(i)==int or type(i)==float)):
						dimension_error=12
						break
					elif(i==0):
						dimension_error=13
						break
			if(not dimension_error):
				for i in points:
					if(not type(i)==list):
						dimension_error=14
						break
					for j in i:
						if(not type(j)==int):
							dimension_error=15
							break
					if(dimension_error):
						break
		if(dimension_error==1):
			raise "Points has to be a list of points."
		elif(dimension_error==2):
			raise "Masses has to be a list of masses."
		elif(dimension_error==3):
			raise "Thita has to be a list of angles."
		elif(dimension_error==5):
			raise "Number of points must be equal to the number of masses."
		elif(dimension_error==6):
			raise "Dimension of points must be equal to dimension of velocity."
		elif(dimension_error==7):
			raise "Incorrect number of angles provided."
		elif(dimension_error==8):
			raise "Number of points must be equal to the number of set of connections."
		elif(dimension_error==9):
			raise "Each point has to be a list of coordinates."
		elif(dimension_error==10):
			raise "Each point has to have the same dimensions."
		elif(dimension_error==11):
			raise "Each coordinate has to be a number."
		elif(dimension_error==12):
			raise "Each mass has to be a number."
		elif(dimension_error==13):
			raise "Mass of a point cannot be zero."
		elif(dimension_error==14):
			raise "Each set of connections must be a list of pointers to a point."
		elif(dimension_error==15):
			raise "Each pointer has to be an integer."
		else:
			self.points=points#Coordinates of each point
			self.hit_points=points#Coordinates for hitbox
			self.masses=masses#Mass of each point
			self.Thita=Thita#Initial angle of rotation of shape
			self.COM=[0 for i in points[0]]
			self.net_mass=0#Total mass of body
			for i in range(len(points)):
				for j in range(len(points[0])):
					self.COM[j]+=points[i][j]*masses[i]#Adds the jth points mass*(value of coordinate in jth dimension) of ith point
				self.net_mass+=masses[i]#Adds mass of each point
			for i in range(len(COM)):
				self.COM[i]/=self.net_mass#Weighted average of coordinates
			set_collision_radius()#Collision radius is the minimum distance a point must be in order to collide with the body
			self.velocity=velocity
			self.connections=connections
			self.hitbox_accuracy=hitbox_accuracy
	
	def hitbox_approximate(self):
		
		def remove_repeats(hit_points):#Remove repeated points to reduce calculation and eliminate zero distance errors
			i=0
			while(i<len(hit_points)):
				j=i+1
				while(j<len(hit_points)):
					if(hit_points[i]==hit_points[j]):
						if(j<len(hit_points)-1):
							hit_points=hit_points[:j]+hit_points[j+1:]
						else:
							hit_points=hit_points[:j]
					j+=1
				i+=1
			return hit_points
		
		def remove_collinear(hit_points):#Remove collinear points to reduce calculation
			i=0
			while(i<len(hit_points)):
				j=i+1
				while(j<len(hit_points)):
					k=j+1
					while(k<len(hit_points)):
						vect0=[hit_points[k][l]-hit_points[i][l] for l in range(len(hit_points[0]))]
						vect1=[hit_points[j][l]-hit_points[i][l] for l in range(len(hit_points[0]))]
						collinear=True
						for l in range(1,len(vect0)):
							if(not vect0[0]/vect1[1]==vect0[l]/vect1[l]):
								collinear=False
								break
						if(collinear):
							dispij=abs(hit_points[i][0]-hit_points[j][0])
							dispjk=abs(hit_points[j][0]-hit_points[k][0])
							dispki=abs(hit_points[k][0]-hit_points[i][0])
							if(dispij>dispjk and dispij>dispki):
								hit_points.remove(hit_points[k])
								k-=1
							elif(dispjk>dispjk and dispij>dispki):
								hit_points.remove(hit_points[i])
								j=i+1
								k=j
							else:
								hit_points.remove(hit_points[j])
								k=j
						k+=1
					j+=1
				i+=1
			return hit_points
		
		def find_coefficients(equations):#Required to find equation of the n-1 dimensional body(line,plane...) that contains n points needed for integration
			if(len(equations)==1):#If there is only one equation then the only variable can be calculated
				return [equations[0].value/equations[0].coefficients[0]]
			else:#Using substitution method to solve multiple variables in recursion
				coefficients=[[equations[i].coefficients[j]-equations[0].coefficients[j]*equations[i].coefficients[0]/coefficients[0].equations[0] for j in range(1,len(equations[0].coefficients))] for i in range(1,len(equations))]
				value=[equations[i].value-equations[0].value*equations[i].coefficients[0]/equations[0].coefficients[0] for i in range(1,len(equations))]
				coefficients=find_coefficients([equation(coefficients[i],value[i]) for i in range(len(equations)-1)])
				a0=equations[0].value
				for i in range(1,len(equations[0].coefficients)):
					a0-=coefficients[i]*equations[0].coefficients[i]
				a0/=equations[0].coefficients[0]
				return a0+coefficients
		
		def find_normal(base_points,peak_point):#Given a base in and n-dimensional space, calculate normal, by ax1+by1+cz1=........+d/sqrt(a*a+b*b+c*c+.....)
			value=30
			coeffecients_of_plane=find_coefficient([equation(i,value) for i in base_points])
			num=0
			dem=0
			for i in range(coefficients_of_plane):
				num+=base_paints[i]*coefficients_of_plane[i]
				den+=coefficients_of_plane[i]*coefficients_of_plane[i]
			num-=value
			den=math.sqrt(den)
			return num/den
		
		def remove_hit_point(current_point,hit_points,connections):#Function to remove hitpoint from object
			hit_points.pop(current_point)
			for i in connections[current_point]:
				connections[i].remove(current_point)
			connections.pop(current_point)
			new_connections=[]
			for i in connections:
				lst=[]
				for j in i:
					lst.append(j if j<current_point else j-1)
				new_connections.append(lst)
			return (hit_points,new_connections)
		
		def is_looped(connections,reached_points,to_be_reached):#Checks if all the given points are directly connected to at least one of the same set, to form a base
			for i in reached_points:
				for j in to_be_reached:
					if j in connections[i]:
						reached_points.append(j)
						to_be_reached.remove(j)
						if(len(to_be_reached)==0):
							break
					if(len(to_be_reached)==0):
						break
			return len(to_be_reached)==0
		
		def has_close_base(current_point,hit_points,connections,collision_radius,hitbox_accuracy):#Checks if a base is close to a given point
			current_connections=connections[current_point]
			
			if(not is_looped(connections,current_connections[0],current_connections[1:])):
				return False
			
			if len(current_connections)>len(hit_points[0]):
				base_lst=[hit_points[i] for i in current_connections[:len(hit_points[0])]]
				max_deviation_from_base=0
				min_deviation_from_base=0
				normal=find_normal(base_lst,hit_points[current_point])
				for i in current_connections[len(hit_points[0]):]:
					deviation=find_normal(base_lst,hit_points[i])
					if(deviation>max_deviation_from_base):
						max_deviation_from_base=deviation
					elif(deviation<min_deviation_from_base):
						min_deviation_from_base=deviation
				if((max_deviation-min_deviation)/collision_radius>1-hitbox_accuracy/100):
					return False
			else:
				normal=find_normal([hit_points[i] for i in current_connections],points[current_point])
			if(normal/collision_radius>1-hitbox_accuracy/100):
				return False
			
			centre=[0 for i in len(hit_points[0])]
			max_dist_of_base_from_centre=0
			for i in current_connections:
				for j in range(len(hit_points[i])):
					centre[j]+=hit_points[i][j]
			for i in range(len(centre)):
				centre[i]/=len(current_connections)
			for i in current_connections:
				current_dist=dist(hit_points[i],centre)
				if(current_dist>max(max_dist_of_base_from_centre,normal)):
					max_dist_of_base_from_centre=current_dist
			if(dist(hit_points[current_point],centre)>max(max_dist_of_base_from_centre,normal)):
				return False
			return True
		
		self.hit_points=remove_repeats(self.hit_points)
		self.hit_points=remove_collinear(self.hit_points)
		for i in range(len(hit_points)):
			if has_close_base(i,self.hit_points,self.connections,self.collision_radius,self.hit_box_accuracy)#Approximates a small hill as flat plane
				self.hit_points,self.connections=remove_hit_point(i,self.hit_points,self.connections)
