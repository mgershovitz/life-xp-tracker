from flask import Flask, render_template, request, redirect
import os 
from db import add_quest_to_completed,  fetch_quests_from_notion


app = Flask(__name__)

@app.route('/')
def dropdown():
	quests = fetch_quests_from_notion()  # Fetch quests from the source database
	print(quests)
	return render_template('dropdown.html', quests=quests)

@app.route('/add-quest', methods=['GET'])
def add_quest():
    quest_name = request.args.get('quest')  # Get selected quest
    xp_value = request.args.get('xp')  # Get XP value for the selected quest

    # Make sure both quest name and XP value are present
    if quest_name and xp_value:
        try:
            xp_value = int(xp_value)  # Ensure XP is an integer
            if add_quest_to_completed(quest_name, xp_value):  # Add to the completed database
                return redirect('/')  # Redirect to the home page
            else:
                return "Failed to add quest to completed database", 500
        except ValueError:
            return "Invalid XP value", 400
    return "No quest or XP selected", 400

if __name__ == '__main__':
	port = int(os.environ.get('PORT', 4000))
	app.run(host="0.0.0.0", port=port)