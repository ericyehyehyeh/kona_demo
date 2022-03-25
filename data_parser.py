import json
import queue

# map id to real name
channelid_to_channel = {}
userid_to_name = {}


channels_to_teams = {}
# garentee has manerger, second manerger, directs
teams_to_member = {}
teamsid_to_team = {}
teams = {}

def parse_channels():
    global channelid_to_channel,channels_to_teams
    print("start parsing channel data")
    with open("data/channels.json") as channel_json:
        channels = json.load(channel_json)
    
    for channel_id, channel_info in channels.items():
        channelid_to_channel.update({channel_id:channel_info["name"]})
        channels_to_teams.update({channelid_to_channel[channel_id]:[]})

def parse_teams():
    global teams,teamsid_to_team,userid_to_name,teams_to_member,channels_to_teams
    print("start parsing team data")
    with open("data/teams.json") as team_json:
        teams = json.load(team_json)

    for user, userInfo in teams.items():
        userid_to_name.update({user:userInfo["realName"]})


    for user, userInfo in teams.items():
        if "teams" in userInfo:
            for id, team in userInfo["teams"].items():
                team_id = user + "&" +id
                teamsid_to_team.update({team_id:team})
                # create member list
                teams_to_member[team["name"]]={
                    "manager": "",
                    "s_manager": [],
                    "members": []
                }            
                teams_to_member[team["name"]]["manager"] = userid_to_name[user]
                for mem in team["s_manager"]:
                    if mem in userid_to_name:
                        teams_to_member[team["name"]]["s_manager"].append(userid_to_name[mem])
                    else:
                        print(f"error id: {mem}")
                
                for mem in team["directs"]:
                    if mem != user and mem not in team["s_manager"]:
                        if mem in userid_to_name:
                            teams_to_member[team["name"]]["members"].append(userid_to_name[mem])
                        else:
                            print(f"error id: {mem}")

                
    # build chanel tree by bfs
    for teams_id, team_info in teamsid_to_team.items():
        #find prime channel
        if "channel_id" in team_info["settings"]:
            channel_id = team_info["settings"]["channel_id"]
            # bfs
            queue = []
            queue.append(teams_id)
            
            while queue:
                top = queue.pop(0)
                channels_to_teams[channelid_to_channel[channel_id]].append(teamsid_to_team[top]["name"])
                if "consolidatedTeams" in teamsid_to_team[top]["settings"]:
                    for id in teamsid_to_team[top]["settings"]["consolidatedTeams"]:
                        queue.append(id)

     
def get_teams(channel):
    parse_channels()
    parse_teams()
    team_dic = {}
    for team in channels_to_teams[channel]:
        team_dic.update({team:teams_to_member[team]})
    return team_dic


def get_channel():
    parse_channels()
    channel_list = []
    for channels in channels_to_teams.keys():
        channel_list.append(channels)
    
    return channel_list
