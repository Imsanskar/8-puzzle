import sys
from collections import deque
import heapq
import resource

class Node():
    def __init__(self, state, parent=None, action="initial"):
        self.state = tuple(state)
        self.parent = parent
        self.action = action
        self.blankRow = self.getEmpty() // 3
        self.blanlColumn = self.getEmpty() % 3

    def isGoal(self):
        return all(i == self.state[i] for i in range(9))

    def getEmpty(self):
        for i in range(9):
            if self.state[i] == 0:
                return i

    def manhattan(self):
        goalState = list(i for i in range(9))
        currentState = list(self.state)
        return sum(abs(currentState[i]//3 - goalState[i]//3) + abs(currentState[i]%3 - goalState[i]%3) for i in range(9))


    def moveLeft(self):
        emptyCell = self.getEmpty()
        if(emptyCell%3 == 0):
            return None
        else:
            newBoard = list(self.state)
            newBoard[emptyCell], newBoard[emptyCell-1] = newBoard[emptyCell-1], 0
            return Node(newBoard, self, "left")


    def moveRight(self):
        emptyCell = self.getEmpty()
        if(emptyCell % 3 == 2):
            return None
        else:
            newBoard = list(self.state)
            newBoard[emptyCell], newBoard[emptyCell+1] = newBoard[emptyCell+1], 0
            return Node(newBoard, self, "right")



    def moveUp(self):
        emptyCell = self.getEmpty()
        if(emptyCell // 3 == 0):
            return None
        else:
            newBoard = list(self.state)
            newBoard[emptyCell], newBoard[emptyCell-3] = newBoard[emptyCell-3], 0
            return Node(newBoard, self, "up")


    def moveDown(self):
        emptyCell = self.getEmpty()
        if(emptyCell // 3 == 2):
            return None
        else:
            newBoard = list(self.state)
            newBoard[emptyCell], newBoard[emptyCell+3] = newBoard[emptyCell+3], 0
            return Node(newBoard, self, "down")

    def getChildren(self):
        children = []
        children.append(self.moveUp())
        children.append(self.moveRight())
        children.append(self.moveDown())
        children.append(self.moveLeft())
        return list(filter(None, children))


    def __str__(self):
        s = "Action:" + self.action + "\n"
        for i in range(9):
            if(i % 3 < 2):
                s += str(self.state[i]) + ' | '
            else:
                s += str(self.state[i]) + "\n"
        return s

    def __lt__(self, other):
        return self.manhattan() < other.manhattan()


def dfs(state):
    stack = []
    stack.append(Node(state))
    explored = set()
    while True:
        if(len(stack) == 0):
            sys.exit("no solution")
        node = stack.pop()
        explored.add(node.state)
        if node.isGoal():
            solution = []
            while node.parent is not None:
                solution.append(node)
                node = node.parent
            print(node)
            solution.reverse()
            return solution
            print(node)
        for neighbour in node.getChildren():
            if neighbour.state not in explored and neighbour not in stack:
                stack.append(neighbour)
                # explored.add(neighbour.state)



def bfs(state):
    queue = deque()
    queue.append(Node(state))
    explored = set()
    while True:
        if not queue:
            sys.exit("no solution")
        node = queue.popleft()
        explored.add(node.state)
        if node.isGoal():
            solution = []
            while node.parent is not None:
                solution.append(node)
                node = node.parent
            print(node)
            solution.reverse()
            return solution
        for neighbour in node.getChildren():
            if neighbour.state not in explored and neighbour not in queue:
                queue.append(neighbour)


def astar(state):
    stack = []
    heapq.heapify(stack)
    heapq.heappush(stack, Node(state))
    explored = set()
    while True:
        if not state:
            sys.exit("No solution")
        node = heapq.heappop(stack)
        explored.add(node.state)
        if node.isGoal():
            solution = []
            while node.parent is not None:
                solution.append(node)
                node = node.parent
            print(node)
            solution.reverse()
            return solution
        for neighbour in node.getChildren():
            if neighbour.state not in explored and neighbour not in stack:
                heapq.heappush(stack, neighbour)



def main():
    board = list(eval(sys.argv[2]))
    if(sys.argv[1] == "bfs"):
        solution = bfs(board)
    if(sys.argv[1] == "dfs"):
        solution = dfs(board)
    if(sys.argv[1] == "ast"):
        solution = astar(board)

    file = open('output.txt', 'w')
    output = ""
    for sol in solution:
        output += str(sol) + "\n"
    file.write("Path to goal:\n" + output + "\n\n")
    file.write("Path Cost:" + str(len(solution)) + "\n")
    file.write('max_ram_usage: ' + str(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024))

    file.close()



if __name__ == "__main__":
    main()
