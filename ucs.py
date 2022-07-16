
def ucs(start, end):
    # initialize queue and explored
    explored = {}
    priorityQueue = []
    visited = {}

    # have dictionary at start where you do possible actions
    # node, parent, cost, depth

    heapq.heappush(priorityQueue, (0, start, None, None))  # (cost, current node, parent node, action taken)

    # while there are still values in the queue
    while priorityQueue:
        # get the first path from the queue
        cost, curr_node, parent_node, action_taken = heapq.heappop(priorityQueue)

        # if it has been seen before AND it had a lower cost, dont keep going
        if (curr_node in visited) and (visited[curr_node][0] < cost):
            continue

        # check if we got to the end
        if curr_node == end:
            visited[curr_node] = (cost, parent_node, action_taken)
            return visited

        # update visited dict
        visited[curr_node] = (cost, parent_node, action_taken)

        # loop through the actions indices
        for action_index in node_actions[curr_node]:
            # use the action to get the neighbor and its hash key
            neighbor = perform_action(curr_node, action_list[action_index])
            neighbor_cost = cost + action_costs[action_index]

            # check if neighbor has been visited OR if it has been visited at a higher cost
            if (neighbor not in visited) or (visited[neighbor][0] > neighbor_cost):
                neighbor_node = (neighbor_cost, neighbor, curr_node, action_index)
                heapq.heappush(priorityQueue, neighbor_node)

    # if the queue is empty return fail
    return 'FAIL'
