import pygame
from pygame.rect import Rect
from math import sin, cos, sqrt
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, PIX2M, M2PIX
from utils import *


class Simulation(object):
    """
    Represents the simulation.
    """
    def __init__(self, player, ball):
        """
        Creates the simulation.

        :param roomba: the roomba robot used in this simulation.
        :type roomba: Roomba
        """
        self.point_list = []
        self.player = player
        self.ball = ball

    def check_collision(self, num1, num2):
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
        left = self.player[num1].pose.position.x - self.player[num1].radius
        right = self.player[num1].pose.position.x + self.player[num1].radius
        top = self.player[num1].pose.position.y - self.player[num1].radius
        bottom = self.player[num1].pose.position.y + self.player[num1].radius
        # Testing if the bounding box has hit a wall
        if left <= 0.0:
            self.player[num1].pose.position.x = self.player[num1].radius
            bumper_state = True
        if right >= width:
            self.player[num1].pose.position.x = width - self.player[num1].radius
            bumper_state = True
        if top <= 0.0:
            self.player[num1].pose.position.y = self.player[num1].radius
            bumper_state = True
        if bottom >= height:
            self.player[num1].pose.position.y = height - self.player[num1].radius
            bumper_state = True

        # check collision with other player
        dist_players = sqrt((self.player[num1].pose.position.x - self.player[num2].pose.position.x)**2+(self.player[num1].pose.position.y - self.player[num2].pose.position.y)**2)
        if dist_players <=(self.player[num1].radius + self.player[num2].radius):
            bumper_state = True
        return bumper_state

    
    def check_collisionBall(self):
        """
        Checks collision between the ball with the walls and other players.

        :return: the bumper state (if a collision has been detected).
        :rtype: bool
        """
        num1 = 0
        num2 = 1
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
        dist_player1 = sqrt((self.ball.pose.position.x - self.player[num1].pose.position.x)**2+(self.ball.pose.position.y - self.player[num1].pose.position.y)**2)
        if dist_player1 <=(self.ball.radius + self.player[num1].radius):
            bumper_state = True
        dist_player2 = sqrt((self.ball.pose.position.x - self.player[num2].pose.position.x)**2+(self.ball.pose.position.y - self.player[num2].pose.position.y)**2)
        if dist_player2 <=(self.ball.radius + self.player[num2].radius):
            bumper_state = True

        velocityBall = TransformCartesian(self.ball.linear_speed, self.ball.pose.rotation)
        velocityBall = Vector2(velocityBall.x, velocityBall.y)
        
        dirvector1 = Vector2(self.ball.pose.position.x - self.player[num1].pose.position.x, self.ball.pose.position.y - self.player[num1].pose.position.y)
        dirvector1.normalize()
        u1 = velocityBall.dot(dirvector1)
        if u1 > 0 and dist_player1 <=(self.ball.radius + self.player[num1].radius):
            return False

        dirvector2 = Vector2(self.ball.pose.position.x - self.player[num2].pose.position.x, self.ball.pose.position.y - self.player[num2].pose.position.y)
        dirvector2.normalize()
        u1 = velocityBall.dot(dirvector2)
        if u1 > 0 and dist_player2 <=(self.ball.radius + self.player[num2].radius):
            return False
        return bumper_state
    
    # def check_goal(self):


    def update(self):
        """
        Updates the simulation.
        """
        # Adding roomba's current position to the movement history
        # self.point_list.append((round(M2PIX * self.player[num1].pose.position.x), round(M2PIX * self.player[num1].pose.position.y)))
        # if len(self.point_list) > 2000:
        #     self.point_list.pop(0)
        # Verifying collision
        num1 = 0
        num2 = 1
        bumper_state1 = self.check_collision(0,1)
        bumper_state2 = self.check_collision(1,0)
        bumper_stateBall = self.check_collisionBall()
        self.player[num1].set_bumper_state(bumper_state1)
        self.player[num2].set_bumper_state(bumper_state2)
        self.ball.set_bumper_state(bumper_stateBall)
        self.ball.posPlayer = [self.player[num1].pose,self.player[num2].pose]
        self.ball.speedPlayer = [self.player[num1].linear_speed,self.player[num2].linear_speed]
        # Updating the robot's behavior and movement
        self.player[num1].update()
        self.player[num2].update()
        self.ball.update()

    def draw(self, window):
        """
        Draws the roomba and its movement history.

        :param window: pygame's window where the drawing will occur.
        """
        num1 = 0
        num2 = 1
        # Drawing soccer field
        pygame.draw.circle(window, (255,255,255), (round(SCREEN_WIDTH/2), round(SCREEN_HEIGHT/2)), 70, 3)
        pygame.draw.line(window, (255,255,255), (round(SCREEN_WIDTH/2), 30), (round(SCREEN_WIDTH/2), SCREEN_HEIGHT - 30), 3)
        pygame.draw.line(window, (255,255,255), (30, 30), (round(SCREEN_WIDTH)-30, 30), 3)
        pygame.draw.line(window, (255,255,255), (30, 30), (30, round(SCREEN_HEIGHT)-30), 3)
        pygame.draw.line(window, (255,255,255), (round(SCREEN_WIDTH)-30, 30), (round(SCREEN_WIDTH)-30, round(SCREEN_HEIGHT)-30), 3)
        pygame.draw.line(window, (255,255,255), (30, round(SCREEN_HEIGHT)-30), (round(SCREEN_WIDTH)-30, round(SCREEN_HEIGHT)-30), 3)
        # If we have less than 2 points, we are unable to plot the movement historypygame.draw.line(window, (255,255,255), (30, round(SCREEN_HEIGHT)-30), (round(SCREEN_WIDTH)-30, round(SCREEN_HEIGHT)-30), 3)
        # if len(self.point_list) >= 2:
        #     pygame.draw.lines(window, (255, 0, 0), False, self.point_list, 4)
        # Computing roomba's relevant points and radius in pixels
        sx1 = round(M2PIX * self.player[num1].pose.position.x)
        sy1 = round(M2PIX * self.player[num1].pose.position.y)
        ex1 = round(M2PIX * (self.player[num1].pose.position.x +self.player[num1].radius * cos(self.player[num1].pose.rotation)))
        ey1 = round(M2PIX * (self.player[num1].pose.position.y + self.player[num1].radius * sin(self.player[num1].pose.rotation)))
        r1 = round(M2PIX * self.player[num1].radius)
        # Drawing roomba's inner circle
        pygame.draw.circle(window, (255,0,0), (sx1, sy1), r1, 0)
        # Drawing roomba's outer circle
        pygame.draw.circle(window, (50, 50, 50), (sx1, sy1), r1, 4)
        # Drawing roomba's orientation
        pygame.draw.line(window, (50, 50, 50), (sx1, sy1), (ex1, ey1), 3)

        # roomba 2
        sx2 = round(M2PIX * self.player[num2].pose.position.x)
        sy2 = round(M2PIX * self.player[num2].pose.position.y)
        ex2 = round(M2PIX * (self.player[num2].pose.position.x +self.player[num2].radius * cos(self.player[num2].pose.rotation)))
        ey2 = round(M2PIX * (self.player[num2].pose.position.y + self.player[num2].radius * sin(self.player[num2].pose.rotation)))
        r2 = round(M2PIX * self.player[num2].radius)
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
        # Drawing soccer goal
        pygame.draw.rect(window, (0, 0, 0), Rect(0, round(SCREEN_HEIGHT)/2-100, 30, 200))
        pygame.draw.rect(window, (0, 0, 0), Rect(round(SCREEN_WIDTH)-30, round(SCREEN_HEIGHT)/2-100, 30, 200))

        
def draw(simulation, window, logo):
    """
    Redraws the pygame's window.

    :param simulation: the simulation object.
    :param window: pygame's window where the drawing will occur.
    """
    window.fill((35,142,35))
    window.blit(logo, (round(SCREEN_WIDTH)/2+100,40))
    simulation.draw(window)
    pygame.display.update()

