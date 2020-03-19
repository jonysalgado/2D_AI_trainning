from constants import *
from utils import Pose
from player import Roomba
from ball import Ball
from simulation import *
from state_machine import FiniteStateMachine, MoveForwardState
from state_machine_ball import FiniteStateMachineBall, MoveForwardStateBall
import numpy as np
pygame.init()

window = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

pygame.display.set_caption("Jony team")

clock = pygame.time.Clock()

behavior1 = FiniteStateMachine(MoveForwardState())
behavior2 = FiniteStateMachine(MoveForwardState())
behavierBall = FiniteStateMachineBall(MoveForwardStateBall(False))
pose1 = Pose(PIX2M * SCREEN_WIDTH/3, PIX2M * SCREEN_HEIGHT/2, 0)
pose2 = Pose(0, 0, pi) # Pose(PIX2M * 2 * SCREEN_WIDTH/3, PIX2M * SCREEN_HEIGHT/2, pi)
poseBall = Pose(PIX2M * SCREEN_WIDTH / 2.0, PIX2M * SCREEN_HEIGHT / 2.0, 0)
player = np.array([Roomba(pose1, 1.0, 2.0, RADIUS_PLAYER, behavior1), Roomba(
    pose2, 0.0, 2.0, RADIUS_PLAYER, behavior2)])
ball = Ball(poseBall, 1.0, 100, RADIUS_BALL, behavierBall)
simulation = Simulation(player, ball)

# logo and font
logo = pygame.image.load('team_logo.xpm')
font = pygame.font.SysFont('Comic Sans MS', 30)


run = True
while run:
    clock.tick(FREQUENCY)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    simulation.update()
    draw(simulation, window, logo, font)
    

pygame.quit()
