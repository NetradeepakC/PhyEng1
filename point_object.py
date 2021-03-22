import math_2
class point_object:
	
	default_mass=1
	default_x=0
	default_y=0
	default_speedx=0
	default_speedy=0
	default_charge=0
	
	def init(self,position=[default_x,default_y],velocity=[default_speedx,default_speedy],mass=default_mass,charge=default_charge):
		
		self.position=position
		self.velocity=velocity
		self.mass=mass
		self.charge=charge
	
	def change_state(self,force=[0,0,0],time_step=1/60,values={}):
		
		acceleration=[]
		if(type(force[0])==int):
			for i in force:
				acceleration.append(i/self.mass)
		else:
			values["body_mass"]=self.mass
			values["body_charge"]=self.charge
			for i in range(len(self.position)):
				values["coordinate"+str(i)]=self.position[i]
				values["axial_velocity"+str(i)]=self.velocity[i]
			for i in force:
				acceleration.append(i.evaluate_equation(values)/self.mass)
		for i in range(len(acceleration)):
			self.velocity[i]+=acceleration[i]*time_step
			self.position[i]+=self.velocity[i]*time_step
