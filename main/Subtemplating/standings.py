import pandas as pd


def GenerateStandingsOLD(conf, teams):
    prefix = """
    <section class="widget">
        <h3>{} ({})</h3>""".format(conf.name, conf.abbreviation)

    rows = []
    for t in teams:
        pct = 0.0
        if t.wins + t.losses > 0:
            pct = t.wins / (t.wins + t.losses)

        cPct = 0.0
        if t.conf_wins + t.conf_losses > 0:
            cPct = t.conf_wins / (t.conf_wins + t.conf_losses)

        rows.append((t.school.name, t.wins, t.losses, pct, t.conf_wins, t.conf_losses, cPct))
    df = pd.DataFrame(rows, columns=["Team", "Wins", "Losses", "Pct", "Conf. Wins", "Conf. Losses", "Conf. Pct"])
    df = df.sort_values(by="Conf. Pct", ascending=False)
    df = df.reset_index(drop=True)
    df.index = df.index + 1
    table = df.to_html()

    suffix = """</section>"""

    return prefix + table + suffix


def GenerateStandingsHTML(conf, teams):
    prefix = """
    <section class="widget">
        <h3>{} ({})</h3>""".format(conf.name, conf.abbreviation)

    table = ""
    if conf.division1:
        table += "<h4>{}</h4>".format(conf.division1)
        table += GenerateStandingsTable(teams.filter(school__division=conf.division1))

        table += "<h4>{}</h4>".format(conf.division2)
        table += GenerateStandingsTable(teams.filter(school__division=conf.division2))
    else:
        table = GenerateStandingsTable(teams)

    suffix = "</section>"

    return prefix + table + suffix


def GenerateStandingsTable(teams):
    rows = []
    for t in teams:
        pct = 0.0
        if t.wins + t.losses > 0:
            pct = t.wins / (t.wins + t.losses)

        cPct = 0.0
        if t.conf_wins + t.conf_losses > 0:
            cPct = t.conf_wins / (t.conf_wins + t.conf_losses)

        rows.append((TeamLink(t), t.wins, t.losses, pct, t.conf_wins, t.conf_losses, cPct))
    df = pd.DataFrame(rows, columns=["Team", "Wins", "Losses", "Pct", "Conf. Wins", "Conf. Losses", "Conf. Pct"])
    df = df.sort_values(by="Conf. Pct", ascending=False)
    df = df.reset_index(drop=True)
    df.index = df.index + 1
    table = df.to_html(escape=False)

    return table


# todo: replace this with non-hardcoded version (reverse?)
# todo: link to team, not school
def TeamLink(t):
    return "<a href=\"/team/{}\">{}</a>".format(t.id, t.school.abbreviation)
