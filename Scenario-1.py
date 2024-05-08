import glob
import csv
import os
import sys
import random
import time
import cv2
import numpy as np
import math
import utility as ut
import model as md
import tensorflow as tf
from keras.models import load_model
import matplotlib.pyplot as plt
from keras import Sequential
from collections import deque
from keras.layers import Dense, Dropout, Conv2D, MaxPooling2D, Activation, Flatten
from keras.optimizers import Adam
import matplotlib.pyplot as plt
from keras.activations import relu, linear
from keras.callbacks import TensorBoard
from scipy.spatial import distance



np.random.seed(32)
random.seed(32)

try:
	sys.path.append(glob.glob('../../../carla/dist/carla-*%d.%d-%s.egg' % (
		sys.version_info.major,
		sys.version_info.minor,
		'win-amd64' if os.name == 'nt' else 'linux-x86_64'))[0])
except IndexError:
	pass
import carla


class CarlaVehicle(object):
	"""
	class responsable of:
		-spawning the ego vehicle
		-destroy the created objects
		-providing environment for RL training
	"""

	#Class Variables
	SHOW_CAM = SHOW_PREVIEW
	front_camera = None
	def __init__(self):
		self.client = carla.Client('127.0.0.1',2000)
		self.client.set_timeout(5.0)
		self.im_width = IM_WIDTH
		self.im_height = IM_HEIGHT

	def reset(self,Norender):
		'''reset function to reset the environment before 
		the begining of each episode
		:params Norender: to be set true during training
		'''
		self.collision_hist = []
		self.world = self.client.get_world()
		self.map = self.world.get_map()

		#Code for setting no rendering mode
		if Norender:
			settings = self.world.get_settings()
			settings.no_rendering_mode = False
			self.world.apply_settings(settings)

		self.actor_list = []
		self.blueprint_library = self.world.get_blueprint_library()
		self.bp = self.blueprint_library.filter("vehicle.lincoln.mkz2017")[0]
		self.bp1 = self.blueprint_library.filter("vehicle.audi.a2")[0]
		self.bp2 = self.blueprint_library.filter("vehicle.audi.etron")[0]
		self.bp3 = self.blueprint_library.filter("vehicle.citroen.c3")[0]
		self.bp4 = self.blueprint_library.filter("vehicle.audi.a2")[0]
		self.static_prop = self.blueprint_library.filter("static.prop.streetbarrier")[0]
		self.pedes = self.blueprint_library.filter("walker.pedestrian.0010")[0]


		#static overtaking with obstacle

		# traffic with multi-obstacle and front vehicle
		init_loc = carla.Location(x=-64.2040, y=134.322726, z=1)
		# traffic with multi-obstacle
		# init_loc = carla.Location(x=-58.2040, y=138.322726, z=1)
		# traffic
		# init_loc = carla.Location(x=-38.2040, y=138.322726, z=1) 
		# init_loc = carla.Location(x = 56.73741, y = 133.322726, z=1)
		# init_loc = carla.Location(x=71.750694, y=131.111465, z=1)
		# init_pos = carla.Transform(init_loc, carla.Rotation(pitch=0.094270, yaw=-3.097657, roll=-1.246277))
		init_pos = carla.Transform(init_loc, carla.Rotation(yaw=0))




		#First scenario test
		# self.target_loc_straight = carla.Location(x = 100, y = 134.322726, z=1)

		prop_1_loc = carla.Transform(carla.Location(x=-26.970741, y=138.322726, z=1), carla.Rotation(pitch=0.119906, yaw=-0.817204, roll=0.000000))
		prop_1 = self.world.spawn_actor(self.bp3, prop_1_loc)
		self.actor_list.append(prop_1)




		control =  carla.VehicleControl()
		control.steer = 0
		control.throttle = 0.17
		prop_1.apply_control(control)









