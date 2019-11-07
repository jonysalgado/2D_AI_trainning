def rotation(self, agent):
        # detect collision with walls
        width = SCREEN_WIDTH * PIX2M
        height = SCREEN_HEIGHT * PIX2M
        left = agent.pose.position.x - agent.radius
        right = agent.pose.position.x + agent.radius
        top = agent.pose.position.y - agent.radius
        bottom = agent.pose.position.y + agent.radius
        beta1 = math.atan((agent.posPlayer1.position.y - agent.pose.position.y)/(agent.posPlayer1.position.x - agent.pose.position.x))
        dist_player1 = math.sqrt((agent.pose.position.x - agent.posPlayer1.position.x)**2+(agent.pose.position.y - agent.posPlayer1.position.y)**2)
        collision1 = False
        if dist_player1 <=(agent.radius + RADIUS_PLAYER1):
            collision1 = True
        beta2 = math.atan((agent.posPlayer2.position.y - agent.pose.position.y)/(agent.posPlayer2.position.x - agent.pose.position.x))
        dist_player2 = math.sqrt((agent.pose.position.x - agent.posPlayer2.position.x)**2+(agent.pose.position.y - agent.posPlayer2.position.y)**2)
        collision2 = False
        if dist_player2 <=(agent.radius + RADIUS_PLAYER2):
            collision2 = True

        if left <= 0.0 or (math.fabs(beta1 - math.pi) < 1.0e-3 and collision1) or (math.fabs(beta2 - math.pi) < 1.0e-3 and collision2): 
            if math.fabs(agent.pose.rotation - math.pi) > 1.0e-3:
                agent.pose.rotation += 3*math.pi - 2*agent.pose.rotation
            else:
                agent.pose.rotation *= -1
        elif right >= width or (math.fabs(beta1) < 1.0e-3 and collision1) or (math.fabs(beta2) < 1.0e-3 and collision2):
            if math.fabs(agent.pose.rotation) > 1.0e-3:
                agent.pose.rotation += math.pi - 2*agent.pose.rotation
            else:
                agent.pose.rotation += math.pi
        elif top <= 0.0 or (math.fabs(beta1 - 3*math.pi/2.0) < 1.0e-3 and collision1) or (math.fabs(beta2 - 3*math.pi/2.0) < 1.0e-3 and collision2):
            if math.fabs(agent.pose.rotation - math.pi/2.0) > 1.0e-3:
                agent.pose.rotation += 2*math.pi - 2*agent.pose.rotation
            else:
                agent.pose.rotation += math.pi/2.0
        elif bottom >= height or (math.fabs(beta1 - math.pi/2.0) < 1.0e-3 and collision1) or (math.fabs(beta2 - math.pi/2.0) < 1.0e-3 and collision2):
            if math.fabs(agent.pose.rotation - 3*math.pi/2.0) > 1.0e-3:
                agent.pose.rotation += 4*math.pi - 2*agent.pose.rotation
            else:
                agent.pose.rotation += math.pi/2.0
        elif beta1 > 2*math.pi and beta1 < 3*math.pi/2.0 and collision1:
            agent.pose.rotation += 5*math.pi - 2*agent.pose.rotation - beta1
        elif beta1 > 0 and beta1 < math.pi/2.0 and collision1:
            agent.pose.rotation += math.pi - 2*agent.pose.rotation + beta1
        elif beta1 > math.pi/2.0 and beta1 < math.pi and collision1:
            agent.pose.rotation += math.pi - 2*agent.pose.rotation + 2*beta1
        elif beta1 > math.pi and beta1 < 3*math.pi/2.0 and collision1:
            agent.pose.rotation += math.pi - 2*agent.pose.rotation + 2*beta1
        elif beta2 > 2*math.pi and beta2 < 3*math.pi/2.0 and collision2:
            agent.pose.rotation += 5*math.pi - 2*agent.pose.rotation - beta2
        elif beta2 > 0 and beta2 < math.pi/2.0 and collision2:
            agent.pose.rotation += math.pi - 2*agent.pose.rotation + beta2
        elif beta2 > math.pi/2.0 and beta2 < math.pi and collision2:
            agent.pose.rotation += math.pi - 2*agent.pose.rotation + 2*beta2
        elif beta2 > math.pi and beta2 < 3*math.pi/2.0 and collision2:
            agent.pose.rotation += math.pi - 2*agent.pose.rotation + 2*beta2
        if collision1:
            agent.linear_speed += agent.speedPlayer1
        if collision2:
            agent.linear_speed += agent.speedPlayer2