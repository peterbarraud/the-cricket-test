from libs.dataclasses import GameInfo


def get_game_info(game_header):
    # tossWinner = game_header['tossResults'].get('tossWinnerId',0) # seems that for many games, we haven't got any toss details
    # descisionToBat = game_header['tossResults'].get('decision',None) == 'Batting' # seems that for many games, we haven't got any toss details
    game_info = GameInfo()
    game_info.Id = game_header['matchId']
    game_info.SeriesId = game_header['seriesId']
    game_info.Start = game_header['matchStartTimestamp']
    game_info.End = game_header['matchCompleteTimestamp']
    game_info.TossWinner = game_header['tossResults'].get('tossWinnerId',0)
    game_info.DescisionToBat = game_header['tossResults'].get('decision',None) == 'Batting'
    if game_header['team1']['name'] == game_header['venue']['country']:
        game_info.HomeTeamId = game_header['team1']['id']
        game_info.AwayTeamId = game_header['team2']['id']
    elif game_header['team2']['name'] == game_header['venue']['country']:
        game_info.HomeTeamId = game_header['team2']['id']
        game_info.AwayTeamId = game_header['team1']['id']
    if game_header['result'] and game_header['result'].get('winningteamId',False):
        game_info.Winner = game_header['result']['winningteamId']
        game_info.Margin = game_header['result']['winningMargin']
        game_info.IsWinByRuns = game_header['result']['winByRuns']
        game_info.IsInnningsWin = game_header['result']['winByInnings']
    return game_info

