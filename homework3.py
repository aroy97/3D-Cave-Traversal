import heapq
import math
import time

possible_movement_options = [[0, 0, 0], [1, 0, 0], [-1, 0, 0], [0, 1, 0], [0, -1, 0], [0, 0, 1],
                             [0, 0, -1], [1, 1, 0], [1, -1, 0], [-1, 1, 0], [-1, -1, 0],
                             [1, 0, 1], [1, 0, -1], [-1, 0, 1], [-1, 0, -1], [0, 1, 1],
                             [0, 1, -1], [0, -1, 1], [0, -1, -1]]

cost_per_movement = [0, 10, 10, 10, 10, 10, 10, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14]

information_in_file = list()
file_to_read_as_input = 'input.txt'
file_to_write_as_output = 'output.txt'


def breadth_first_search(entry_location, destination_location):
    list_to_traverse = list()
    list_to_traverse.append((entry_location, None))
    visited_locations = {}
    while list_to_traverse:
        current_location, previous_location = list_to_traverse.pop(0)
        if current_location in visited_locations:
            continue
        if current_location == destination_location:
            visited_locations[current_location] = previous_location
            return visited_locations
        visited_locations[current_location] = previous_location
        for possible_movement in movement_list_for_cave_locations[current_location]:
            possible_next_location = go_to_location(current_location, possible_movement_options[possible_movement])
            if (possible_next_location not in visited_locations) \
                    and (possible_next_location[0] < maximum_maze_dimensions[0]) \
                    and (possible_next_location[1] < maximum_maze_dimensions[1]) \
                    and (possible_next_location[2] < maximum_maze_dimensions[2]):
                list_to_traverse.append((possible_next_location, current_location))
    return 'FAIL'


def uniform_cost_search(entry_location, destination_location):
    list_to_traverse = list()
    heapq.heappush(list_to_traverse, (0, entry_location, None, None))
    visited_locations = {}
    while list_to_traverse:
        cost_till_current_location, current_location, previous_location, movement_from_previous_location = heapq.heappop(
            list_to_traverse)
        if (current_location in visited_locations) and (
                visited_locations[current_location][0] < cost_till_current_location):
            continue
        if current_location == destination_location:
            visited_locations[current_location] = (
                cost_till_current_location, previous_location, movement_from_previous_location)
            return visited_locations
        visited_locations[current_location] = (
            cost_till_current_location, previous_location, movement_from_previous_location)
        for possible_movement in movement_list_for_cave_locations[current_location]:
            possible_next_location = go_to_location(current_location, possible_movement_options[possible_movement])
            possible_next_location_cost = cost_till_current_location + cost_per_movement[possible_movement]
            if ((possible_next_location not in visited_locations) or (
                    visited_locations[possible_next_location][0] > possible_next_location_cost)) \
                    and (possible_next_location[0] < maximum_maze_dimensions[0]) \
                    and (possible_next_location[1] < maximum_maze_dimensions[1]) \
                    and (possible_next_location[2] < maximum_maze_dimensions[2]):
                possible_next_location_structure = (
                    possible_next_location_cost, possible_next_location, current_location, possible_movement)
                heapq.heappush(list_to_traverse, possible_next_location_structure)
    return 'FAIL'


def a_star_search(entry_location, destination_location):
    list_to_traverse = list()
    heapq.heappush(list_to_traverse, (0, entry_location, None, None, 0))
    visited_locations = {}
    while list_to_traverse:
        cost_till_current_location, current_location, previous_location, movement_from_previous_location, previous_location_heuristic = heapq.heappop(
            list_to_traverse)
        cost_till_current_location = cost_till_current_location - previous_location_heuristic
        if (current_location in visited_locations) and (
                visited_locations[current_location][0] < cost_till_current_location):
            continue
        if current_location == destination_location:
            visited_locations[current_location] = (
                cost_till_current_location, previous_location, movement_from_previous_location)
            return visited_locations
        visited_locations[current_location] = (
            cost_till_current_location, previous_location, movement_from_previous_location)
        for possible_movement in movement_list_for_cave_locations[current_location]:
            possible_next_location = go_to_location(current_location, possible_movement_options[possible_movement])
            possible_next_location_cost = cost_till_current_location + cost_per_movement[
                possible_movement] + future_distance_prediction(possible_next_location, destination_location)
            if ((possible_next_location not in visited_locations) or (
                    visited_locations[possible_next_location][0] > possible_next_location_cost)) \
                    and (possible_next_location[0] < maximum_maze_dimensions[0]) \
                    and (possible_next_location[1] < maximum_maze_dimensions[1]) \
                    and (possible_next_location[2] < maximum_maze_dimensions[2]):
                possible_next_location_structure = (
                    possible_next_location_cost, possible_next_location, current_location, possible_movement,
                    future_distance_prediction(possible_next_location, destination_location))
                heapq.heappush(list_to_traverse, possible_next_location_structure)
    return 'FAIL'


def go_to_location(current_location, possible_movement):
    return current_location[0] + possible_movement[0], current_location[1] + possible_movement[1], current_location[2] + \
           possible_movement[2]


def generate_coordinates(x_coordinate, y_coordinate, z_coordinate):
    return tuple([int(x_coordinate), int(y_coordinate), int(z_coordinate)])


def future_distance_prediction(first_point_of_interest, second_point_of_interest):
    return math.sqrt(((first_point_of_interest[0] - second_point_of_interest[0]) ** 2) +
                     ((first_point_of_interest[1] - second_point_of_interest[1]) ** 2) +
                     ((first_point_of_interest[2] - second_point_of_interest[2]) ** 2))


def organize_output_pattern(visited_locations, destination_location, method_of_traversal):
    destination_reached = False
    cost_of_traversal = 0
    count_for_all_movements = 0
    travelled_locations = list()
    cost_of_individual_movement = list()
    if method_of_traversal == 'BFS':
        while destination_reached is False:
            if visited_locations[destination_location] is not None:
                cost_of_individual_movement.insert(0, 1)
                count_for_all_movements = count_for_all_movements + 1
                cost_of_traversal = cost_of_traversal + 1
                travelled_locations.insert(0, destination_location)
                destination_location = visited_locations[destination_location]
            else:
                destination_reached = True
                cost_of_individual_movement.insert(0, 0)
                count_for_all_movements = count_for_all_movements + 1
                travelled_locations.insert(0, destination_location)
        output_file_to_create_bfs = open(file_to_write_as_output, 'w')
        output_file_to_create_bfs.write(str(cost_of_traversal) + '\n')
        output_file_to_create_bfs.write(str(count_for_all_movements) + '\n')
        for location_index in range(0, len(travelled_locations)):
            if location_index == (len(travelled_locations) - 1):
                location_data = ([str(coordinates) for coordinates in travelled_locations[location_index]])
                location_data.append(str(cost_of_individual_movement[location_index]))
                location_data_to_print = ' '.join(location_data)
                output_file_to_create_bfs.write(location_data_to_print)
            else:
                location_data = ([str(coordinates) for coordinates in travelled_locations[location_index]])
                location_data.append(str(cost_of_individual_movement[location_index]))
                location_data_to_print = ' '.join(location_data)
                output_file_to_create_bfs.write(location_data_to_print + '\n')
        output_file_to_create_bfs.close()
    else:
        while destination_reached is False:
            if locations_covered[destination_location][1] is None:
                count_for_all_movements = count_for_all_movements + 1
                travelled_locations.insert(0, destination_location)
                cost_of_individual_movement.insert(0, 0)
                destination_reached = True
            else:
                cost_of_traversal = cost_of_traversal + cost_per_movement[visited_locations[destination_location][2]]
                count_for_all_movements = count_for_all_movements + 1
                travelled_locations.insert(0, destination_location)
                cost_of_individual_movement.insert(0, cost_per_movement[visited_locations[destination_location][2]])
                destination_location = visited_locations[destination_location][1]
        output_file_to_create_ucs_or_astar = open(file_to_write_as_output, 'w')
        output_file_to_create_ucs_or_astar.write(str(cost_of_traversal) + '\n')
        output_file_to_create_ucs_or_astar.write(str(count_for_all_movements) + '\n')
        for location_index in range(0, len(travelled_locations)):
            if location_index == (len(travelled_locations) - 1):
                location_data = ([str(coordinates) for coordinates in travelled_locations[location_index]])
                location_data.append(str(cost_of_individual_movement[location_index]))
                location_data_to_print = " ".join(location_data)
                output_file_to_create_ucs_or_astar.write(location_data_to_print)
            else:
                location_data = ([str(coordinates) for coordinates in travelled_locations[location_index]])
                location_data.append(str(cost_of_individual_movement[location_index]))
                location_data_to_print = " ".join(location_data)
                output_file_to_create_ucs_or_astar.write(location_data_to_print + '\n')
        output_file_to_create_ucs_or_astar.close()


movement_list_for_cave_locations = dict()
code_execution_start_time = time.time()
with open(file_to_read_as_input, 'r') as input_file:
    for information_per_line in input_file.readlines():
        cleaned_information = information_per_line.strip()
        information_in_file.append(cleaned_information)
algorithm_to_be_executed = information_in_file[0]
maximum_maze_dimensions = generate_coordinates(information_in_file[1].split()[0], information_in_file[1].split()[1],
                                               information_in_file[1].split()[2])
entry_location_in_cave = generate_coordinates(information_in_file[2].split()[0], information_in_file[2].split()[1],
                                              information_in_file[2].split()[2])
destination_location_in_cave = generate_coordinates(information_in_file[3].split()[0],
                                                    information_in_file[3].split()[1],
                                                    information_in_file[3].split()[2])
for location_index_in_cave in range(5, len(information_in_file)):
    location_information = information_in_file[location_index_in_cave].split()
    cave_location = generate_coordinates(location_information[0], location_information[1], location_information[2])
    possible_location_movements = list()
    for movement_counter in range(3, len(location_information)):
        movement = int(location_information[movement_counter])
        possible_location_movements.append(movement)
    movement_list_for_cave_locations[cave_location] = possible_location_movements
if algorithm_to_be_executed == 'A*':
    locations_covered = a_star_search(entry_location_in_cave, destination_location_in_cave)
elif algorithm_to_be_executed == 'BFS':
    locations_covered = breadth_first_search(entry_location_in_cave, destination_location_in_cave)
elif algorithm_to_be_executed == 'UCS':
    locations_covered = uniform_cost_search(entry_location_in_cave, destination_location_in_cave)
code_execution_end_time = time.time()
if locations_covered == 'FAIL':
    output_file_to_create = open(file_to_write_as_output, 'w')
    output_file_to_create.write('FAIL')
    output_file_to_create.close()
else:
    organize_output_pattern(locations_covered, destination_location_in_cave, algorithm_to_be_executed)