
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
        if (is_the_point_in_range(i, source_point)):
            start = i;
        if (is_the_point_in_range(i, destination_point)):
            destination = i;
        if(start != None and destination != None):
            path, boxes = A_algorithm(start, destination, mesh)
            return path, boxes
        
    return [],[] ## not in range

def is_the_point_in_range (box, source): 
    if (((box[0] <= source[0]) and (box[2] <= source[1])) and (box[1] >= source[0] and box[3] >= source[1])):
        return True
    return False

def get_priority(current, destination):
    x1 = (current[0] + current[1]);
    x2 = (destination[0] + destination[1])
    y1 = (current[2] + current[3])
    y2 = (destination[2] + destination[3])
    return ((x1- x2)**2 + (y1 - y2)**2) ** 0.5
    ## calculate by heuristic function then get the distance


def A_algorithm(start,destination, mesh):
    
    path = [];        
    pqueue = []
    heapq.heappush(pqueue, (0, start))
    visited = [start];   ##save visited box
    if start == destination:
        return path,visited;
    came_from = {}        
    came_from[start] = None 
    cost = {}  # Cost to reach each no
    cost[start] = 0;

    while  pqueue: ## search box
        e, current = heapq.heappop(pqueue)
        visited.append(current);

        if current == destination:
            while current is not None:
                path.append(((current[0] + current[1]) / 2, (current[2] + current[3]) / 2))
                current = came_from[current]
            path.reverse()
            pqueue.clear();
            break;
        
        for i in mesh['adj'][current]:

            temporarily_cost = cost[current] + get_priority(current,i);
            if i not in came_from or temporarily_cost < cost[i]:
                cost[i] = temporarily_cost
                came_from[i] = current
                priority = temporarily_cost + get_priority(i, destination)
                heapq.heappush(pqueue, (priority, i))

    return path, visited;

