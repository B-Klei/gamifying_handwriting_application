
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


# Main program
"""def exercise_results(json_dict):
    # Variables
    global exercisesCompleted

    global totalExercisePoints
    global totalPoints

    global accuracyPoints
    global tiltPoints
    global pressurePoints

    global accuracyBadges
    global tiltBadges
    global pressureBadges

    exercisesCompleted = 0
    totalPoints = 0

    accuracyBadges = 0
    tiltBadges = 0
    pressureBadges = 0

    # Points, badges calculation
    for exercise in json_dict["exercises"]:
        exercisesCompleted += 1
        totalExercisePoints = 0

        for parameter in exercise["parameters"]:
            if parameter["name"] == "accuracy":
                accuracyPoints = assign_points(parameter["standard deviation"], 1.5)
                accuracyBadges += assign_badges(accuracyPoints)
                totalExercisePoints += accuracyPoints

            elif parameter["name"] == "tilt":
                tiltPoints = assign_points(parameter["standard deviation"], 1.5)
                tiltBadges += assign_badges(tiltPoints)
                totalExercisePoints += tiltPoints

            elif parameter["name"] == "pressure":
                pressurePoints = assign_points(parameter["standard deviation"], 1.5)
                pressureBadges += assign_badges(pressurePoints)
                totalExercisePoints += pressurePoints

            totalPoints += totalExercisePoints"""


# Progress bar
def progress_bar(progress_points, full_points):
    progress_portion = 100*progress_points/full_points

    return progress_portion
