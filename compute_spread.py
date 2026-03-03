from scipy.stats import norm

def point_spread(away_off, away_def, home_off, home_def, hfa = 2.9, possesions = 67.3, neutral = False):
    away_net = away_off - away_def
    home_net = home_off - home_def

    scale_factor = possesions / 100

    home_value = (home_net - away_net) * scale_factor

    if (not neutral):
        home_value += hfa

    return home_value

def win_prob(home_value, std_dev = 10):
    home_wp = 1 - norm.cdf(0, loc=home_value, scale=std_dev)
    away_wp = 1 - home_wp
    return home_wp, away_wp