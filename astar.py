def astar(start, end):
    # initialize queue and explored
    priorityQueue = []
    visited = {}

    heapq.heappush(priorityQueue,
                   (0, start, None, None, 0))  # (cost, current node, parent node, action taken, parent heuristic)
    # while there are still values in the queue
    while priorityQueue:
        # get the first path from the queue
        cost, curr_node, parent_node, action_taken, parent_h = heapq.heappop(priorityQueue)
        cost = cost - parent_h

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
            # use the action to get the neighbor and its cost
            neighbor = perform_action(curr_node, action_list[action_index])
            neighbor_cost = cost + action_costs[action_index] + heuristic_(neighbor, end)

            if (neighbor not in visited) or (visited[neighbor][0] > neighbor_cost):
                neighbor_node = (neighbor_cost, neighbor, curr_node, action_index, heuristic_(neighbor, end))
                heapq.heappush(priorityQueue, neighbor_node)

    # if the queue is empty return fail
    return 'FAIL'