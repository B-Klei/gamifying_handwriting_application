# Sort badges
def sort_badges(dictionary_list):
    badges_numbers = []

    for student in dictionary_list:
        badges_numbers.append(int(student["total_badges"]))

    sorted_badges = list(dict.fromkeys(sorted(badges_numbers)))
    sorted_badges.reverse()

    return sorted_badges


# Sort points if same number of badges
def sort_points(sorted_badges, dictionary_list):
    list_points = []

    for badgesNumber in sorted_badges:
        same_badge_list = []
        for student in dictionary_list:
            if badgesNumber == int(student["total_badges"]):
                same_badge_list.append(student["total_points"])
        same_badge_list_sorted = sorted(same_badge_list)
        same_badge_list_sorted.reverse()
        list_points.append(same_badge_list_sorted)

    return list_points


# Leaderboard
def leaderboard(dictionary_list):
    sorted_badges = sort_badges(dictionary_list)
    list_points = sort_points(sorted_badges, dictionary_list)
    leaderboard_list = []

    for lists in list_points:
        for points in lists:
            for student in dictionary_list:
                if points == student["total_points"]:
                    leaderboard_list.append(student)

    return leaderboard_list
