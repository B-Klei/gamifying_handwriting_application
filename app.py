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
stdLimit = 1.5  # highest standard variation for which a badge is awarded
pointLimit = 20  # number of points earned for stdLimit

# program
exercisesCompleted = 0  # number of exercises completed
totalExercisePoints = 0  # points earned for one exercise
totalPoints = 0  # points earned for all exercises

accuracyPoints = 0  # points earned for accuracy
tiltPoints = 0  # points earned for tilt
pressurePoints = 0  # points earned for pressure

accuracyBadges = 0  # number of badges awarded for accuracy
tiltBadges = 0  # number of badges awarded for tilt
pressureBadges = 0  # number of badges awarded for pressure

x = "10 exercises"  # temporary

# Program
# Points, badges calculation
for attempt in data:
    exercisesCompleted += 1
    totalExercisePoints = 0

    # Accuracy
    stdAccuracy = attempt['accuracy_std']
    accuracyPoints = assign_points(float(stdAccuracy), stdLimit, pointLimit)
    accuracyBadges += assign_badges(accuracyPoints, pointLimit)
    totalExercisePoints += accuracyPoints

    # Tilt
    stdTilt = attempt['tilt_std']
    tiltPoints = assign_points(float(stdTilt), stdLimit, pointLimit)
    tiltBadges += assign_badges(accuracyPoints, pointLimit)
    totalExercisePoints += tiltPoints

    # Pressure
    stdPressure = attempt['pressure_std']
    pressurePoints = assign_points(float(stdPressure), stdLimit, pointLimit)
    pressureBadges += assign_badges(pressurePoints, pointLimit)
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
                    html.H4("Exercises"),
                    html.P(("Next badge: ", x)),
                    html.P(
                        (
                            dbc.Progress(value=progress_bar(exercisesCompleted, 10),
                                         color="purple", label=exercisesCompleted,
                                         style={"height": "20px", "width":"80%", "display": "inline-block"}),
                            "grey badge"
                        )
                    )
                ]
            ),
            style={"width": "50%", "display":"inline-block"},
        ),
        dbc.Card(
            dbc.CardBody(
                [
                    html.H4("Exercises"),
                    html.P(("Next badge: ", x)),
                    html.P(
                        (
                            dbc.Progress(value=progress_bar(exercisesCompleted, 10),
                                         color="purple", label=exercisesCompleted,
                                         style={"height": "20px", "width":"80%", "display":"inline-block"}),
                            "grey badge"
                        )
                    )
                ]
            ),
            style={"width": "50%", "display":"inline-block"},
        ),
        dbc.Card(
            dbc.CardBody(
                [
                    html.H4("Exercises"),
                    html.P(("Next badge: ", x)),
                    html.P(
                        (
                            dbc.Progress(value=progress_bar(exercisesCompleted, 10),
                                         color="purple", label=exercisesCompleted,
                                         style={"height": "20px", "width":"80%", "display":"inline-block"}),
                            "grey badge"
                        )
                    )
                ]
            ),
            style={"width": "50%", "display":"inline-block"},
        )
        ]
)

if __name__ == "__main__":
    app.run_server(debug=True)
