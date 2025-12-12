import pandas

def clean_names(schools):
    schools = (
    schools.str.lower()
           .str.replace(" ", "-", regex=False)
           .str.replace("&", "", regex=False)
           .str.replace("(", "", regex=False)
           .str.replace(")", "", regex=False)
           .str.replace(".", "", regex=False)
           .str.replace("'", "", regex=False)
           .str.replace("unc-", "north-carolina-", regex=False)
           .str.replace("uc-", "california-", regex=False)   
    )

    # Fix school names for url
    fixes = {
        'bowling-green' : 'bowling-green-state',
        'east-texas-am' : 'texas-am-commerce',
        'william--mary' : 'william-mary',
        'fdu' : 'fairleigh-dickinson',
        'houston-christian' : 'houston-baptist',
        'iu-indy' : 'iupui',
        'kansas-city' : 'missouri-kansas-city',
        'little-rock' : 'arkansas-little-rock',
        'louisiana' : 'louisiana-lafayette',
        'nc-state' : 'north-carolina-state',
        'omaha' : 'nebraska-omaha',
        'purdue-fort-wayne' : 'ipfw',
        'sam-houston' : 'sam-houston-state',
        'siu-edwardsville' : 'southern-illinois-edwardsville',
        'st-thomas' : 'st-thomas-mn',
        'tcu' : 'texas-christian',
        'texas-rio-grande-valley' : 'texas-pan-american',
        'the-citadel' : 'citadel',
        'uab' : 'alabama-birmingham',
        'ucf' : 'central-florida',
        'ut-arlington' : 'texas-arlington',
        'utah-tech' : 'dixie-state',
        'utep' : 'texas-el-paso',
        'utsa' : 'texas-san-antonio',
        'vmi' : 'virginia-military-institute'
    }

    schools = schools.replace(fixes)

    return schools