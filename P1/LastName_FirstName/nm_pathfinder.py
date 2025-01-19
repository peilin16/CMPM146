import heapq

def find_path (source_point, destination_point, mesh):

    """
    Searches for a path from source_point to destination_point through the mesh

    Args:
        source_point: starting point of the pathfinder
        destination_point: the ultimate goal the pathfinder must reach
        mesh: pathway constraints the path adheres to

    Returns:

        A path (list of points) from source_point to destination_point if exists
        A list of boxes explored by the algorithm
    """

    start  = None
    destination = None
    for i in mesh["boxes"]: 
        if (within_bounds(i, source_point)):
            start = i
        if (within_bounds(i, destination_point)):
            destination = i
        if(start != None and destination != None):
            path, boxes = A_algorithm(start, destination, mesh)
            if(len(path)>=2):
                path[0] = source_point
                path[len(path) - 1] = destination_point
            elif (len(path) > 0 and path[0] == -1):
                # if path could not be found, remove placeholder denominator
                path.pop()
                # then feed to nm_interactive
            elif source_point != destination_point:
                path.append(source_point)
                path.append(destination_point)
            return path, boxes
        
    return [],[] ## not in range

def within_bounds (box, point):
    # check if point in range of box 
    # x1, x2, y1, y2
    # 0,  1.  2,  3
    # bias inclusive to bottom right so points exactly on edge of boxes won't be missed
    if (((box[0] < point[0]) and (box[2] < point[1])) 
    and (box[1] >= point[0] and box[3] >= point[1])):
        return True
    return False

def get_priority(current, destination):
    x1 = (current[0] + current[1])
    x2 = (destination[0] + destination[1])
    y1 = (current[2] + current[3])
    y2 = (destination[2] + destination[3])
    return ((x1- x2)**2 + (y1 - y2)**2) ** 0.5
    ## calculate by heuristic function then get the distance

def A_algorithm (start, destination, mesh):
    path = []
    pqueue = []
    heapq.heappush(pqueue, (0, start, "destination"))
    heapq.heappush(pqueue, (0, destination, "start"))
    visited = [] #save visited box
    forward_visited = []
    backward_visited = []
    if start == destination:
        return path, visited
    #initalize tables
    forward_came_from = {start: None}        
    forward_cost = {start: 0}
    backward_came_from = {destination: None}
    backward_cost = {destination: 0}

    while  pqueue: ## search box
        e, current, goal = heapq.heappop(pqueue)
        # find out which search added the node to queue
        terminate_check = backward_came_from
        if (goal == "start"):
            terminate_check = forward_came_from
        # check if node in other search's list
        if (current in terminate_check):
            midpoint = current
            # if current is in both lists, rebuild path
            # this loop builds the path from midpoint to start
            while current is not None:
                path.append(((current[0] + current[1]) / 2, (current[2] + current[3]) / 2))
                current = forward_came_from[current]
            # since the path is reversed, i.e. Midpoint, B, A, start, we have to reverse the list
            path.reverse() 
            # reset current to the midpoint
            current = midpoint
            # this loops build path from midpoint to goal
            while current is not None:
                    path.append(((current[0] + current[1]) / 2, (current[2] + current[3]) / 2))
                    current = backward_came_from[current]
            # this one is not reversed so we don't have to modify the list
            pqueue.clear()
            return path, visited

        visited.append(current)
        for i in mesh['adj'][current]:
            if (goal == "destination"):
                temporary_cost = forward_cost[current] + get_priority(current,i)
                if i not in forward_came_from or temporary_cost < forward_cost[i]:
                    forward_cost[i] = temporary_cost
                    forward_came_from[i] = current
                    priority = temporary_cost + get_priority(i, destination)
                    heapq.heappush(pqueue, (priority, i, goal))
            if (goal == "start"):
                temporary_cost = backward_cost[current] + get_priority(current,i)
                if i not in backward_came_from or temporary_cost < backward_cost[i]:
                    backward_cost[i] = temporary_cost
                    backward_came_from[i] = current
                    priority = temporary_cost + get_priority(i, start)
                    heapq.heappush(pqueue, (priority, i, goal))
    print("No path!")
    return [-1], visited
            
    

