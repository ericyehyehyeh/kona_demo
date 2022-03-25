var current_channel = ""

$(document).ready(function () {
    var element = document.getElementById("side_list");
    let default_channel = element.firstElementChild.firstElementChild;
    current_channel = default_channel.id
    document.getElementById(current_channel).className = "nav-link text-white active";

    // make live call to backend
    get_teams_information(current_channel)
})


function channel_hit(element_in) {
    document.getElementById(current_channel).className = "nav-link text-white";
    element_in.className = "nav-link text-white active";
    current_channel = element_in.id;
    document.getElementById("Org_title").innerHTML = "<b>#" + current_channel + " Organization Chart</b>";
    get_teams_information(current_channel)
}

function generate_name_tag(name, title) {
    html = '<div class="col-md-3"><div class="bg-white text-center rounded box">'
    if (title === "Team Manager") {
        html += '<h5 class="mt-3 name text-primary">'
    }
    else if (title === "Secondary Manager") {
        html += '<h5 class="mt-3 name text-info">'
    }
    else {
        html += '<h5 class="mt-3 name">'
    }
    html += name +'</h5><span class="work d-block">'+title+'</span></div></div>'
    return html
}

function get_teams_information(channel) {
    $.ajax(
        {
            type: "GET",
            url: "/team",
            dataType: "json",
            data: { "id": channel },
            success: function (data) {
        
                if (document.getElementById("team_block_new")){
                    document.getElementById("team_block").style.visibility = "visible";
                    document.getElementById("team_block_new").remove();
                }
                

                var new_value = "";

                var count = 0;
                const element_team = document.getElementById("team_block");
                var clone_element = element_team.cloneNode(true);
                const element_name = document.getElementById("team_name");
                var clone_name = element_name.cloneNode(true);
                const element_member = document.getElementById("team_mem_row");
                var clone_member = element_member.cloneNode(true);

                
                for (const[team,team_member] of Object.entries(data)) {               
                    clone_element.id = "team_block" + count.toString();
                    clone_name.innerHTML = team;
                    clone_name.id = "team_name" + count.toString();

                    var member_html = "";
                    member_html += generate_name_tag(team_member["manager"], "Team Manager")
                    // s_manager showing
                    for (let i in team_member["s_manager"]) {
                        member_html += generate_name_tag(team_member["s_manager"][i], "Secondary Manager")
                    }
                    // members showing
                    for (let i in team_member["members"]) {
                        member_html += generate_name_tag(team_member["members"][i], "Team Member")
                    }

                    clone_member.innerHTML = member_html;
                    clone_member.id = "team_mem_row" + count.toString();
                    
                    element_name.after(clone_name);
                    element_member.after(clone_member);                  
                    element_team.after(clone_element);
                    new_value = new_value + element_team.innerHTML;
                    count = count + 1;
                }
                count = count - 1;
                document.getElementById("team_block").innerHTML = new_value;
                document.getElementById("team_block").id = "team_block_new";

                document.getElementById("team_block" + count.toString()).id = "team_block";
                document.getElementById("team_block").style.visibility = "hidden";

            }
        });
}