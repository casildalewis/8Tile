import copy
import heapq

def succ(state):
    """
    Given a state of the puzzle, represented as a single list of integers with a 0 in the 
    empty space, find all of the possible successor states.

    The number of successor states depends on the current state.  There could be 2 (empty 
    grid is at corner),  3 (empty grid is at middle of a boundary), or 4 (empty grid is 
    at the center of a boundary) successors.

    Args:
        state (list): current state of the game

    returns: successors (list of lists)
    """

    successors = []

    zero_index = state.index(0)
    zero_x = int(zero_index/3)
    zero_y = zero_index%3

    movable_indices  = [(zero_x-1, zero_y), (zero_x+1, zero_y), (zero_x, zero_y-1), (zero_x, zero_y+1)]

    for (x, y) in movable_indices:
        if x in range(3) and y in range(3):

            successor = copy.deepcopy(state)
            successor[(x*3) + y] = 0
            successor[zero_index] = state[(x*3) + y]
            successors.append(successor)

    successors = sorted(successors)
    return successors

def print_succ(state):
    """
    This function should print out the successor states of the initial state, as well as 
    their heuristic value.

    Args:
        state (list): current state of the game
    """

    successors = succ(state)

    for successor in successors:

        heuristic_val = heuristic(successor)
        print(str(successor) + " h=" + str(heuristic_val))

def solve(state):
    """
    Given a state of the puzzle, perform the A* search algorithm and print the path from 
    the current state to the goal state, along with the heuristic values of each 
    intermediate state, and total moves taken to reach the state.

    Args:
        state (list): current state of the game
    """

    goal = [1, 2, 3, 4, 5, 6, 7, 8, 0]
    open = []
    closed = []

    state_h = heuristic(state)
    heapq.heappush(open, (0+state_h, state, (0, state_h, -1)))

    while open:
        n = heapq.heappop(open)
        closed.append(n)

        (n_gh, n_state, (n_g, n_h, n_pindex)) = n

        if n_state == goal:
            break

        n_successors = succ(n_state)
        for n_succ in n_successors:

            g = n_g + 1
            h = heuristic(n_succ)
            pindex = closed.index(n)

            if not any (n_succ in x for x in closed+open):
                heapq.heappush(open, (g+h, n_succ, (g, h, pindex)))
            else:
                for x in closed+open:
                    (x_gh, x_state, (x_g, x_h, x_pindex)) = x
                    if n_succ == x_state:
                        if g < x_g:
                            open.remove(x)
                            heapq.heappush(open, (g+h, n_succ, (g, h, pindex)))

    solution = [closed[-1]]
    index = closed[-1][2][2]
    
    while index != -1:
        solution.insert(0, closed[index])
        index = closed[index][2][2]

    for x in solution:
        (gh, state, (g, h, pindex)) = x
        print(str(state) + " h=" + str(h) + " moves: " + str(g))


def heuristic (state):
    """
    We will use the sum of Manhattan distance of each tile to its goal position as 
    our heuristic function. 

    The Manhattan distance in this case is the sum of the absolute difference of 
    their x co-ordinates and y co-ordinates.

    Args:
        state (list): current state of the game

    returns: heuristic value of current state (int)
    """

    heuristic_val = 0
    goal = [1, 2, 3, 4, 5, 6, 7, 8, 0]
    
    for num in state:
        if num == 0:
            continue

        goal_index = goal.index(num)
        x1 = int(goal_index/3)
        y1 = goal_index%3

        state_index = state.index(num)
        x2 = int(state_index/3)
        y2 = state_index%3

        heuristic_val += abs(y2 - y1) + abs(x2 - x1)

    return heuristic_val

# if __name__ == "__main__":
#     # print(heuristic([2, 5, 8, 4, 3, 6, 7, 1, 0]))
#     # print_succ([8,7,6,5,4,3,2,1,0])
#     # solve([1, 2, 3, 4, 0, 6, 7, 5, 8])
#     # solve([4,3,8,5,1,6,7,2,0])
#     # solve([1,2,3,4,5,6,7,0,8])