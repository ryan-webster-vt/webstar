'''
Converts team names from data source to URL compatable names
'''
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

'''

'''
def clean_opponent_names(schools):
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

    fixes = {
        'arkansas–pine-bluff' : 'arkansas-pine-bluff',
        'grambling-state' : 'grambling',
        'illinois–chicago' : 'illinois-chicago',
        'liu' : 'long-island-university',
        'louisiana–monroe' : 'louisiana-monroe',
        'loyola-chicago' : 'loyola-il',
        'umbc' : 'maryland-baltimore-county',
        'umass-lowell' : 'massachusetts-lowell',
        'ole-miss' : 'mississippi',
        'unlv' : 'nevada-las-vegas',
        'prairie-view-am' : 'prairie-view',
        'st-marys-ca' : 'saint-marys-ca',
        'usc-upstate' : 'south-carolina-upstate',
        'smu' : 'southern-methodist',
        'ut-martin' : 'tennessee-martin',
        'texas-am–corpus-christi' : 'texas-am-corpus-christi',
        'texas–rio-grande-valley' : 'texas-pan-american',
        'vcu' : 'virginia-commonwealth'
    }

    schools = schools.replace(fixes)

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

'''
Convert names into proper format for website
'''
def display_names(schools):
    fixes = {
        'Connecticut' : 'UConn',
        'Brigham Young' : 'BYU',
        'Saint Louis' : 'St. Louis',
        'Saint Marys Ca' : 'St. Mary\'s (CA)',
        'Saint Johns Ny' : 'St. John\'s',
        'North Carolina State' : 'NC State',
        'North Carolina' : 'UNC',
        'Southern Methodist' : 'SMU',
        'Miami Fl' : 'Miami (FL)',
        'Virginia Commonwealth' : 'VCU',
        'Ucla' : 'UCLA',
        'Texas Am' : 'Texas A&M',
        'South Florida' : 'USF',
        'Mcneese State' : 'McNeese State',
        'Texas Christian' : 'TCU',
        'Miami Oh' : 'Miami (OH)',
        'Louisiana State' : 'LSU',
        'Central Florida' : 'UCF',
        'Southern California' : 'USC',
        'North Carolina Wilmington' : 'NC Wilmington',
        'Stephen F Austin' : 'Stephen F. Austin',
        'Mississippi' : 'Ole Miss',
        'St Thomas Mn' : 'St. Thomas',
        'Texas Pan American' : 'UTRGV',
        'Depaul' : 'DePaul',
        'Illinois Chicago' : 'UIC',
        'Alabama Birmingham' : 'UAB',
        'Florida Atlantic' : 'FAU',
        'California Irvine' : 'UC Irvine',
        'William Mary' : 'William & Mary',
        'California San Diego' : 'UC San Diego',
        'California Baptist' : 'Cal Baptist',
        'Nevada Las Vegas' : 'UNLV',
        'Bowling Green State' : 'Bowling Green',
        'Saint Josephs' : 'St. Joseph\'s',
        'St Bonaventure' : 'St. Bonaventure',
        'College Of Charleston' : 'Charleston',
        'Tennessee Martin' : 'UT Martin',
        'Texas Arlington' : 'UT Arlington',
        'Florida International' : 'FIU',
        'Dixie State' : 'Utah Tech',
        'Long Island University' : 'LIU',
        'California Davis' : 'UC Davis',
        'Massachusetts' : 'UMass',
        'James Madison' : 'JMU',
        'Queens Nc' : 'Queens',
        'Texas Am Corpus Christi' : 'Texas A&M Corpus Christi',
        'North Carolina Asheville' : 'UNC Asheville',
        'Maryland Baltimore County' : 'UMBC',
        'Southeast Missouri State' : 'SE Missouri State',
        'Saint Peters' : 'St. Peters',
        'Nebraska Omaha' : 'Omaha',
        'North Carolina At' : 'North Carolina A&T',
        'Souther Illinois Edwardsville' : 'SIUE',
        'Ipfw' : 'IPFW',
        'Texas El Paso' : 'UTEP',
        'Grambling' : 'Grambling St.',
        'California Riverside' : 'UC Riverside',
        'Mount St Marys' : 'Mount St. Mary\'s',
        'Southeastern Louisiana' : 'SE Louisiana',
        'Massachusetts Lowell' : 'UMass Lowell',
        'Albany Ny' : 'Albany',
        'Texas Am Commerce' : 'East Texas A&M',
        'North Carolina Greensboro' : 'UNC Greensboro',
        'Louisiana Lafayette' : 'Louisiana',
        'Alabama Am' : 'Alabama A&M',
        'Njit' : 'NJIT',
        'Loyola Md' : 'Loyola Maryland',
        'Loyola Il' : 'Loyola Illinois',
        'Iupui' : 'IUPUI',
        'Florida Am' : 'Florida A&M',
        'North Carolina Central' : 'UNC Central',
        'Texas San Antonio' : 'UTSA',
        'Missouri Kansas City' : 'Kansas City',
        'Citadel' : 'The Citadel',
        'Saint Francis Pa' : 'St. Francis PA',
        'Virginia Military Institute' : 'VMI'
    }
    schools = schools.replace(fixes)
    return schools