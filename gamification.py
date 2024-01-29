
# Assigning points
def assign_points(standard_deviation, std_limit, point_limit):
    points = int(100 - (standard_deviation*100/(std_limit*100/point_limit)))
    # "limit*100/20" = std for which 0 points are assigned
    # assigns 100 points for std=0.0, 80 points for std=limit
    if points < 0:
        points = 0

    return points


# Assigning badges
def assign_badges(points, point_limit):
    badge = 0

    if points >= (100-point_limit):
        badge = 1

    return badge


# Next goal
def next_goal(achieved, goal_list):
    i = 0
    result = goal_list[0]
    while achieved >= goal_list[i]:
        result = goal_list[i+1]
        i += 1

    return result


# Progress bar
def progress_bar(progress_points, full_points):
    progress_portion = 100*progress_points/full_points

    return progress_portion
