import math
class collision:
    def __init__(self,m1,m2,x1,x2,y1,y2,v1,v2):
        self.m1 = m1
        self.m2 = m2
        self.x1 = x1
        self.x2 = x2
        self.y1 = y1
        self.y2 = y2
        self.v1 = v1
        self.v2 = v2
        self.timex = 0
        self.timey = 0
    def ifcollide1d(self,x_1,x_2,v_1,v_2):
        if (x_1 - x_2 > 0 and v_2 - v_1 > 0) or (x_1 - x_2 < 0 and v_1 - v_2 > 0):
            return True
        else:
            return False

    def collide1d(self, vv1, vv2):
            l = []
            u1 = ((self.m2*(vv2-vv1) + self.m1*vv1 + self.m2*vv2)/(self.m1 + self.m2))
            l.append(u1)
            l.append(vv1 + u1 - vv2)
            return l

    def ifcollide2d(self):
        if self.ifcollide1d(self.x1, self.x2, self.v1[0], self.v2[0]):
          self.timex = abs((self.x2-self.x1)/(self.v2[0]-self.v1[0]))
          if self.ifcollide1d(self.y1, self.y2, self.v1[1], self.v2[1]):
            self.timey = abs((self.y2-self.y1)/(self.v2[1]-self.v1[1]))
            if self.timex != self.timey:
                return False
            else:
                return True
          else:
                return False
        else:
            return False
    def collide2d(self):
        li = []
        a = self.collide1d(self.v1[0], self.v2[0])
        b = self.collide1d(self.v1[1], self.v2[1])
        for i in range(2):
            li.append(a[i])
            li.append(b[i])
        return li
#obj = collision(2, 4, 2, 6, 0 ,0 ,[4,0] , [+8,0])
#rint(obj.collide2d())
#print(obj.ifcollide2d())
#print(obj.ifcollide1d(1,2,1,-2))




