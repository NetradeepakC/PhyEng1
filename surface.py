import custom_math as m2
class Surface:
	def init(self,points,dimension):
		coefficients=[]
		values=[]
		for i in range(dimension):
			coefficients.append([points[i][j] for i in range(dimension)])
			values.append(30)
		self.coefficients=m2.solve_equations([m2.equation(coefficients[i],values[i]) for i in range(dimension)])
