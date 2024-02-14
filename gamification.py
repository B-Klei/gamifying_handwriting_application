
# Assigning points
def assign_points(standard_deviation, std_limit, point_limit):
    # point calculation formula
    zero_points = std_limit*100/(100-point_limit)  # std for which 0 points are assigned
    points = int(100 - (standard_deviation*100/zero_points))  # points calculated and rounded down
    # 100 points assigned for "std = 0.0", "point_limit points" assigned for "std = std_limit"

    if points < 0:  # avoiding negative points
        points = 0

    return points


# Assigning badges
def assign_badges(points, point_limit):
    badge = 0  # establishing variable

    if points >= point_limit:  # if achieved points are above limit,
        badge = 1  # badge is awarded

    return badge


# Next goal
def next_goal(achieved, goal_list):
    i = 0  # iterating variable
    result = goal_list[0]  # initial value = first value in the list
    while goal_list[i] <= achieved:  # going through as long as the list item value is smaller than the achieved goal
        result = goal_list[i+1]  # result is the next goal in the list
        i += 1

    return result


# Progress bar
def progress_bar(progress_points, full_points):
    # calculating the achieved points portion in percentage
    progress_portion = 100*progress_points/full_points

    return progress_portion


# Badge Icon
def which_badge(display_badge, earned_badges_list):
    if display_badge in earned_badges_list:
        icon_src = "assets/badge_icon_black.png"
    else:
        icon_src = "assets/badge_icon_grey.png"

    return icon_src


# alt text
def which_alt(display_badge, earned_badges_list):
    if display_badge in earned_badges_list:
        alt_text = "badge earned"
    else:
        alt_text = "badge not yet earned"

    return alt_text
