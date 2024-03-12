from dash import Dash, dcc, html
import dash_bootstrap_components as dbc
import csv
from gamification import *  # functions file
from leaderboard import *  # leaderboard sorting functions
from attribute import *  # attribute class
from badge_dictionary import *  # dictionary of badges
from dash.dependencies import Input, Output  # necessary for callback

# Opening main file, converting into a list of dictionaries
with open("dummy.csv", mode='r') as file:  # open file
    csv_reader = csv.DictReader(file)  # convert rows to dictionaries
    data = []

    for row in csv_reader:
        data.append(row)  # append each dictionary to list

# Opening leaderboard file, converting into a list of dictionaries
with open("leaderboard_dummy.csv", mode='r') as file:  # open file
    csv_reader = csv.DictReader(file)  # convert rows to dictionaries
    leaderboard_data = []

    for row in csv_reader:
        leaderboard_data.append(row)  # append each dictionary to list


# Dash
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Variables
# misc
pointLimit = 80  # number of points awarded for achieving std_limit
allGoals = [1, 5, 10, 25, 50, 100]  # list of all goals
badgesEarned = []  # list of earned badges
badgesDictionary = badges_dictionary(allGoals)  # dictionary of all the badges

# exercises
exercisesCompleted = 0  # number of completed exercises
totalExercisePoints = 0  # total points earned per exercise
totalPoints = 0  # total points earned

# objects
accuracy = Attribute(1.5, "#ff0055")  # accuracy object
tilt = Attribute(1.5, "#070091")  # tilt object
pressure = Attribute(1.5, "#02c42f")  # pressure object

# Program
# Points, badges calculation
for attempt in data:  # going through data
    exercisesCompleted += 1  # completed exercises counter
    totalExercisePoints = 0  # number of total points earned per exercise set to 0

    # Accuracy
    stdAccuracy = attempt['accuracy_std']  # getting the standard deviation value
    accuracy.points = assign_points(float(stdAccuracy), accuracy.std_limit, pointLimit)  # assigning points
    accuracy.point_list.append(accuracy.points)  # append points to list of points
    accuracy.badges += assign_badges(accuracy.points, pointLimit)  # badges counter
    totalExercisePoints += accuracy.points  # total exercise points counter

    # Tilt
    stdTilt = attempt['tilt_std']  # getting the standard deviation value
    tilt.points = assign_points(float(stdTilt), tilt.std_limit, pointLimit)  # assigning points
    tilt.point_list.append(tilt.points)  # append points to list of points
    tilt.badges += assign_badges(tilt.points, pointLimit)  # badges counter
    totalExercisePoints += tilt.points  # total exercise points counter

    # Pressure
    stdPressure = attempt['pressure_std']  # getting the standard deviation value
    pressure.points = assign_points(float(stdPressure), pressure.std_limit, pointLimit)  # assigning points
    pressure.point_list.append(pressure.points)  # append points to list of points
    pressure.badges += assign_badges(pressure.points, pointLimit)  # badges counter
    totalExercisePoints += pressure.points  # total exercise points counter

    totalPoints += totalExercisePoints  # total points counter

# Badges
for badge_category in badgesDictionary:  # going through categories
    if badge_category == "completedExercisesBadges":  # category Completed exercises
        for badge in badgesDictionary[badge_category]:  # going through badges
            if badgesDictionary[badge_category][badge] <= exercisesCompleted:  # if badge is earned
                badgesEarned.append(badge)  # append badge to list of earned badges

    elif badge_category == "accuracyBadges":  # category Accuracy
        for badge in badgesDictionary[badge_category]:  # going through badges
            if badgesDictionary[badge_category][badge] <= accuracy.badges:  # if badge is earned
                badgesEarned.append(badge)  # append badge to list of earned badges

    elif badge_category == "tiltBadges":  # category Tilt
        for badge in badgesDictionary[badge_category]:  # going through badges
            if badgesDictionary[badge_category][badge] <= tilt.badges:  # if badge is earned
                badgesEarned.append(badge)  # append badge to list of earned badges

    elif badge_category == "pressureBadges":  # category Pressure
        for badge in badgesDictionary[badge_category]:  # going through badges
            if badgesDictionary[badge_category][badge] <= pressure.badges:  # if badge is earned
                badgesEarned.append(badge)  # append badge to list of earned badges

# Layout
app.layout = html.Div(

    children=[
        dbc.Row(  # header row
            dbc.Card(  # Student info
                dbc.CardBody(
                    [
                        html.H1(data[0]["student_name"],  # Name
                                style={"display": "inline-block"}),
                        html.H5(["ID: ", data[0]["student_id"]],  # ID
                                style={"display": "inline-block"}),
                        html.H5(["Total points: ", totalPoints],  # Total points
                                style={"display": "inline-block"}),
                        html.H2(["Badges: ", len(badgesEarned)],  # Number of badges
                                style={"display": "inline-block", "float": "right"})
                    ]
                ),
                style={"width": "100%"},  # display full width
            ),

        ),
        dbc.Row(  # first row
            [
                dbc.Card(  # Exercise performance
                    dbc.CardBody(
                        [
                            html.H4("Last exercise"),  # heading
                            html.Div(  # attribute names
                                children=
                                [
                                    html.P("Accuracy:"),
                                    html.P("Tilt:"),
                                    html.P("Pressure:")
                                ],
                                style={"display": "inline-block", "line-height": "37px"}
                            ),
                            html.Div(  # attribute points
                                children=
                                [
                                    html.H5(accuracy.points, style={"margin": "17px 0px"}),  # points earned for accuracy
                                    html.H5(tilt.points, style={"margin": "17px 0px"}),  # points earned for tilt
                                    html.H5(pressure.points, style={"margin": "17px 0px"})  # points earned for pressure
                                ],
                                style={"display": "inline-block", "margin": "0px 25px 0px 10px"}
                            ),
                            html.Div(
                                children=
                                [
                                    html.P("0", style={"font-size": "12px", "margin": "7px 0px"}),
                                    html.P("0", style={"font-size": "12px", "margin": "7px 0px"}),
                                    html.P("0", style={"font-size": "12px", "margin": "7px 0px"})
                                ],
                                style={"display": "inline-block", "line-height": "37px"}
                            ),
                            html.Div(  # progress bars
                                children=
                                [
                                    html.P(
                                        dbc.Progress(
                                            value=progress_bar(accuracy.points, pointLimit),  # portion
                                            color=accuracy.colour,  # attribute colour
                                            style={"height": "20px", "width": "300px"}  # bar style
                                        ),
                                        style={"height": "35px"}  # paragraph style
                                    ),
                                    html.P(
                                        dbc.Progress(value=progress_bar(tilt.points, pointLimit),  # portion
                                                        color=tilt.colour,  # attribute colour
                                                        style={"height": "20px", "width": "300px"}),  # bar style
                                        style={"height": "35px"}  # paragraph style
                                    ),
                                    html.P(
                                        dbc.Progress(value=progress_bar(pressure.points, pointLimit),  # portion
                                                        color=pressure.colour,  # attribute colour
                                                        style={"height": "20px", "width": "300px"}),  # bar style
                                        style={"height": "35px"}  # paragraph style
                                    )
                                ],
                                style={"display": "inline-block"}  # display in the same line
                            ),
                            html.Div(
                                children=
                                [
                                    html.P(pointLimit, style={"font-size": "12px", "margin": "7px 0px"}),
                                    html.P(pointLimit, style={"font-size": "12px", "margin": "7px 0px"}),
                                    html.P(pointLimit, style={"font-size": "12px", "margin": "7px 0px"})
                                ],
                                style={"display": "inline-block", "line-height": "37px"}
                            )

                        ]
                    ),
                    style={"width": "50%", "display": "inline-block"},  # width, display in the same line
                ),
                dbc.Card(  # Completed exercises
                    dbc.CardBody(
                        [
                            html.H4("Exercises"),  # heading
                            html.P(
                                ("Next badge: ", next_goal(exercisesCompleted, allGoals),  # next goal text
                                    " exercises" if exercisesCompleted > 1 else " exercise"),  # pl/sg
                                style={"line-height": "37px"}
                            ),
                            html.P(
                                [
                                    dbc.Progress(
                                        value=progress_bar(exercisesCompleted,
                                                           next_goal(exercisesCompleted, allGoals)),  # portion
                                            color="purple", label=exercisesCompleted,  # attribute colour, label
                                            style={"height": "20px", "width": "80%", "display": "inline-block"}
                                    ),
                                    html.Div(
                                        html.Div(
                                            [
                                                html.Img(  # badge image
                                                    src="assets/badge_icon_grey.png",  # source
                                                    alt="next badge: " + str(next_goal(exercisesCompleted, allGoals)),
                                                    # alt text
                                                    width="100%",  # image width the size of div
                                                    className="badge-img"  # css
                                                ),
                                                html.Div(  # badge text
                                                    html.P(str(next_goal(exercisesCompleted, allGoals))),  # next goal
                                                    className="badge-text", style={"top": "20px"}  # css, text position
                                                )
                                            ], className="badge-div", style={"width": "40px"}  # css, badge size
                                        ), className="badge-upper-div"  # css
                                    )
                                ]
                            )
                        ]
                    ),
                    style={"width": "50%", "display": "inline-block"},  # display in the same line
                ),
            ]
        ),
        dbc.Row(  # second row
            [

                dbc.Card(  # Badge display
                    dbc.CardBody(
                        [
                            html.Div(
                                [
                                    html.H4("Badges"),  # Heading
                                    html.Ul(  # category list
                                        [
                                            html.Li(  # item in category list
                                                html.Ul(  # badge list
                                                    [
                                                        html.Li(  # item in badge list
                                                            html.Div(  # badge
                                                                html.Div(
                                                                    [
                                                                        html.Img(  # badge image
                                                                            src=which_badge(badge, badgesEarned),  # source
                                                                            alt=which_alt(badge, badgesEarned),  # alt text
                                                                            width="100%",  # image width the size of div
                                                                            className="badge-img"
                                                                        ),
                                                                        html.Div(
                                                                            html.P(badge),  # badge text
                                                                            className="badge-text"
                                                                        )
                                                                    ], className="badge-div"
                                                                ), className="badge-upper-div"
                                                            ),
                                                        ) for badge in badgesDictionary[category]  # for each badge in category
                                                    ], style={
                                                        "padding": "10px",  # padding
                                                        "listStyle": "none"  # no bullets
                                                    }
                                                ), style={"display": "inline-block", "padding": "5px"},  # show in line, padding
                                            ) for category in badgesDictionary  # for each category of badges
                                        ], style={"listStyle": "none", "padding": "0"}  # category list: no bullets, no padding
                                    )
                                ], style={"maxHeight": "400px", "overflow": "scroll"}  # make it scrollable
                            )
                        ]
                    ),
                    style={"width": "55%", "display": "inline-block"},  # card style
                ),
                dbc.Card(  # Leaderboard
                    dbc.CardBody(
                        [
                            html.Div(
                                [
                                    html.H4("Leaderboard"),  # heading
                                    html.Ul(  # leaderboard list
                                        [
                                            html.Li(  # item in the list
                                                dbc.Card(
                                                    dbc.CardBody(
                                                        [
                                                            html.H6(  # position
                                                                student["position"],
                                                                style={"display": "inline-block"}
                                                            ),
                                                            html.H6(  # student's name
                                                                student["student_name"],
                                                                style={"display": "inline-block", "margin": "0px 20px"}
                                                            ),
                                                            html.P(  # total points
                                                                ["Points: ", student["total_points"]],
                                                                style={
                                                                    "display": "inline-block",
                                                                    "position": "relative",
                                                                    "margin-left": "20px",
                                                                    "font-size": "15px"
                                                                }
                                                            ),
                                                            html.H5(  # number of badges
                                                                student["total_badges"],
                                                                style={"float": "right", "display": "inline-block"}
                                                            )
                                                        ]
                                                    ),
                                                    className="you"  # different class for this student
                                                    if (student["student_id"] == data[0]["student_id"])
                                                    else ""
                                                )
                                            ) for student in leaderboard(leaderboard_data)  # for each student in sorted list
                                        ], style={"listStyle": "none", "padding": "0"}  # no bullets, no padding
                                    )
                                ], style={"maxHeight": "400px", "overflow": "scroll"}  # make it scrollable
                            )
                        ]
                    ), style={"width": "35%", "display": "inline-block"}  # card style
                ),
            ]
        ),
        dbc.Row(
            [
                dbc.Card(  # Attribute graph
                    dbc.CardBody(
                        [
                            html.H4("Attributes overall"),  # title
                            dcc.RadioItems(  # radio items displayed horizontally
                                options=[
                                    {"label": "accuracy", "value": "accuracy_graph"},
                                    {"label": "tilt", "value": "tilt_graph"},
                                    {"label": "pressure", "value": "pressure_graph"}
                                ],
                                value="accuracy_graph", inline=True, id="radio", labelStyle={"margin": "10px"}
                            ),
                            dcc.Graph(id="attribute_graph"),  # graph, content from callback
                        ]
                    ),
                    style={"width": "50%", "display": "inline-block"},
                ),

                dbc.Card(
                    dbc.CardBody(
                        [
                            html.H4("Practice"),  # heading
                            dcc.Graph(
                               figure={
                                    "data": [
                                        {
                                            "x": [student["time_begin"][:10] for student in data],  # x-axis: dates
                                            "y": accuracy.point_list,  # y-axis: points earned for accuracy
                                            "type": "lines",  # graph type: line graph
                                            "name": "accuracy",
                                            "line": dict(color=accuracy.colour),  # line colour
                                        }
                                    ],
                                    "layout": {
                                        "yaxis": {"range": [0, 100], "title": "points"},  # y-axis fixed to full range of points, description
                                        "xaxis": {"title": "attempt"}  # x-axis description
                                    }
                                }
                            )
                        ]
                    ), style={"width": "50%", "display": "inline-block"}  # card style
                )
            ]
        )
    ]
)


# Callback
@app.callback(
    Output('attribute_graph', 'figure'),
    [Input(component_id='radio', component_property='value')]
)
def build_graph(value):
    if value == "accuracy_graph":  # value from radio items
        return {
            "data": [
                {
                    "x": [x for x in range(1, exercisesCompleted+1)],  # x-axis: attempt number
                    "y": accuracy.point_list,  # y-axis: points earned for accuracy
                    "type": "lines",  # graph type: line graph
                    "name": "accuracy",
                    "line": dict(color=accuracy.colour),  # line colour
                }
            ],
            "layout": {
                "yaxis": {"range": [0, 100], "title": "points"},  # y-axis fixed to full range of points, description
                "xaxis": {"title": "attempt"}  # x-axis description
            }
        }
    elif value == "tilt_graph":  # value from radio items
        return {
            "data": [
                {
                    "x": [x for x in range(1, exercisesCompleted+1)],  # x-axis: attempt number
                    "y": tilt.point_list,  # y-axis: points earned for tilt
                    "type": "lines",  # graph type: line graph
                    "name": "tilt",
                    "line": dict(color=tilt.colour),  # line colour
                }
            ],
            "layout": {
                "yaxis": {"range": [0, 100], "title": "points"},  # y-axis fixed to full range of points, description
                "xaxis": {"title": "attempt"}  # x-axis description
            }
        }
    elif value == "pressure_graph":  # value from radio items
        return {
            "data": [
                {
                    "x": [x for x in range(1, exercisesCompleted+1)],  # x-axis: attempt number
                    "y": pressure.point_list,  # y-axis: points earned for pressure
                    "type": "lines",  # graph type: line graph
                    "name": "pressure",
                    "line": dict(color=pressure.colour),  # line colour
                }
            ],
            "layout": {
                "yaxis": {"range": [0, 100], "title": "points"},  # y-axis fixed to full range of points, description
                "xaxis": {"title": "attempt"}  # x-axis description
            }
        }


# Display in browser
if __name__ == "__main__":
    app.run_server(debug=True)  # "debug=True": being able to edit while program is running
