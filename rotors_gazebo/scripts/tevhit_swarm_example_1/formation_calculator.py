import math
from decimal import Decimal

# Each target positions calculated around of the reference point,
# the reference point is center of all UAVs.


def square_formation_target_positions(reference_point, total_uav_count, distance_between_uav):
    if total_uav_count <= 4:
        position1 = [0, 0]
        position2 = [0, 0]
        position3 = [0, 0]
        position4 = [0, 0]

        distance_between_uav /= 2

        position1[0] = reference_point[0] + distance_between_uav
        position1[1] = reference_point[1] + distance_between_uav

        position2[0] = reference_point[0] + distance_between_uav
        position2[1] = reference_point[1] - distance_between_uav

        position3[0] = reference_point[0] - distance_between_uav
        position3[1] = reference_point[1] + distance_between_uav

        position4[0] = reference_point[0] - distance_between_uav
        position4[1] = reference_point[1] - distance_between_uav

        return [position1, position2, position3, position4]
    else:
        total_uav_count_without_corners = total_uav_count - 4

        if total_uav_count_without_corners % 4 > 0:
            addition = 1
        else:
            addition = 0

        distance_between_corners = ((int(total_uav_count_without_corners / 4) + addition) + 1) * distance_between_uav

        position1 = [0, 0]
        position2 = [0, 0]
        position3 = [0, 0]
        position4 = [0, 0]

        distance_between_corners /= 2

        position1[0] = reference_point[0] + distance_between_corners
        position1[1] = reference_point[1] + distance_between_corners

        position2[0] = reference_point[0] + distance_between_corners
        position2[1] = reference_point[1] - distance_between_corners

        position3[0] = reference_point[0] - distance_between_corners
        position3[1] = reference_point[1] + distance_between_corners

        position4[0] = reference_point[0] - distance_between_corners
        position4[1] = reference_point[1] - distance_between_corners

        positions = [position1, position2, position3, position4]

        total_uav_count_over_edge_1 = 0
        total_uav_count_over_edge_2 = 0
        total_uav_count_over_edge_3 = 0
        total_uav_count_over_edge_4 = 0

        i = total_uav_count_without_corners
        while i > 0:
            total_uav_count_over_edge_1 += 1
            i -= 1
            if i == 0:
                break

            total_uav_count_over_edge_2 += 1
            i -= 1
            if i == 0:
                break

            total_uav_count_over_edge_3 += 1
            i -= 1
            if i == 0:
                break

            total_uav_count_over_edge_4 += 1
            i -= 1
            if i == 0:
                break

        for i in range(total_uav_count_over_edge_1):
            temp_position = [0, 0]
            temp_position[0] = position1[0]
            temp_position[1] = position1[1] - distance_between_uav * (i + 1)
            positions.append(temp_position)

        for i in range(total_uav_count_over_edge_2):
            temp_position = [0, 0]
            temp_position[0] = position2[0] - distance_between_uav * (i + 1)
            temp_position[1] = position2[1]
            positions.append(temp_position)

        for i in range(total_uav_count_over_edge_3):
            temp_position = [0, 0]
            temp_position[0] = position3[0] + distance_between_uav * (i + 1)
            temp_position[1] = position3[1]
            positions.append(temp_position)

        for i in range(total_uav_count_over_edge_4):
            temp_position = [0, 0]
            temp_position[0] = position4[0]
            temp_position[1] = position4[1] + distance_between_uav * (i + 1)
            positions.append(temp_position)

        return positions


def triangle_formation_target_positions(reference_point, total_uav_count, distance_between_uav):
    if total_uav_count <= 3:
        position2 = [0, 0]
        position3 = [0, 0]

        position1 = [reference_point[0], reference_point[1] + (distance_between_uav / 2)]

        position2[0] = position1[0] + math.sin(math.radians(30)) * distance_between_uav
        position2[1] = position1[1] - math.cos(math.radians(30)) * distance_between_uav

        position3[0] = position1[0] + math.sin(math.radians(-30)) * distance_between_uav
        position3[1] = position1[1] - math.cos(math.radians(-30)) * distance_between_uav

        return [position1, position2, position3]
    else:
        total_uav_count_without_corners = total_uav_count - 3

        if total_uav_count_without_corners % 3 > 0:
            addition = 1
        else:
            addition = 0

        distance_between_corners = ((int(total_uav_count_without_corners / 3) + addition) + 1) * distance_between_uav

        position2 = [0, 0]
        position3 = [0, 0]

        position1 = [reference_point[0], reference_point[1] + (distance_between_corners / 2)]

        position2[0] = position1[0] + math.sin(math.radians(30)) * distance_between_corners
        position2[1] = position1[1] - math.cos(math.radians(30)) * distance_between_corners

        position3[0] = position1[0] + math.sin(math.radians(-30)) * distance_between_corners
        position3[1] = position1[1] - math.cos(math.radians(-30)) * distance_between_corners

        positions = [position1, position2, position3]

        total_uav_count_over_edge_1 = 0
        total_uav_count_over_edge_2 = 0
        total_uav_count_over_edge_3 = 0

        i = total_uav_count_without_corners
        while i > 0:
            total_uav_count_over_edge_1 += 1
            i -= 1
            if i == 0:
                break

            total_uav_count_over_edge_2 += 1
            i -= 1
            if i == 0:
                break

            total_uav_count_over_edge_3 += 1
            i -= 1
            if i == 0:
                break

        for i in range(total_uav_count_over_edge_1):
            temp_position = [0, 0]
            temp_position[0] = position1[0] + math.sin(math.radians(30)) * distance_between_uav * (i + 1)
            temp_position[1] = position1[1] - math.cos(math.radians(30)) * distance_between_uav * (i + 1)
            positions.append(temp_position)

        for i in range(total_uav_count_over_edge_2):
            temp_position = [0, 0]
            temp_position[0] = position1[0] + math.sin(math.radians(-30)) * distance_between_uav * (i + 1)
            temp_position[1] = position1[1] - math.cos(math.radians(-30)) * distance_between_uav * (i + 1)
            positions.append(temp_position)

        for i in range(total_uav_count_over_edge_3):
            temp_position = [0, 0]
            temp_position[0] = position3[0] + distance_between_uav * (i + 1)
            temp_position[1] = position3[1]
            positions.append(temp_position)

        return positions


def pentagon_formation_target_positions(reference_point, total_uav_count, distance_between_uav):
    if total_uav_count <= 5:
        position2 = [0, 0]
        position3 = [0, 0]
        position4 = [0, 0]
        position5 = [0, 0]

        position1 = [reference_point[0], reference_point[1] + distance_between_uav]

        position2[0] = position1[0] + math.sin(math.radians(54)) * distance_between_uav
        position2[1] = position1[1] - math.cos(math.radians(54)) * distance_between_uav

        position3[0] = position1[0] + math.sin(math.radians(-54)) * distance_between_uav
        position3[1] = position1[1] - math.cos(math.radians(-54)) * distance_between_uav

        position4[0] = position2[0] + math.sin(math.radians(-18)) * distance_between_uav
        position4[1] = position2[1] - math.cos(math.radians(-18)) * distance_between_uav

        position5[0] = position3[0] + math.sin(math.radians(18)) * distance_between_uav
        position5[1] = position3[1] - math.cos(math.radians(18)) * distance_between_uav

        return [position1, position2, position3, position4, position5]
    else:
        total_uav_count_without_corners = total_uav_count - 5

        if total_uav_count_without_corners % 5 > 0:
            addition = 1
        else:
            addition = 0

        distance_between_corners = ((int(total_uav_count_without_corners / 5) + addition) + 1) * distance_between_uav

        position2 = [0, 0]
        position3 = [0, 0]
        position4 = [0, 0]
        position5 = [0, 0]

        position1 = [reference_point[0], reference_point[1] + distance_between_corners]

        position2[0] = position1[0] + math.sin(math.radians(54)) * distance_between_corners
        position2[1] = position1[1] - math.cos(math.radians(54)) * distance_between_corners

        position3[0] = position1[0] + math.sin(math.radians(-54)) * distance_between_corners
        position3[1] = position1[1] - math.cos(math.radians(-54)) * distance_between_corners

        position4[0] = position2[0] + math.sin(math.radians(-18)) * distance_between_corners
        position4[1] = position2[1] - math.cos(math.radians(-18)) * distance_between_corners

        position5[0] = position3[0] + math.sin(math.radians(18)) * distance_between_corners
        position5[1] = position3[1] - math.cos(math.radians(18)) * distance_between_corners

        positions = [position1, position2, position3, position4, position5]

        total_uav_count_over_edge_1 = 0
        total_uav_count_over_edge_2 = 0
        total_uav_count_over_edge_3 = 0
        total_uav_count_over_edge_4 = 0
        total_uav_count_over_edge_5 = 0

        i = total_uav_count_without_corners
        while i > 0:
            total_uav_count_over_edge_1 += 1
            i -= 1
            if i == 0:
                break

            total_uav_count_over_edge_2 += 1
            i -= 1
            if i == 0:
                break

            total_uav_count_over_edge_3 += 1
            i -= 1
            if i == 0:
                break

            total_uav_count_over_edge_4 += 1
            i -= 1
            if i == 0:
                break

            total_uav_count_over_edge_5 += 1
            i -= 1
            if i == 0:
                break

        for i in range(total_uav_count_over_edge_1):
            temp_position = [0, 0]
            temp_position[0] = position1[0] + math.sin(math.radians(54)) * distance_between_uav * (i + 1)
            temp_position[1] = position1[1] - math.cos(math.radians(54)) * distance_between_uav * (i + 1)
            positions.append(temp_position)

        for i in range(total_uav_count_over_edge_2):
            temp_position = [0, 0]
            temp_position[0] = position1[0] + math.sin(math.radians(-54)) * distance_between_uav * (i + 1)
            temp_position[1] = position1[1] - math.cos(math.radians(-54)) * distance_between_uav * (i + 1)
            positions.append(temp_position)

        for i in range(total_uav_count_over_edge_3):
            temp_position = [0, 0]
            temp_position[0] = position2[0] + math.sin(math.radians(-18)) * distance_between_uav * (i + 1)
            temp_position[1] = position2[1] - math.cos(math.radians(-18)) * distance_between_uav * (i + 1)
            positions.append(temp_position)

        for i in range(total_uav_count_over_edge_4):
            temp_position = [0, 0]
            temp_position[0] = position3[0] + math.sin(math.radians(18)) * distance_between_uav * (i + 1)
            temp_position[1] = position3[1] - math.cos(math.radians(18)) * distance_between_uav * (i + 1)
            positions.append(temp_position)

        for i in range(total_uav_count_over_edge_5):
            temp_position = [0, 0]
            temp_position[0] = position4[0] - (distance_between_uav * (i + 1))
            temp_position[1] = position4[1]
            positions.append(temp_position)

        return positions


def v_formation_target_positions(reference_point, total_uav_count, distance_between_uav, angle):
    positions = []

    uav_count_between_corners = int(total_uav_count / 2)

    position1 = [reference_point[0], reference_point[1] - (int(total_uav_count / 4) * distance_between_uav)]
    positions.append(position1)

    for i in range(1, uav_count_between_corners + 1):
        temp_position = [0, 0]
        temp_position[0] = position1[0] + math.sin(math.radians(180 + (angle / 2 * 1))) * distance_between_uav * i
        temp_position[1] = position1[1] - math.cos(math.radians(180 + (angle / 2 * 1))) * distance_between_uav * i
        positions.append(temp_position)

        if len(positions) == total_uav_count:
            break

        temp_position = [0, 0]
        temp_position[0] = position1[0] + math.sin(math.radians(180 + (angle / 2 * -1))) * distance_between_uav * i
        temp_position[1] = position1[1] - math.cos(math.radians(180 + (angle / 2 * -1))) * distance_between_uav * i
        positions.append(temp_position)

    return positions


def crescent_formation_target_positions(reference_point, total_uav_count, radius):
    angle_between_uav = int(300 / total_uav_count)
    positions = []
    temp_angle = 0
    for i in range(0, total_uav_count):
        temp_angle = temp_angle + angle_between_uav
        temp_position = [0, 0]
        temp_position[0] = reference_point[0] + math.sin(math.radians(temp_angle)) * radius
        temp_position[1] = reference_point[1] - math.cos(math.radians(temp_angle)) * radius

        if 0.01 > temp_position[0] > -0.01:
            temp_position[0] = 0
        if 0.01 > temp_position[1] > -0.01:
            temp_position[1] = 0

        positions.append(temp_position)

    return positions


def circle_formation_target_positions(reference_point, total_uav_count, radius):
    angle_between_uav = int(360 / total_uav_count)
    positions = []
    temp_angle = 0
    for i in range(0, total_uav_count):
        temp_angle = temp_angle + angle_between_uav
        temp_position = [0, 0]
        temp_position[0] = reference_point[0] + math.sin(math.radians(temp_angle)) * radius
        temp_position[1] = reference_point[1] - math.cos(math.radians(temp_angle)) * radius

        if 0.01 > temp_position[0] > -0.01:
            temp_position[0] = 0
        if 0.01 > temp_position[1] > -0.01:
            temp_position[1] = 0

        positions.append(temp_position)

    return positions


def star_formation_target_positions(reference_point, total_uav_count, distance_between_uav):
    positions = []

    uav_count_between_corners = int(total_uav_count / 3)

    position1 = [reference_point[0], (reference_point[1] + distance_between_uav)]
    positions.append(position1)

    for i in range(1, uav_count_between_corners):
        temp_position = [0, 0]
        temp_position[0] = position1[0] + math.sin(math.radians(18)) * distance_between_uav * i
        temp_position[1] = position1[1] - math.cos(math.radians(18)) * distance_between_uav * i
        positions.append(temp_position)

        temp_position = [0, 0]
        temp_position[0] = position1[0] + math.sin(math.radians(-18)) * distance_between_uav * i
        temp_position[1] = position1[1] - math.cos(math.radians(-18)) * distance_between_uav * i
        positions.append(temp_position)

    ref1 = positions[len(positions) - 1]
    ref2 = positions[len(positions) - 2]

    for i in range(1, uav_count_between_corners):
        temp_position = [0, 0]
        temp_position[0] = ref1[0] + math.sin(math.radians(126)) * distance_between_uav * i
        temp_position[1] = ref1[1] - math.cos(math.radians(126)) * distance_between_uav * i
        positions.append(temp_position)

        temp_position = [0, 0]
        temp_position[0] = ref2[0] + math.sin(math.radians(-126)) * distance_between_uav * i
        temp_position[1] = ref2[1] - math.cos(math.radians(-126)) * distance_between_uav * i
        positions.append(temp_position)

    ref3 = positions[len(positions) - 1]
    for i in range(1, uav_count_between_corners):
        temp_position = [0, 0]
        temp_position[0] = ref3[0] + math.sin(math.radians(90)) * distance_between_uav * i
        temp_position[1] = ref3[1] - math.cos(math.radians(90)) * distance_between_uav * i
        positions.append(temp_position)

    positions.pop(len(positions) - 1)
    return positions
