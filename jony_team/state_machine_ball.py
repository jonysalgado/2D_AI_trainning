import random
import math
from constants import *
from utils import *


class FiniteStateMachineBall(object):
    """
    A finite state machine.
    """
    def __init__(self, state):
        self.state = state

    def change_state(self, new_state):
        self.state = new_state

    def update(self, agent):
        
        self.state.check_transition(agent, self)
        self.state.execute(agent)
    
 


class State(object):
    """
    Abstract state class.
    """
    def __init__(self, state_name):
        """
        Creates a state.

        :param state_name: the name of the state.
        :type state_name: str
        """
        self.state_name = state_name

    def check_transition(self, agent, fsm):
        """
        Checks conditions and execute a state transition if needed.

        :param agent: the agent where this state is being executed on.
        :param fsm: finite state machine associated to this state.
        """
        raise NotImplementedError("This method is abstract and must be implemented in derived classes")

    def execute(self, agent):
        """
        Executes the state logic.

        :param agent: the agent where this state is being executed on.
        """
        raise NotImplementedError("This method is abstract and must be implemented in derived classes")


class MoveForwardStateBall(State):
    def __init__(self, collidePlayer):
        super().__init__("MoveForward")
        self.collidePlayer = collidePlayer
    def check_transition(self, agent, state_machine):  
        if agent.get_bumper_state():
            state_machine.change_state(Reflection())

      


        

    def execute(self, agent):
        if self.collidePlayer:
            agent.set_cont_friction(True)
        else:
            agent.set_cont_friction(False, 1)
        velocity = math.fabs(agent.linear_speed)-math.fabs(GRAVITY_ACCLERATION*FRICTION_SLOWDOWN*(agent.cont_friction)**(1/3)*SAMPLE_TIME/100)
        if velocity < 0:
            velocity = 0
        # print(velocity, agent.linear_speed, agent.cont_friction)
        agent.set_velocity(velocity,0)
       
        agent.move()

class Reflection(State):
    def __init__(self):
        super().__init__("Reflection")
        self.collidePlayer = False
    def check_transition(self, agent, state_machine):  
        self.rotation(agent)
        state_machine.change_state(MoveForwardStateBall(self.collidePlayer))

    
    def rotation(self, agent):
        # detect collision with walls
        coordinate = TransformCartesian(agent.linear_speed, agent.pose.rotation)
        # Computing the limits of the roomba's bounding box
        width = SCREEN_WIDTH * PIX2M
        height = SCREEN_HEIGHT * PIX2M
        left = agent.pose.position.x - agent.radius
        right = agent.pose.position.x + agent.radius
        top = agent.pose.position.y - agent.radius
        bottom = agent.pose.position.y + agent.radius
        # print(agent.pose.rotation, coordinate.x, coordinate.y)
        # Testing if the bounding box has hit a wall
        if left <= 0.0 or right >= width: 
            if math.fabs(agent.pose.rotation) < 1.0e-3:
                agent.pose.rotation = math.pi
            else:
                agent.pose.rotation = TransformPolar(-1 * coordinate.x, coordinate.y).rotation
        if top <= 0.0 or bottom >= height:
            agent.pose.rotation = TransformPolar(coordinate.x, -1*coordinate.y).rotation

        # Collision with other players
        dist_player1 = math.sqrt((agent.pose.position.x - agent.posPlayer1.position.x)**2+(agent.pose.position.y - agent.posPlayer1.position.y)**2)
        dist_player2 = math.sqrt((agent.pose.position.x - agent.posPlayer2.position.x)**2+(agent.pose.position.y - agent.posPlayer2.position.y)**2)
        if dist_player1 <=(agent.radius + RADIUS_PLAYER1):
            self.collidePlayer1(agent)
            self.collidePlayer = True
        if dist_player2 <=(agent.radius + RADIUS_PLAYER2):
            self.collidePlayer2(agent)
            self.collidePlayer = True



    def collidePlayer1(self, agent):
        if agent.linear_speed < 1.0e-2:
            agent.linear_speed = agent.speedPlayer1
        velocityBall = TransformCartesian(agent.linear_speed, agent.pose.rotation)
        velocityBall = Vector2(velocityBall.x, velocityBall.y)
        velocityPlayer1 = TransformCartesian(agent.speedPlayer1, agent.posPlayer1.rotation)
        velocityPlayer1 = Vector2(velocityPlayer1.x, velocityPlayer1.y)
        dirvector = Vector2(agent.pose.position.x - agent.posPlayer1.position.x, agent.pose.position.y - agent.posPlayer1.position.y)
        dirvector.normalize()
        u1 = velocityBall.dot(dirvector)
        u1normal = Vector2(velocityBall.x - u1 * dirvector.x,velocityBall.y - u1 * dirvector.y)
        u2 = velocityPlayer1.dot(dirvector)
        v1 = ((BALL_MASS - PLAYER_MASS) * u1 + 2 * BALL_MASS * u2) / ( BALL_MASS + PLAYER_MASS)
        vfinal = Vector2(u1normal.x + v1 * dirvector.x,u1normal.y + v1 * dirvector.y)
        vfinal = TransformPolar(vfinal.x, vfinal.y)
        agent.linear_speed, agent.pose.rotation = vfinal.linear_speed, vfinal.rotation
        print(agent.linear_speed, agent.pose.rotation)

    def collidePlayer2(self, agent):
        if agent.linear_speed < 1.0e-2:
            agent.linear_speed = agent.speedPlayer2
        velocityBall = TransformCartesian(agent.linear_speed, agent.pose.rotation)
        velocityBall = Vector2(velocityBall.x, velocityBall.y)
        velocityPlayer2 = TransformCartesian(agent.speedPlayer2, agent.posPlayer2.rotation)
        velocityPlayer2 = Vector2(velocityPlayer2.x, velocityPlayer2.y)
        dirvector = Vector2(agent.pose.position.x - agent.posPlayer2.position.x, agent.pose.position.y - agent.posPlayer2.position.y)
        dirvector.normalize()
        u1 = velocityBall.dot(dirvector)
        u1normal = Vector2(velocityBall.x - u1 * dirvector.x,velocityBall.y - u1 * dirvector.y)
        u2 = velocityPlayer2.dot(dirvector)
        v1 = ((BALL_MASS - PLAYER_MASS) * u1 + 2 * BALL_MASS * u2) / ( BALL_MASS + PLAYER_MASS)
        vfinal = Vector2(u1normal.x + v1 * dirvector.x,u1normal.y + v1 * dirvector.y)
        vfinal = TransformPolar(vfinal.x, vfinal.y)
        agent.linear_speed, agent.pose.rotation = vfinal.linear_speed, vfinal.rotation
        
        

    def execute(self, agent):
       
        agent.move()

    

