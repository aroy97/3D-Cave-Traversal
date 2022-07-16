def breadth_first_search(entry_point, destination_point):
    list_to_traverse = list()
    list_to_traverse.append((entry_point, None))
    visited_locations = {}
    while list_to_traverse:
        current_location, previous_location = list_to_traverse.pop(0)
        if current_location in visited_locations:
            continue
        if current_location == destination_point:
            visited_locations[current_location] = previous_location
            return visited_locations
        visited_locations[current_location] = previous_location
        for possible_movement in node_actions[current_location]:
            possible_next_location = perform_action(current_location, action_list[possible_movement])

            if possible_next_location not in visited_locations:
                list_to_traverse.append((possible_next_location, current_location))
    return 'FAIL'
