from flask import Flask, render_template
from db import getActivities  
import os 

app = Flask(__name__)

@app.route('/')
def dropdown():
	activities = getActivities()  # Fetch items from the Notion database
	return render_template('dropdown.html', items=activities)

if __name__ == '__main__':
	port = int(os.environ.get('PORT', 4000))
	app.run(host="0.0.0.0", port=port)