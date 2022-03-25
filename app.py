from flask import Flask, render_template, request, jsonify
from data_parser import get_channel, get_teams


app = Flask(__name__)

@app.route('/')
def index():

    Channels_list = get_channel()

    Current_Channel = Channels_list[0]
    
    return render_template('index.html',Channels = Channels_list, Current_Channel = Current_Channel)
    

@app.route('/team')
def team():
    channel = request.args.get("id")
    teams_list = get_teams(channel)
    return jsonify(teams_list)

if __name__ == "__main__":
    app.run(debug = True)
