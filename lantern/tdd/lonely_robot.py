class Asteroid:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Robot:
    def __init__(self, x, y, asteroid, direction):
        self.x = x
        self.y = y
        self.direction = direction
        self.asteroid = asteroid
        if self.x > self.asteroid.x:
            raise MissAsteroidError()
        if self.y > self.asteroid.y:
            raise MissAsteroidError()

    def check_robot_on_an_asteroid(self):
        if self.x > self.asteroid.x or self.y > self.asteroid.y or self.x < 0 or self.y < 0:
            raise RobotFallFromAsteroidError()

    def turn_left(self):
        turns = dict(E="N", N="W", W="S", S="E")
        self.direction = turns[self.direction]

    def turn_right(self):
        turns = dict(N="E", E="S", S="W", W="N")
        self.direction = turns[self.direction]

    def move_forward(self):
        move_forward = dict(N=(self.x, self.y + 1), E=(self.x + 1, self.y), S=(self.x, self.y - 1),
                            W=(self.x - 1, self.y))
        self.x, self.y = move_forward[self.direction]
        self.check_robot_on_an_asteroid()

    def move_backward(self):
        move_backward = dict(N=(self.x, self.y - 1), E=(self.x - 1, self.y), S=(self.x, self.y + 1),
                             W=(self.x + 1, self.y))
        self.x, self.y = move_backward[self.direction]
        self.check_robot_on_an_asteroid()


class MissAsteroidError(Exception):
    pass


class RobotFallFromAsteroidError(Exception):
    pass
