import pandas as pd

from main.models import *


def GeneratePositionTable(pos, team, allPositions):
    addPos = ""
    if pos in ["LT", "LG", "C", "RG", "RT"]:
        addPos = "OL"
    elif pos == "DE":
        addPos = "EDGE"
    elif pos in ["FS", "SS"]:
        addPos = "S"

    players = team.playerteam_set.filter(player__position=pos)
    if addPos:
        players = players | team.playerteam_set.filter(player__position=addPos)

    rows = []
    for pt in players:
        p = pt.player
        rows.append(("<input type=\"number\" name=\"{}_string\" value=\"{}\">".format(pt.id, pt.string),
                     "<select name=\"{}_pos\">".format(pt.id) +
                     "".join(["<option value=\"{}\" {}>{}</option>".format(posOpt, "selected" if posOpt == pt.player.position else "", posOpt) for posOpt in allPositions]) +
                     "</select>",
                     p.first + " " + p.last,
                     pt.age,
                     p.height,
                     p.weight,
                     p.GetBadges(),
                     p.stars,
                     pt.string))
    df = pd.DataFrame(rows, columns=["String", "Position", "Name", "Age", "Height", "Weight", "Badges", "Stars", "StringSort"])
    df = df.sort_values(by="StringSort").reset_index(drop=True)
    df.index += 1
    df = df.drop(columns=["StringSort"])

    with pd.option_context("display.max_colwidth", -1):
        table = df.to_html(escape=False)

    return table


# takes the POST dict
def SaveChanges(postDict):
    print(postDict)
    for name, val in postDict.items():
        """if ptId != "csrfmiddlewaretoken":
            pt = PlayerTeam.objects.get(id=ptId)
            pt.string = s
            pt.save()"""

        if "_string" in name:
            ptId = name[:name.find("_")]
            pt = PlayerTeam.objects.get(id=ptId)
            pt.string = val
            pt.save()

        elif "_pos" in name:
            ptId = name[:name.find("_")]
            p = PlayerTeam.objects.get(id=ptId).player
            p.position = val
            p.save()
