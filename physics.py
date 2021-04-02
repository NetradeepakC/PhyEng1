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
import math
import custom_math as m2


def Update_Kinematics(Radial_Object, force=None, time_step=1 / 60, values=None):

	if force is None:
		force = [0, 0]
	if values is None:
		values = {}
	acceleration = []
	for i in force:
		acceleration.append(i/Radial_Object.mass)
	for i in range(len(acceleration)):
		Radial_Object.velocity[i] += acceleration[i]*time_step
		Radial_Object.position[i] += Radial_Object.velocity[i]*time_step


def Surface_Collision(Radial_Object_List, Surface_List, time_step=1 / 60):
	for i in Surface_List:
		Magnitude_of_Normal = m2.Magnitude(i.coefficients)
		Unit_Vector_Along_Normal = [j/Magnitude_of_Normal for j in i.coefficients]
		for j in Radial_Object_List:
			if j.radius > m2.normal_from_surface(j.position, i):
				Cos = m2.Cos(j.velocity, i.coefficients)
				Speed_Along_Normal = m2.Magnitude(j.velocity)*Cos
				Velocity_Along_Normal = [Speed_Along_Normal*k for k in Unit_Vector_Along_Normal]
				Velocity_Along_Surface = [j.velocity[k]-Velocity_Along_Normal[k] for k in range(len(j.velocity))]
				j.position = [j.position[k]-Velocity_Along_Normal[k]*time_step for k in range(len(j.velocity))]
				j.velocity = [Velocity_Along_Surface[k]-Velocity_Along_Normal[k] for k in range(len(j.velocity))]


class newtonian_physics_model:

	def __init__(self, dimensions=2, point_ground_gravity=9.81, Gravitational_Constant=6.6743e-11, Vacuum_Electric_Permittivity=8.85412878128e-12, Vacuum_Magnetic_Permeability=1.25663706212e-6):
		
		self.dimensions = dimensions
		self.point_ground_gravity = point_ground_gravity
		self.Gravitational_Constant = Gravitational_Constant
		self.Electrostatic_Constant = 1/(4*math.pi*Vacuum_Electric_Permittivity)
		self.Vacuum_Electric_Permittivity = Vacuum_Electric_Permittivity
		self.Vacuum_Magnetic_Permeability = Vacuum_Magnetic_Permeability

	def Get_Gravity(self):
		def den(values):
			target_coordinate = [values["0.2."+str(i)] for i in range(self.dimensions)]
			source_coordinate = [values["1.2."+str(i)] for i in range(self.dimensions)]
			sum = 0
			for i in range(self.dimensions):
				sum += (target_coordinate[i]-source_coordinate[i])**2
			return sum
		return [(lambda values: self.Gravitational_Constant * values["0.0"] * values["1.0"] * (values["1.2."+str(i)]-values["0.2."+str(i)]) / (den(values)**(self.dimensions/2))) for i in range(self.dimensions)]
	
	def Get_Electrostatic_Force(self):
		def den(values):
			target_coordinate = [values["0.2."+str(i)] for i in range(self.dimensions)]
			source_coordinate = [values["1.2."+str(i)] for i in range(self.dimensions)]
			sum = 0
			for i in range(self.dimensions):
				sum += (target_coordinate[i]-source_coordinate[i])**2
			return sum
		return [(lambda values: self.Electrostatic_Constant * values["0.1"] * values["1.1"] * (values["0.2."+str(i)]-values["1.2."+str(i)]) / (den(values)**(self.dimensions/2))) for i in range(self.dimensions)]
	
	def Equate_Electrostatic_Potential(self, obj1, obj2):
		if obj1.conductivity and obj2.conductivity:
			Charge_Transferred = 0
			if self.dimensions == 2:
				log1 = math.log(obj1.radius)
				log2 = math.log(obj2.radius)
				Charge_Transferred = (obj1.charge*log1-obj2.charge*log2)/(log1+log2)
			else:
				Charge_Transferred = (obj1.charge*(obj2.radius**(1-self.dimensions))-obj2.charge*(obj1.radius**(1-self.dimensions)))/(obj1.radius**(1-self.dimensions)+obj2.radius**(1-self.dimensions))
			obj1.charge -= Charge_Transferred
			obj2.charge += Charge_Transferred
