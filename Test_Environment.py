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
import pygame
import Radial_Object as RO
import surface as SU
import physics as phy
import random

pygame.init()
infoObject = pygame.display.Info()
pygame.display.set_caption("Test Environment")
screen = pygame.display.set_mode((infoObject.current_w, int(infoObject.current_w/2)))
clock = pygame.time.Clock()

width = infoObject.current_w
height = infoObject.current_w/2
running = True
Radial_Object_List = []
Surface_List = []
Physics_Model_List = [phy.newtonian_physics_model(Gravitational_Constant=1000)]
Gravity_List = [Physics_Model_List[i].Get_Gravity() for i in range(len(Physics_Model_List))]
Radial_Object_List.append(RO.Radial_Object([width/2-200+400*random.random(), height/2-200+400*random.random()], [10, 0], 1, 0, 5, False, [255, 0, 0]))
Radial_Object_List.append(RO.Radial_Object([width/2-200+400*random.random(), height/2-200+400*random.random()], [0, 10], 1, 0, 5, False, [0, 255, 0]))
Radial_Object_List.append(RO.Radial_Object([width/2-200+400*random.random(), height/2-200+400*random.random()], [-10, 0], 1, 0, 5, False, [0, 0, 255]))
Radial_Object_List.append(RO.Radial_Object([width/2-200+400*random.random(), height/2-200+400*random.random()], [0, -10], 1, 0, 5, False, [0, 255, 255]))
Radial_Object_List.append(RO.Radial_Object([width/2-200+400*random.random(), height/2-200+400*random.random()], [10, 0], 1, 0, 5, False, [255, 0, 255]))
Radial_Object_List.append(RO.Radial_Object([width/2-200+400*random.random(), height/2-200+400*random.random()], [0, 10], 1, 0, 5, False, [255, 255, 0]))
Radial_Object_List.append(RO.Radial_Object([width/2-200+400*random.random(), height/2-200+400*random.random()], [0, -10], 1, 0, 5, False, [255, 255, 255]))
Surface_List.append(SU.Surface([[0, 0], [width, 0]], 2))
Surface_List.append(SU.Surface([[width, 0], [width, height]], 2))
Surface_List.append(SU.Surface([[width, height], [0, height]], 2))
Surface_List.append(SU.Surface([[0, 0], [0, height]], 2))

while running:
	clock.tick(60)
	
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False
		if event.type == pygame.KEYUP:
			if event.key == pygame.K_RETURN:
				pass
	
	screen.fill((0, 0, 0))
	
	for i in Radial_Object_List:
		force = [0, 0]
		values = {
		"0.0": i.mass,
		"0.1": i.charge 
		}
		for j in range(Physics_Model_List[0].dimensions):
			values["0.2."+str(j)] = i.position[j]
		for j in range(Physics_Model_List[0].dimensions):
			values["0.3."+str(j)] = i.velocity[j]
		for j in Radial_Object_List:
			if not j == i:
				values["1.0"] = j.mass
				values["1.1"] = j.charge
				for k in range(Physics_Model_List[0].dimensions):
					values["1.2."+str(k)] = j.position[k]
				for k in range(Physics_Model_List[0].dimensions):
					values["1.3."+str(k)] = j.velocity[k]
				temp = [Gravity_List[0][i](values) for i in range(len(Gravity_List[0]))]
				force = [force[i]+temp[i] for i in range(len(temp))]
				
		Physics_Model_List[0].Update_Kinematics(i, force=force)
	
	for i in Radial_Object_List:
		pygame.draw.circle(screen, i.color, i.position, i.radius)
	
	Physics_Model_List[0].Surface_Collision(Radial_Object_List, Surface_List)
	
	pygame.display.update()
