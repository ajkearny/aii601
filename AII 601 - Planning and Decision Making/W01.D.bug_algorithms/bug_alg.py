import matplotlib.pyplot as plt
import numpy as np
from bresenham import bresenham_points

OBSTACLE = 1
FREE = 0

rotate_cw_mat = np.array([[0, 1], [-1, 0]])
rotate_ccw_mat = np.array([[0, -1], [1, 0]])

def make_simple_grid():
    grid = np.zeros((30, 30))
    grid[10:15, 10:15] = OBSTACLE
    grid[14:20, 12:14] = OBSTACLE

    return grid

def make_hook_grid():
    grid = np.zeros((30, 30))
    grid[5:7, 14:26] = OBSTACLE  # Topmost bar
    grid[10:12, 10:20] = OBSTACLE  # Upper bar
    grid[10:24, 10:12] = OBSTACLE  # Bottom bar
    grid[20:24, 10:23] = OBSTACLE  # Left bar
    grid[7:24, 23:26] = OBSTACLE  # Right bar
    grid = grid[:, ::-1]

    return grid

class BugRobot(object):
    def __init__(self, position, orientation):
        self.position = position
        self.orientation = orientation

    def _move_forward(self):
        self.position += self.orientation

    def _turn_out(self):
        self.orientation = rotate_ccw_mat @ self.orientation

    def _turn_in(self):
        self.orientation = rotate_cw_mat @ self.orientation

    def is_on_line(self, line):
        manhattan_dist = (np.abs(line[0] - self.position[0]) +
                          np.abs(line[1] - self.position[1]))
        return np.min(manhattan_dist) < 0.5

    def follow_line(self, grid, line):
        manhattan_dist = (np.abs(line[0] - self.position[0]) +
                          np.abs(line[1] - self.position[1]))
        ind = np.argwhere(manhattan_dist < 0.5)[0]

        # If reached the end, stop
        if ind == line.shape[1] - 1:
            return False

        # Move if possible
        next_pos = line[:, ind+1].T[0]
        orientation = next_pos.T - self.position
        self.orientation = np.array(
            [round(orientation[0]), round(orientation[1])])
        if grid[next_pos[0], next_pos[1]] == OBSTACLE:
            return True
        else:
            self._move_forward()
            return False

    def follow_object(self, grid):
        p = self.position
        of = self.orientation
        ocw = rotate_cw_mat @ of
        occw = rotate_ccw_mat @ of

        is_wall_ahead = grid[p[0]+of[0], p[1]+of[1]] == OBSTACLE
        is_wall_side = grid[p[0]+ocw[0], p[1]+ocw[1]] == OBSTACLE

        if is_wall_ahead:
            # Turn out
            self._turn_out()
            self.follow_object(grid)
        elif is_wall_side:
            # Follow
            self._move_forward()
        else:
            # Turn in and move
            self._turn_in()
            self._move_forward()

def plot_scene(grid, robot, line=None):
    plt.clf()
    plt.imshow(1 - grid, cmap='gray', vmin=0, vmax=1)
    if line is not None:
        plt.plot(line[1], line[0], '.')

    plt.plot(robot.position[1], robot.position[0], 'x')
    plt.show()
    plt.pause(0.01)


def bug_0(grid, start, goal):
    line = bresenham_points(start, goal)
    robot = BugRobot(position=start,
                     orientation=np.array([1, 0]))

    plt.ion()
    plot_scene(grid, robot, line)
    plt.pause(2)
    follow_line = True
    for _ in range(1000):
        print(f"Position: {robot.position} | "
              f"Orientation: {robot.orientation} | "
              f"Is On Line: {robot.is_on_line(line)}")
        plot_scene(grid, robot, line)

        if follow_line:
            # Follow the line until we cannot
            did_encounter_obstacle = robot.follow_line(grid, line)
            if did_encounter_obstacle:
                follow_line = False
        else:
            # Follow the object until we encounter
            robot.follow_object(grid)
            if robot.is_on_line(line):
                follow_line = True

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--scenario', default='line-draw', required=False,
                        help='[line-draw, no-obstacle, simple-obstacle, hook]')
    parser.add_argument('--planner', default=None, required=False,
                        help='[{None}: plotting only, bug0]')
    args = parser.parse_args()

    # Simple Grid Example
    if args.scenario == 'line-draw':
        grid = None
        start = np.array([3, 20])
        goal = np.array([25, 5])
        line = bresenham_points(start, goal)
        plt.plot(line[0, :], line[1, :], '.')
        plt.gca().set_aspect('equal')
        plt.show()
    elif args.scenario == 'no-obstacle':
        grid = np.zeros((30, 30))
        start = np.array([3, 12])
        goal = np.array([25, 8])
    elif args.scenario == 'simple-obstacle':
        grid = make_simple_grid()
        start = np.array([3, 12])
        goal = np.array([25, 8])
    elif args.scenario == 'hook':
        grid = make_hook_grid()
        start = np.array([3, 14])
        goal = np.array([15, 14])

    # Algorithm
    if args.planner is None and grid is not None:
        line = bresenham_points(start, goal)
        robot = BugRobot(position=start,
                         orientation=np.array([1, 0]))
        plot_scene(grid, robot, line)
        plt.show()
    if args.planner == 'bug0':
        bug_0(grid, start, goal)
    if args.planner == 'bug1':
        bug_1(grid, start, goal)
