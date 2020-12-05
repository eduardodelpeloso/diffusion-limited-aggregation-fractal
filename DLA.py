                                                                                        #!/usr/bin/env python3
# -*- coding: utf-8 -*-=
"""
Created on Sun Aug 30 23:01:52 2020

@author: eduardo
"""

import random
import math
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
import seaborn as sns

def distance(x_center, y_center, x_pos, y_pos):
    return (x_pos - x_center) ** 2 + (y_pos - y_center) ** 2

#@profile
def do_it_all():
    
    particles_file = 'particles_10k.txt'
    centers_file = 'centers_10k.txt'
    counts_file = 'counts_10k.txt'
    
    num_target = 10000

    num_actual = 1
    
    max_radius = 0
    delta_radius = 50
    
    x_center = 0
    y_center = 0
    
    particles = {(x_center, y_center)}
    centers = [(x_center, y_center)]
    
    while num_actual < num_target:
    
        # Particle's initianl position in a random location over
        # the circle of radius "radius" centered in (x_center, y_center)
        initial_position = random.random()
        x_pos = int(x_center + (max_radius + delta_radius) * math.cos(initial_position * 2.0 * math.pi))
        y_pos = int(y_center + (max_radius + delta_radius) * math.sin(initial_position * 2.0 * math.pi))
        
        particle_walks = True
    
        while particle_walks:
    
            # Random walk in a square grid
            move = random.random()   

            if move < 0.25:
                x_pos += 1
            elif move < 0.50:
                x_pos -= 1
            elif move < 0.75:
                y_pos += 1
            else:
                y_pos -= 1
                
            dist = distance(x_center, y_center, x_pos, y_pos)    
                
            # If particle wanders too far way from the Brownian tree,
            # begin again with new particle
            
            if  dist > (max_radius + 2 * delta_radius) ** 2:
                break
                
                
            # If particle gets caught in the Brownian tree
            if (x_pos + 1, y_pos) in particles or \
               (x_pos - 1, y_pos) in particles or \
               (x_pos, y_pos + 1) in particles or \
               (x_pos, y_pos - 1) in particles:
                   
                    # Append particle to tree
                    particles.add((x_pos, y_pos))
            
                    # Calculate the new center of mass
                    x_center = 0
                    y_center = 0
                    for particle in particles:
                        x_center += particle[0]
                        y_center += particle[1]
                    x_center = int(0.5 + x_center / len(particles))
                    y_center = int(0.5 + y_center / len(particles))
                    centers.append((x_center, y_center))
                    
                    num_actual += 1
                    particle_walks = False
                    
                    sqrt_dist = math.sqrt(dist)
                    
                    if sqrt_dist > max_radius:
                        max_radius = sqrt_dist
    
                    print("num_actual = ", num_actual)
                    
    with open(particles_file, 'w') as fp:
        fp.write('\n'.join('%s,%s' % x for x in particles))
        
    with open(centers_file, 'w') as fp:
        fp.write('\n'.join('%s,%s' % x for x in centers))
        
    
    dists_centers = []
    for center in centers:
        dists_centers.append(math.sqrt(distance(0, 0, center[0], center[1])))
            
    print("max_dist_centers: ", max(dists_centers))
    
    dists_particles = []
    for particle in particles:
        dists_particles.append(math.sqrt(distance(x_center, y_center, particle[0], particle[1])))
        
    
    counts = []
    for count_radius in np.arange(int(0.5 + 2.0 * max(dists_centers)), int(0.5 * max(dists_particles))):
        count = 0
        for dist_particle in  dists_particles:
            if dist_particle <= count_radius:
                count += 1
        counts.append((math.log10(count_radius), math.log10(count)))

    with open(counts_file, 'w') as fp:
        fp.write('\n'.join('%s,%s' % x for x in counts))

    df = pd.read_csv(counts_file, header=None)
    x = df[0].values.reshape(-1, 1)
    y = df[1].values.reshape(-1, 1)
    
    regressor = LinearRegression()  
    regressor.fit(x, y)
    
    print("DLA fractal dimension = ", round(regressor.coef_[0][0], 2))
        
if __name__ == '__main__':

    do_it_all()
