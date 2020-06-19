import pytest
from lonely_robot import Robot, Asteroid, MissAsteroidError, RobotFallFromAsteroidError


class TestRobotCreation:
    def test_parameters(self):
        x, y = 10, 15
        asteroid = Asteroid(x + 1, y + 1)
        direction = "E"
        robot = Robot(x, y, asteroid, direction)
        assert robot.x == 10
        assert robot.y == 15
        assert robot.direction == direction
        assert robot.asteroid == asteroid

    @pytest.mark.parametrize(
        "asteroid_size,robot_coordinates",
        (
                ((15, 25), (26, 30)),
                ((15, 25), (26, 24)),
                ((15, 25), (15, 27)),
        )
    )
    def test_check_if_robot_on_asteroid(self, asteroid_size, robot_coordinates):
        with pytest.raises(MissAsteroidError):
            asteroid = Asteroid(*asteroid_size)
            Robot(*robot_coordinates, asteroid, "W")


class TestTurns:
    x, y = 10, 15
    asteroid = Asteroid(x + 1, y + 1)

    @pytest.mark.parametrize(
        "current_direction,expected_direction",
        (
                ("N", "W"),
                ("W", "S"),
                ("S", "E"),
                ("E", "N"),
        )
    )
    def test_turn_left(self, current_direction, expected_direction):
        robot = Robot(self.x, self.y, self.asteroid, current_direction)
        robot.turn_left()
        assert robot.direction == expected_direction

    @pytest.mark.parametrize(
        "current_direction,expected_direction",
        (
                ("W", "N"),
                ("N", "E"),
                ("E", "S"),
                ("S", "W"),
        )
    )
    def test_turn_right(self, current_direction, expected_direction):
        robot = Robot(self.x, self.y, self.asteroid, current_direction)
        robot.turn_right()
        assert robot.direction == expected_direction


class TestMove:
    x, y = 10, 15
    asteroid = Asteroid(11, 16)
    current_direction = "W"

    @pytest.mark.parametrize(
        "current_direction,current_position,expected_position",
        (
                ("N", (3, 4), (3, 5)),
                ("E", (3, 4), (4, 4)),
                ("S", (3, 4), (3, 3)),
                ("W", (3, 4), (2, 4)),
        )
    )
    def test_move_forward(self, current_direction, current_position, expected_position):
        robot = Robot(*current_position, self.asteroid, current_direction)
        robot.move_forward()
        assert (robot.x, robot.y) == expected_position

    @pytest.mark.parametrize(
        "current_direction,current_position,expected_position",
        (
                ("N", (3, 4), (3, 3)),
                ("E", (3, 4), (2, 4)),
                ("S", (3, 4), (3, 5)),
                ("W", (3, 4), (4, 4)),
        )
    )
    def test_move_backward(self, current_direction, current_position, expected_position):
        robot = Robot(*current_position, self.asteroid, current_direction)
        robot.move_backward()
        assert (robot.x, robot.y) == expected_position

    @pytest.mark.parametrize(
        "current_direction,robot_coordinates,asteroid_size",
        (
                ("N", (8, 16), (11, 16)),
                ("E", (11, 15), (11, 16)),
                ("S", (3, 0), (11, 16)),
                ("W", (0, 4), (11, 16)),
        )
    )
    def test_check_robot_fall_move_forward(self, asteroid_size, robot_coordinates, current_direction):
        with pytest.raises(RobotFallFromAsteroidError):
            asteroid = Asteroid(*asteroid_size)
            robot = Robot(*robot_coordinates, asteroid, *current_direction)
            robot.move_forward()

    @pytest.mark.parametrize(
        "current_direction,robot_coordinates,asteroid_size",
        (
                ("N", (4, 0), (11, 16)),
                ("E", (0, 15), (11, 16)),
                ("S", (3, 16), (11, 16)),
                ("W", (11, 4), (11, 16)),
        )
    )
    def test_check_robot_fall_move_backward(self, asteroid_size, robot_coordinates, current_direction):
        with pytest.raises(RobotFallFromAsteroidError):
            asteroid = Asteroid(*asteroid_size)
            robot = Robot(*robot_coordinates, asteroid, *current_direction)
            robot.move_backward()
