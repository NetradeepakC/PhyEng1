"""
Each surface is a1*x1+a2*x2+.......=b
The way this is achieved is n n-dimensional points are given and checked which surface which surface passes through it.
Let the points be P1,P2,......Pn
Pm=(Xm1,Xm2,......,Xmn)
a1*X11+a2*X12+......an*X1n=30
a1*X21+a2*X22+......an*X2n=30
.
.
.
an*Xn1+a2*Xn2+......an*Xnn=30
Here, 30 is chosen as am will scale according to it and 30=2*3*5
The above mentioned equations are solved to get a1,a2,......an
"""
import custom_math as m2


class Surface:
	def __init__(self, points, dimension):
		coefficients = []
		values = []
		self.points = points
		for i in range(dimension):
			coefficients.append([points[i][j] for j in range(dimension)])
			values.append(30)
		self.coefficients = m2.solve_equations([m2.equation(coefficients[i], values[i]) for i in range(dimension)])
		self.value = 30
