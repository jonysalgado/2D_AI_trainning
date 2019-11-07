from math import pi
# Simulation Parameters
# soccer field (105,68) x 6
SCREEN_WIDTH = 636
SCREEN_HEIGHT = 414
PIX2M = 0.01  # factor to convert from pixels to meters
M2PIX = 100.0  # factor to convert from meters to pixels

# Sample Time Parameters
FREQUENCY = 60.0  # simulation frequency
SAMPLE_TIME = 1.0 / FREQUENCY  # simulation sample time

# Behavior Parameters
MOVE_FORWARD_TIME = 3.0  # time moving forward before switching to the spiral behavior
MOVE_IN_SPIRAL_TIME = 20.0  # time moving in spiral before switching back to moving forward
GO_BACK_TIME = 0.5  # time going back after hitting a wall
FORWARD_SPEED = 0.5  # default linear speed when going forward
BACKWARD_SPEED = -0.1 # default backward speed when going back after hitting a wall
INITIAL_RADIUS_SPIRAL = 0.2  # initial spiral radius
SPIRAL_FACTOR = 0.05  # factor used to make the spiral grow while the time passes
ANGULAR_SPEED = 100  # default angular speed
# Ball Parameters
FRICTION_SLOWDOWN = 0.5
REFLECTION = pi
BALL_MASS = 0.450
# players Parameters
RADIUS_PLAYER1 = 0.34 / 2.0
RADIUS_PLAYER2 = 0.30 / 2.0
PLAYER_MASS = 75
# world Parameters
GRAVITY_ACCLERATION = 9.8
