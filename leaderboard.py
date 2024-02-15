# Primary sorting - sort badges
def sort_badges(dictionary_list):
    badges_numbers = []

    for student in dictionary_list:
        badges_numbers.append(int(student["total_badges"]))  # append number of total badges to list

    sorted_badges = list(dict.fromkeys(sorted(badges_numbers)))  # sort list and remove duplicates
    sorted_badges.reverse()  # reverse order

    return sorted_badges


# Secondary sorting - sort points if same number of badges
def sort_points(sorted_badges, dictionary_list):
    list_points = []  # list of lists of points earned by students with same number of badges

    for badgesNumber in sorted_badges:  # for each number of badges
        same_badge_list = []  # list of points earned by students with same number of badges

        for student in dictionary_list:  # go through each student
            if badgesNumber == int(student["total_badges"]):  # if they have the same number of badges
                same_badge_list.append(student["total_points"])  # append points to list

        same_badge_list_sorted = sorted(same_badge_list)  # sort list
        same_badge_list_sorted.reverse()  # reverse order
        list_points.append(same_badge_list_sorted)  # append list to another list

    return list_points


# Leaderboard
def leaderboard(dictionary_list):
    sorted_badges = sort_badges(dictionary_list)  # primary sorting
    list_points = sort_points(sorted_badges, dictionary_list)  # secondary sorting
    leaderboard_list = []
    i = 0

    for lists in list_points:  # go through sorted list
        for points in lists:
            for student in dictionary_list:
                if (sorted_badges[i] == int(student["total_badges"])) and (points == student["total_points"]):
                    # find the correct student based on number of badges and points
                    leaderboard_list.append(student)  # append student's data to list
        i += 1

    return leaderboard_list
