class equation:
	def init(self,coefficients,value):
		self.coefficients=coefficients
		self.value=value
def solve_equations(equations):
	if(len(equations)==1):
		return [equations[0].value/equations[0].coefficients[0]]
	else:
		coefficients=[[equations[i].coefficients[j]-equations[0].coefficients[j]*equations[i].coefficients[0]/coefficients[0].equations[0] for j in range(1,len(equations[0].coefficients))] for i in range(1,len(equations))]
		value=[equations[i].value-equations[0].value*equations[i].coefficients[0]/equations[0].coefficients[0] for i in range(1,len(equations))]
		variables=solve_equations([equation(coefficients[i],value[i]) for i in range(len(equations)-1)])
		a0=equations[0].value
		for i in range(1,len(equations[0].coefficients)):
			a0-=variables[i]*equations[0].coefficients[i]
		a0/=equations[0].coefficients[0]
		return [a0]+variables
