# Dictionary
# Create badge dictionary for a category
def exercise_badges_dictionary(all_goals):
    badge_dictionary = {}

    if len(all_goals) > 0:
        for goal in all_goals:
            if goal == 1:
                badge_name = str(goal) + " exercise"
            else:
                badge_name = str(goal) + " exercises"
            badge_dictionary[badge_name] = goal
    return badge_dictionary


# Create badge dictionary for an attribute
def attribute_badges_dictionary(all_goals, attribute):
    badge_dictionary = {}

    if len(all_goals) > 0:
        for goal in all_goals:
            badge_name = str(goal) + "x " + attribute
            badge_dictionary[badge_name] = goal
    return badge_dictionary


# Create dictionary of all badges
def badges_dictionary(all_goals):
    badge_dictionary = {}
    attributes = ["accuracy", "tilt", "pressure"]

    badge_dictionary["completedExercisesBadges"] = exercise_badges_dictionary(all_goals)
    for attribute in attributes:
        badge_dictionary[(attribute + "Badges")] = attribute_badges_dictionary(all_goals, attribute)

    return badge_dictionary
