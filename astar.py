import pygame
import math

pygame.init()

# Extra bias towards Heuristic Value
# Try 1, 1.2, 1.5, 2, and 10
bias = 2

def heuristic_Cost(start,goal):
    return math.sqrt(abs(goal[0] - start[0])**2 + abs(goal[1] - start[1])**2) * bias
def getNeighbors(current):
    temp = []
    if current[0] - 1 >= 0 and collisions[current[0]-1][current[1]] == 0:
        temp.append((current[0] - 1,current[1]))
    if current[0] + 1 <= 15 and collisions[current[0]+1][current[1]] == 0:
        temp.append((current[0] + 1,current[1]))
    if current[1] - 1 >= 0 and collisions[current[0]][current[1]-1] == 0:
        temp.append((current[0],current[1] - 1))
    if current[1] + 1 <= 15 and collisions[current[0]][current[1]+1] == 0:
        temp.append((current[0],current[1] + 1))
    return temp


# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0,0,255)
LIGHTBLUE = (0,0,128)
GOLD = (255,215,0)

# Pygame Things to make a screen
size =(1024,1024)
sq_size = 64
screen = pygame.display.set_mode(size)
pygame.display.set_caption("A*")


# Visuals Variables

square_x = 0
square_y = 0
square_size = 32
square_offset = 16


# Collision Matrix

collisions =   [[0,1,0,0,0,0,0,0,1,0,0,0,0,0,0,0],\
                [0,1,1,1,0,1,1,1,1,1,1,1,0,1,1,0],\
                [0,0,0,1,0,1,0,1,0,1,0,0,0,0,1,0],\
                [0,1,0,0,0,0,0,0,0,1,0,1,1,0,1,0],\
                [1,1,1,0,1,1,1,1,0,0,0,0,1,0,1,0],\
                [0,0,0,0,1,0,0,0,0,1,1,0,1,1,1,1],\
                [0,1,1,0,1,0,1,0,1,1,0,0,0,0,1,0],\
                [0,1,0,0,0,0,0,0,0,1,1,1,1,0,1,0],\
                [0,1,0,1,1,1,0,1,0,1,0,1,0,0,0,0],\
                [0,0,0,1,0,1,0,1,0,1,0,0,0,1,1,0],\
                [0,1,0,0,0,1,0,1,0,1,0,1,1,1,1,0],\
                [0,1,0,1,0,1,0,1,0,1,0,0,0,0,1,0],\
                [1,1,0,1,0,1,0,1,0,0,0,1,1,0,1,1],\
                [0,0,0,0,0,1,0,1,0,1,0,0,1,0,0,0],\
                [0,1,1,1,0,1,0,1,0,1,0,1,1,1,1,1],\
                [0,0,0,1,0,0,0,1,0,1,0,0,0,0,0,0]]


# Takes the transpose of the matrix above because xy is wierd
collisions = list(map(list,zip(*collisions)))


# A* Stuff
steps = 0

goal = (15,15)
start = (square_x,square_y)

# Set of nodes already evaluated
closedSet = set()

# Set of nodes to be evaluated
openSet = {start}

# For recovering the shortest Path
cameFrom = [[(math.inf,math.inf) for x in range(16)]for y in range(16)]
cameFrom[square_x][square_y] = start

# Initalize gScore
gScore = [[math.inf for x in range(16)]for y in range(16)]
gScore[square_x][square_y] = 0

# Initalize fScore
fScore = [[math.inf for x in range(16)]for y in range(16)]
fScore[square_x][square_y] = heuristic_Cost((square_x,square_y),goal)

found = False
finished_path = []



# Loop until the user clicks the close button.
done = False
 
# Used to manage how fast the screen updates
clock = pygame.time.Clock()
 
# -------- Main Program Loop -----------
while not done:
    # --- Main event loop
    for event in pygame.event.get(): # User did something
        if event.type == pygame.QUIT: # If user clicked close
            done = True # Flag that we are done so we exit this loop
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q or event.key == pygame.K_ESCAPE:
                done = True
            if event.key == pygame.K_UP:
                square_y = square_y - 1
            if event.key == pygame.K_DOWN:
                square_y = square_y + 1
            if event.key == pygame.K_LEFT:
                square_x = square_x - 1
            if event.key == pygame.K_RIGHT:
                square_x = square_x + 1
            if event.key == pygame.K_SPACE:
                steps = steps + 1
                print("STEPS: ",steps)

                # A* loop
                if openSet and  not found:

                    #find the minimum fScore in openSet
                    current = min(openSet, key=lambda x: fScore[x[0]][x[1]])
                    print("Current fScore Value: ", fScore[current[0]][current[1]])
                    print("Position: ", current)

                    # Check if Done
                    if current == goal:
                        print("DONE!!!")
                        found = True


                    openSet.discard(current)
                    closedSet.add(current)

                    # Look at all possible Neighbors
                    for neighbor in getNeighbors(current):

                        # Ignore if already looked at
                        if neighbor in closedSet:
                            continue

                        # If not looked at, add to openList
                        if neighbor not in openSet:
                            openSet.add(neighbor)

                        # If already looked at, check if score needs updating
                        tentative_gScore = gScore[current[0]][current[1]] + 1
                        if tentative_gScore >= gScore[neighbor[0]][neighbor[1]]:
                            continue

                        #Best path yet, update
                        gScore[neighbor[0]][neighbor[1]] = tentative_gScore
                        fScore[neighbor[0]][neighbor[1]] = gScore[neighbor[0]][neighbor[1]]\
                                                            + heuristic_Cost(neighbor,goal)

                        #Record Path
                        cameFrom[neighbor[0]][neighbor[1]] = current
                elif  found and start not in finished_path:
                    print("Position: ", current)
                    finished_path.append(current)
                    current = cameFrom[current[0]][current[1]]
                else:
                    print(len(finished_path))


    # First, clear the screen to white. Don't put other drawing commands
    # above this, or they will be erased with this command.
    screen.fill(WHITE)

    # Prints Grid
    for x in range(0,16):
        pygame.draw.line(screen, BLACK, [0,x*sq_size], [1024,x*sq_size],2)
        pygame.draw.line(screen, BLACK, [x*sq_size,0], [x*sq_size,1024],2)
    # Prints Red collision squares
    for count_x,x in enumerate(collisions):
        for count_y,y in enumerate(x):
            if y == 1:
                    pygame.draw.rect(screen, RED,  [count_x * sq_size + 2,\
                                                    count_y * sq_size + 2,\
                                                    sq_size-2, sq_size-2])

    # Print blue looked at squares
    for position in closedSet:
        pygame.draw.rect(screen, BLUE,  [position[0] * sq_size + 2,\
                                position[1] * sq_size + 2,\
                                sq_size-2, sq_size-2])

    # Print light blue openSet squares
    for position in openSet:
        pygame.draw.rect(screen, LIGHTBLUE,  [position[0] * sq_size + 2,\
                                position[1] * sq_size + 2,\
                                sq_size-2, sq_size-2])
    # Print gold finished Path
    for position in finished_path:
        pygame.draw.rect(screen, GOLD,  [position[0] * sq_size + 2,\
                                position[1] * sq_size + 2,\
                                sq_size-2, sq_size-2])
    
    # Character Square
    pygame.draw.rect(screen, GREEN, [square_x * sq_size + square_offset,\
                                    square_y * sq_size + square_offset,\
                                    square_size, square_size])

    # --- Go ahead and update the screen with what we've drawn.
    pygame.display.flip()
 
    # --- Limit to 60 frames per second
    clock.tick(60)
pygame.quit()

