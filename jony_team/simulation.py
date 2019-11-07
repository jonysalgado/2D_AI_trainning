import pygame
from math import sin, cos, sqrt
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, PIX2M, M2PIX
from utils import *


class Simulation(object):
    """
    Represents the simulation.
    """
    def __init__(self, roomba1, roomba2, ball):
        """
        Creates the simulation.

        :param roomba: the roomba robot used in this simulation.
        :type roomba: Roomba
        """
        self.point_list = []
        self.roomba1 = roomba1
        self.roomba2 = roomba2
        self.ball = ball

    def check_collision1(self):
        """
        Checks collision between the robot and the walls.

        :return: the bumper state (if a collision has been detected).
        :rtype: bool
        """
        # Converting screen limits from pixels to meters
        width = SCREEN_WIDTH * PIX2M
        height = SCREEN_HEIGHT * PIX2M
        bumper_state = False
        # Computing the limits of the roomba's bounding box
        left = self.roomba1.pose.position.x - self.roomba1.radius
        right = self.roomba1.pose.position.x + self.roomba1.radius
        top = self.roomba1.pose.position.y - self.roomba1.radius
        bottom = self.roomba1.pose.position.y + self.roomba1.radius
        # Testing if the bounding box has hit a wall
        if left <= 0.0:
            self.roomba1.pose.position.x = self.roomba1.radius
            bumper_state = True
        if right >= width:
            self.roomba1.pose.position.x = width - self.roomba1.radius
            bumper_state = True
        if top <= 0.0:
            self.roomba1.pose.position.y = self.roomba1.radius
            bumper_state = True
        if bottom >= height:
            self.roomba1.pose.position.y = height - self.roomba1.radius
            bumper_state = True

        # check collision with other player
        dist_players = sqrt((self.roomba1.pose.position.x - self.roomba2.pose.position.x)**2+(self.roomba1.pose.position.y - self.roomba2.pose.position.y)**2)
        if dist_players <=(self.roomba1.radius + self.roomba2.radius):
            bumper_state = True
        return bumper_state

    def check_collision2(self):
        """
        Checks collision between the robot and the walls.

        :return: the bumper state (if a collision has been detected).
        :rtype: bool
        """
        # Converting screen limits from pixels to meters
        width = SCREEN_WIDTH * PIX2M
        height = SCREEN_HEIGHT * PIX2M
        bumper_state = False
        # Computing the limits of the roomba's bounding box
        left = self.roomba2.pose.position.x - self.roomba2.radius
        right = self.roomba2.pose.position.x + self.roomba2.radius
        top = self.roomba2.pose.position.y - self.roomba2.radius
        bottom = self.roomba2.pose.position.y + self.roomba2.radius
        # Testing if the bounding box has hit a wall
        if left <= 0.0:
            self.roomba2.pose.position.x = self.roomba2.radius
            bumper_state = True
        if right >= width:
            self.roomba2.pose.position.x = width - self.roomba2.radius
            bumper_state = True
        if top <= 0.0:
            self.roomba2.pose.position.y = self.roomba2.radius
            bumper_state = True
        if bottom >= height:
            self.roomba2.pose.position.y = height - self.roomba2.radius
            bumper_state = True
        # check collision with other player
        dist_players = sqrt((self.roomba1.pose.position.x - self.roomba2.pose.position.x)**2+(self.roomba1.pose.position.y - self.roomba2.pose.position.y)**2)
        if dist_players <=(self.roomba1.radius + self.roomba2.radius):
            bumper_state = True
        return bumper_state

    def check_collisionBall(self):
        """
        Checks collision between the robot and the walls.

        :return: the bumper state (if a collision has been detected).
        :rtype: bool
        """
        # Converting screen limits from pixels to meters
        width = SCREEN_WIDTH * PIX2M
        height = SCREEN_HEIGHT * PIX2M
        bumper_state = False
        # Computing the limits of the roomba's bounding box
        left = self.ball.pose.position.x - self.ball.radius
        right = self.ball.pose.position.x + self.ball.radius
        top = self.ball.pose.position.y - self.ball.radius
        bottom = self.ball.pose.position.y + self.ball.radius
        # Testing if the bounding box has hit a wall
        if left <= 0.0: 
            self.ball.pose.position.x = self.ball.radius
            bumper_state = True
        if right >= width:
            self.ball.pose.position.x = width - self.ball.radius
            bumper_state = True
        if top <= 0.0:
            self.ball.pose.position.y = self.ball.radius
            bumper_state = True
        if bottom >= height:
            self.ball.pose.position.y = height - self.ball.radius
            bumper_state = True

        # check collision with other player
        dist_player1 = sqrt((self.ball.pose.position.x - self.roomba1.pose.position.x)**2+(self.ball.pose.position.y - self.roomba1.pose.position.y)**2)
        if dist_player1 <=(self.ball.radius + self.roomba1.radius):
            bumper_state = True
        dist_player2 = sqrt((self.ball.pose.position.x - self.roomba2.pose.position.x)**2+(self.ball.pose.position.y - self.roomba2.pose.position.y)**2)
        if dist_player2 <=(self.ball.radius + self.roomba2.radius):
            bumper_state = True

        velocityBall = TransformCartesian(self.ball.linear_speed, self.ball.pose.rotation)
        velocityBall = Vector2(velocityBall.x, velocityBall.y)
        
        dirvector1 = Vector2(self.ball.pose.position.x - self.roomba1.pose.position.x, self.ball.pose.position.y - self.roomba1.pose.position.y)
        dirvector1.normalize()
        u1 = velocityBall.dot(dirvector1)
        if u1 > 0 and dist_player1 <=(self.ball.radius + self.roomba1.radius):
            return False

        dirvector2 = Vector2(self.ball.pose.position.x - self.roomba2.pose.position.x, self.ball.pose.position.y - self.roomba2.pose.position.y)
        dirvector2.normalize()
        u1 = velocityBall.dot(dirvector2)
        if u1 > 0 and dist_player2 <=(self.ball.radius + self.roomba2.radius):
            return False
        return bumper_state

    def update(self):
        """
        Updates the simulation.
        """
        # Adding roomba's current position to the movement history
        # self.point_list.append((round(M2PIX * self.roomba1.pose.position.x), round(M2PIX * self.roomba1.pose.position.y)))
        # if len(self.point_list) > 2000:
        #     self.point_list.pop(0)
        # Verifying collision
        bumper_state1 = self.check_collision1()
        bumper_state2 = self.check_collision2()
        bumper_stateBall = self.check_collisionBall()
        self.roomba1.set_bumper_state(bumper_state1)
        self.roomba2.set_bumper_state(bumper_state2)
        self.ball.set_bumper_state(bumper_stateBall)
        self.ball.posPlayer1 = self.roomba1.pose
        self.ball.posPlayer2 = self.roomba2.pose
        self.ball.speedPlayer1 = self.roomba1.linear_speed
        self.ball.speedPlayer2 = self.roomba2.linear_speed
        # Updating the robot's behavior and movement
        self.roomba1.update()
        self.roomba2.update()
        self.ball.update()

    def draw(self, window):
        """
        Draws the roomba and its movement history.

        :param window: pygame's window where the drawing will occur.
        """
        # Drawing soccer field
        pygame.draw.circle(window, (255,255,255), (round(SCREEN_WIDTH/2), round(SCREEN_HEIGHT/2)), 70, 3)
        pygame.draw.line(window, (255,255,255), (round(SCREEN_WIDTH/2), 3), (round(SCREEN_WIDTH/2), 411), 3)
        pygame.draw.line(window, (255,255,255), (3, 3), (633, 3), 3)
        pygame.draw.line(window, (255,255,255), (3, 3), (3, 411), 3)
        pygame.draw.line(window, (255,255,255), (633, 3), (633, 411), 3)
        pygame.draw.line(window, (255,255,255), (3, 411), (633, 411), 3)
        # If we have less than 2 points, we are unable to plot the movement history
        # if len(self.point_list) >= 2:
        #     pygame.draw.lines(window, (255, 0, 0), False, self.point_list, 4)
        # Computing roomba's relevant points and radius in pixels
        sx1 = round(M2PIX * self.roomba1.pose.position.x)
        sy1 = round(M2PIX * self.roomba1.pose.position.y)
        ex1 = round(M2PIX * (self.roomba1.pose.position.x +self.roomba1.radius * cos(self.roomba1.pose.rotation)))
        ey1 = round(M2PIX * (self.roomba1.pose.position.y + self.roomba1.radius * sin(self.roomba1.pose.rotation)))
        r1 = round(M2PIX * self.roomba1.radius)
        # Drawing roomba's inner circle
        pygame.draw.circle(window, (255,0,0), (sx1, sy1), r1, 0)
        # Drawing roomba's outer circle
        pygame.draw.circle(window, (50, 50, 50), (sx1, sy1), r1, 4)
        # Drawing roomba's orientation
        pygame.draw.line(window, (50, 50, 50), (sx1, sy1), (ex1, ey1), 3)

        # roomba 2
        sx2 = round(M2PIX * self.roomba2.pose.position.x)
        sy2 = round(M2PIX * self.roomba2.pose.position.y)
        ex2 = round(M2PIX * (self.roomba2.pose.position.x +self.roomba2.radius * cos(self.roomba2.pose.rotation)))
        ey2 = round(M2PIX * (self.roomba2.pose.position.y + self.roomba2.radius * sin(self.roomba2.pose.rotation)))
        r2 = round(M2PIX * self.roomba2.radius)
        # Drawing roomba's inner circle
        pygame.draw.circle(window, (255,0,0), (sx2, sy2), r2, 0)
        # Drawing roomba's outer circle
        pygame.draw.circle(window, (50, 50, 50), (sx2, sy2), r2, 4)
        # Drawing roomba's orientation
        pygame.draw.line(window, (50, 50, 50), (sx2, sy2), (ex2, ey2), 3)

        # ball
        sxB = round(M2PIX * self.ball.pose.position.x)
        syB = round(M2PIX * self.ball.pose.position.y)
        exB = round(M2PIX * (self.ball.pose.position.x +self.ball.radius * cos(self.ball.pose.rotation)))
        eyB = round(M2PIX * (self.ball.pose.position.y + self.ball.radius * sin(self.ball.pose.rotation)))
        rB = round(M2PIX * self.ball.radius)
        # Drawing roomba's inner circle
        pygame.draw.circle(window, (255,255,255), (sxB, syB), rB, 0)
        # Drawing roomba's outer circle
        pygame.draw.circle(window, (255, 255, 255), (sxB, syB), rB, 4)

        
def draw(simulation, window):
    """
    Redraws the pygame's window.

    :param simulation: the simulation object.
    :param window: pygame's window where the drawing will occur.
    """
    window.fill((35,142,35))
    simulation.draw(window)
    pygame.display.update()

