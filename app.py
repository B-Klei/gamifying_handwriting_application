from dash import Dash, dcc, html
import dash_bootstrap_components as dbc
import csv
from gamification import *

# Open file and convert to json
with open("dummy.csv", mode='r') as file:
    csv_reader = csv.DictReader(file)
    data = []

    for row in csv_reader:
        data.append(row)

# Dash
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Variables
# limits
stdLimit = 1.5  #
pointLimit = 80  #

# program
exercisesCompleted = 0
totalExercisePoints = 0
totalPoints = 0

accuracyPoints = 0
tiltPoints = 0
pressurePoints = 0

accuracyBadges = 0
tiltBadges = 0
pressureBadges = 0

# Point lists
accuracyPointList = []  # list of all the accuracy points achieved
tiltPointList = []  # list of all the tilt points achieved
pressurePointList = []  # list of all the pressure points achieved

allGoals = [1, 5, 10, 25, 50, 100]

# Colours
accuracyColour = "#ff0055"
tiltColour = "#070091"
pressureColour = "#02c42f"

# Program
# Points, badges calculation
for attempt in data:
    exercisesCompleted += 1
    totalExercisePoints = 0

    # Accuracy
    stdAccuracy = attempt['accuracy_std']
    accuracyPoints = assign_points(float(stdAccuracy), stdLimit, 100-pointLimit)
    accuracyPointList.append(accuracyPoints)
    accuracyBadges += assign_badges(accuracyPoints, 100-pointLimit)
    totalExercisePoints += accuracyPoints

    # Tilt
    stdTilt = attempt['tilt_std']
    tiltPoints = assign_points(float(stdTilt), stdLimit, 100-pointLimit)
    tiltPointList.append(tiltPoints)
    tiltBadges += assign_badges(accuracyPoints, 100-pointLimit)
    totalExercisePoints += tiltPoints

    # Pressure
    stdPressure = attempt['pressure_std']
    pressurePoints = assign_points(float(stdPressure), stdLimit, 100-pointLimit)
    pressurePointList.append(pressurePoints)
    pressureBadges += assign_badges(pressurePoints, 100-pointLimit)
    totalExercisePoints += pressurePoints

    totalPoints += totalExercisePoints

# Layout
"""app.layout = html.Div(

    children=[

        html.H1(children="Avocado Analytics"),

        html.P(

            children=(

                "Analyze the behavior of avocado prices and the number"

                " of avocados sold in the US between 2015 and 2018"

            ),

        ),

        dcc.Graph(

            figure={

                "data": [

                    {

                        "x": data["Date"],

                        "y": data["AveragePrice"],

                        "type": "lines",

                    },

                ],

                "layout": {"title": "Average Price of Avocados"},

            },

        ),

        dcc.Graph(

            figure={

                "data": [

                    {

                        "x": data["Date"],

                        "y": data["Total Volume"],

                        "type": "lines",

                    },

                ],

                "layout": {"title": "Avocados Sold"},

            },

        ),

    ]

)"""

app.layout = html.Div(

    children=[

        dbc.Card(
            dbc.CardBody(
                [
                    html.H4("Exercise results"),
                    html.Div(
                        children=
                        [
                            html.P("Accuracy:"),
                            html.P("Tilt:"),
                            html.P("Pressure:")
                        ],
                        style={"display": "inline-block"}
                    ),
                    html.Div(
                        children=
                        [
                            html.P(accuracyPoints),
                            html.P(tiltPoints),
                            html.P(pressurePoints)
                        ],
                        style={"display": "inline-block"}
                    ),
                    html.Div(
                        children=
                        [
                            html.P(dbc.Progress(value=progress_bar(accuracyPoints, pointLimit), color=accuracyColour,
                                                label=accuracyPoints, style={"height": "20px", "width": "350px"})),
                            html.P(dbc.Progress(value=progress_bar(tiltPoints, pointLimit), color=tiltColour,
                                                label=tiltPoints, style={"height": "20px", "width": "350px"})),
                            html.P(dbc.Progress(value=progress_bar(pressurePoints, pointLimit), color=pressureColour,
                                                label=pressurePoints, style={"height": "20px", "width": "350px"}))
                        ],
                        style={"display": "inline-block"}
                    ),
                    html.Div(
                        children=
                        [
                            html.P("badge" if (accuracyPoints >= pointLimit) else "grey badge"),
                            html.P("badge" if (tiltPoints >= pointLimit) else "grey badge"),
                            html.P("badge" if (pressurePoints >= pointLimit) else "grey badge")
                        ],
                        style={"display": "inline-block"}
                    ),

                ]
            ),
            style={"width": "50%", "display": "inline-block"},
        ),
        dbc.Card(
            dbc.CardBody(
                [
                    html.H4("Exercises"),
                    html.P(("Next badge: ", next_goal(exercisesCompleted, allGoals), " exercises")),
                    html.P(
                        (
                            dbc.Progress(value=progress_bar(exercisesCompleted,
                                                            next_goal(exercisesCompleted, allGoals)),
                                         color="purple", label=exercisesCompleted,
                                         style={"height": "20px", "width": "80%", "display": "inline-block"}),
                            html.P("grey badge", style={"display": "inline-block"})
                        )
                    )
                ]
            ),
            style={"width": "50%", "display": "inline-block"},
        ),
        dbc.Card(
            dbc.CardBody(
                dcc.Graph(
                    figure={
                        "data": [
                            {
                                "x": [x for x in range(1, exercisesCompleted+1)],
                                "y": accuracyPointList,
                                "type": "lines",
                                "name": "accuracy",
                                "line": dict(color=accuracyColour),
                            },
{
                                "x": [x for x in range(1, exercisesCompleted+1)],
                                "y": tiltPointList,
                                "type": "lines",
                                "name": "tilt",
                                "line": dict(color=tiltColour),
                            },
{
                                "x": [x for x in range(1, exercisesCompleted+1)],
                                "y": pressurePointList,
                                "type": "lines",
                                "name": "pressure",
                                "line": dict(color=pressureColour),
                            },
                        ],
                        "layout": {"title": ""},
                    },
                ),
            ),
            style={"width": "50%", "display": "inline-block"},
        )
        ]
)

if __name__ == "__main__":
    app.run_server(debug=True)
