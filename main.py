import os

from db import add_quest_to_completed, fetch_quests_from_notion, get_daily_xp_sum
from flask import Flask, redirect, render_template, request


app = Flask(__name__)


@app.route("/")
def dropdown():
    quests = fetch_quests_from_notion()  # Fetch quests from the source database
    print(quests)
    return render_template("dropdown.html", quests=quests)


@app.route("/add-quest", methods=["GET"])
def add_quest():
    quest_name = request.args.get("quest")  # Get selected quest
    xp_value = request.args.get("xp")  # Get XP value for the selected quest

    # Make sure both quest name and XP value are present
    if quest_name and xp_value:
        try:
            xp_value = int(xp_value)  # Ensure XP is an integer
            if add_quest_to_completed(
                quest_name, xp_value
            ):  # Add to the completed database
                return redirect("/")  # Redirect to the home page
            else:
                return "Failed to add quest to completed database", 500
        except ValueError:
            return "Invalid XP value", 400
    return "No quest or XP selected", 400


@app.route("/daily")
def index():
    # Get the daily XP sum
    daily_xp = get_daily_xp_sum()
    print(daily_xp)

    # Render the HTML page with the daily XP sum
    return render_template("daily.html", daily_xp=daily_xp)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 4000))
    app.run(host="0.0.0.0", port=port)
