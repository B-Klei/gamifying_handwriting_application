from dash import Dash, dcc, html
import dash_bootstrap_components as dbc
import csv
from gamification import *  # functions file
from attribute import *  # attribute class
from badge_dictionary import *  # dictionary of badges
from dash.dependencies import Input, Output  # necessary for callback

# Opening file, converting into a list of dictionaries
with open("dummy.csv", mode='r') as file:
    csv_reader = csv.DictReader(file)
    data = []

    for row in csv_reader:
        data.append(row)

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
                        html.H1(data[0]["student_name"], style={"display": "inline-block"}),  # Name
                        html.H5(["ID: ", data[0]["student_id"]], style={"display": "inline-block"}),  # ID
                        html.H5(["Total points: ", totalPoints], style={"display": "inline-block"}),  # Total points
                        html.H2(["Badges: ", len(badgesEarned)], style={"display": "inline-block", "float": "right"})  # Number of badges
                    ]
                ),
                style={"width": "100%", "position": "sticky"},  # display full width, stick to top
            ),

        ),
        dbc.Row(  # first row
            [
                dbc.Card(  # Exercise performance
                    dbc.CardBody(
                        [
                            html.H4("Exercise performance"),  # heading
                            html.Div(  # attribute names
                                children=
                                [
                                    html.P("Accuracy:"),
                                    html.P("Tilt:"),
                                    html.P("Pressure:")
                                ],
                                style={"display": "inline-block"}  # display in the same line
                            ),
                            html.Div(  # attribute points
                                children=
                                [
                                    html.P(accuracy.points),
                                    html.P(tilt.points),
                                    html.P(pressure.points)
                                ],
                                style={"display": "inline-block"}  # display in the same line
                            ),
                            html.Div(  # progress bars
                                children=
                                [
                                    html.P(dbc.Progress(value=progress_bar(accuracy.points, pointLimit),  # portion
                                                        color=accuracy.colour,  # attribute colour
                                                        style={"height": "20px", "width": "300px"})),
                                    html.P(dbc.Progress(value=progress_bar(tilt.points, pointLimit),
                                                        color=tilt.colour,
                                                        style={"height": "20px", "width": "300px"})),
                                    html.P(dbc.Progress(value=progress_bar(pressure.points, pointLimit),
                                                        color=pressure.colour,
                                                        style={"height": "20px", "width": "300px"}))
                                ],
                                style={"display": "inline-block"}  # display in the same line
                            ),
                            html.Div(  # badges, displayed in grey if not achieved
                                children=
                                [
                                    html.P("badge" if (accuracy.points >= pointLimit) else "grey badge"),
                                    html.P("badge" if (tilt.points >= pointLimit) else "grey badge"),
                                    html.P("badge" if (pressure.points >= pointLimit) else "grey badge")
                                ],
                                style={"display": "inline-block"}  # display in the same line
                            ),

                        ]
                    ),
                    style={"width": "50%", "display": "inline-block"},  # width, display in the same line
                ),
                dbc.Card(  # Completed exercises
                    dbc.CardBody(
                        [
                            html.H4("Exercises"),  # heading
                            html.P(("Next badge: ", next_goal(exercisesCompleted, allGoals), " exercises")),
                            # <- next goal
                            html.P(
                                (
                                    dbc.Progress(value=progress_bar(exercisesCompleted,
                                                                    next_goal(exercisesCompleted, allGoals)),  # portion
                                                 color="purple", label=exercisesCompleted,  # attribute colour, label
                                                 style={"height": "20px", "width": "80%", "display": "inline-block"}),
                                    html.P("grey badge", style={"display": "inline-block"})  # grey badge
                                )
                            )
                        ]
                    ),
                    style={"width": "50%", "display": "inline-block"},  # display in the same line
                ),
            ]
        ),
        dbc.Row(  # second row
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
                    style={"width": "45%", "display": "inline-block"},
                ),
                dbc.Card(  # Badge display
                    dbc.CardBody(
                        [
                            html.H4("Badges"),  # Heading
                            html.Ul(  # category list
                                [
                                    html.Li(  # item in category list
                                        html.Ul(  # badge list
                                            [
                                                html.Li(  # item in badge list
                                                    html.Div(  # badge div
                                                        [
                                                            html.Img(src=which_badge(badge, badgesEarned),
                                                                 alt=which_alt(badge, badgesEarned),
                                                                 width="100px"),
                                                            badge
                                                        ]
                                                    ), style={"padding": "10px"}
                                                ) for badge in badgesDictionary[category]  # for each badge in category
                                            ], style={#"display": "inline-block",  # show in line
                                                      "padding": "10px",  # padding
                                                      "listStyle": "none"}  # no bullets
                                        ), style={"display": "inline-block", "padding": "5px"},  # show in line, padding
                                    ) for category in badgesDictionary  # for each category of badges
                                ], style={"listStyle": "none", "padding": "0"}  # category list: no bullets, no padding
                            )
                        ]
                    ),
                    style={"width": "55%", "display": "inline-block"},  # card style
                )
            ]
        ),
        dbc.Row(
            dbc.Card(
                dbc.CardBody(
                    [
                        html.Img(src=r"assets/badge_icon_black.png",
                                 alt="badge earned", width="50px")
                    ]
                )
            )
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
