# added a function to calulate the kinematics of the shape.
"""
0.0:	target_mass
0.1:	target_charge
0.2.x:	target_coordinate
0.3.x:	target_axial_velocity
1.0:	source_mass
1.1:	source_charge
1.2.x:	source_coordinate
1.3.x:	source_axial_velocity
"""
import math.py
class newtonian_physics_model:

	def init(dimensions=2,point_ground_gravity=9.81,Gravitational_Constant=6.6743e-11,Vacuum_Electric_Permitivity=8.85412878128e-12,Vacuum_Magnetic_Permeability=1.25663706212e-6):
		
		self.dimensions=dimensions
		self.point_ground_gravity=point_ground_gravity
		self.Gravitational_Constant=Gravitational_Constant
		self.Electrostatic_Constant=1/(4*math.PI*Vacuum_Electric_Permeability)
		self.Vacuum_Electric_Permitivity=Vacuum_Electric_Permitivity
		self.Vacuum_Magnetic_Permeability=Vacuum_Magnetic_Permeability
		
	def Update_Kinematics(point_object,force=[0,0],time_step=1/60,values={}):
		
		acceleration=[]
		for i in force:
			if(type(force[0])==int or type(force[0])==float):
				acceleration.append(i/point_object.mass)
			else:
				values["0.0"]=point_object.mass
				values["0.1"]=point_object.charge
				for i in range(len(point_object.position)):
					values["0.2."+str(i)]=point_object.position[i]
					values["0.3."+str(i)]=point_object.velocity[i]
				acceleration.append(i.evaluate(values)/point_object.mass)
		for i in range(len(acceleration)):
			point_object.velocity[i]+=acceleration[i]*time_step
			point_object.position[i]+=point_object.velocity[i]*time_step
	
	def Get_Gravity(self):
		def den(values):
			target_coordinate=[vaules["0.2."+str(i)] for i in range(self.dimensions)]
			source_coordinate=[vaules["1.2."+str(i)] for i in range(self.dimensions)]
			sum=0
			for i in range(self.dimensions):
				sum+=(target_coordinate[i]-source_coordinate[i])**2;
			return sum;
		return [(lambda values: self.Gravitational_Constant * values["0.0"] * values["1.0"] * (values["1.2."+str(i)]-values["0.2."+str(i)]) / (den(values)**(self.dimensions/2))) for i in range(dimensions)]
	
	def Get_Electrostatic_Force(self):
		def den(values):
			target_coordinate=[vaules["0.2."+str(i)] for i in range(self.dimensions)]
			source_coordinate=[vaules["1.2."+str(i)] for i in range(self.dimensions)]
			sum=0
			for i in range(self.dimensions):
				sum+=(target_coordinate[i]-source_coordinate[i])**2;
			return sum;
		return [(lambda values: values["0.1"] * values["1.1"] * (values["0.2."+str(i)]-values["1.2."+str(i)]) / (4*math.PI*self.Vacuum_Electric_Permitivity*(den(values)**(self.dimensions/2)))) for i in range(dimensions)]
