import pandas as pd
import random as rd
from datetime import datetime


area_range = range(1, 22)
crm_cd_range = range(110, 957)
vict_sex_range = [0, 1, 2]
vict_descent_range = range(0, 20)
weapon_desc_range = range(0, 80)
case_range = [0, 1]


area_mapping = {
    1: "Central",
    2: "Rampart",
    3: "Southwest",
    4: "Hollenbeck",
    5: "Harbor",
    6: "Hollywood",
    7: "Wilshire",
    8: "West LA",
    9: "Van Nuys",
    10: "West Valley",
    11: "Northeast",
    12: "77th Street",
    13: "Newton",
    14: "Pacific",
    15: "N Hollywood",
    16: "Foothill",
    17: "Devonshire",
    18: "Southeast",
    19: "Mission",
    20: "Olympic",
    21: "Topanga",
}


crime_code_mapping = {
    510: "VEHICLE_STOLEN",
    330: "BURGLARY_FROM_VEHICLE",
    480: "BIKE - STOLEN",
    343: "SHOPLIFTING-GRAND_THEFT_($950.01&OVER)",
    354: "THEFT OF IDENTITY",
    624: "BATTERY - SIMPLE ASSAULT",
    821: "SODOMY/SEXUAL CONTACT B/W PENIS OF ONE PERSON TO ANUS OF OTHER",
    812: "CHILD ABUSE (13 OR UNDER) (14-15 & SUSPECT 10 YRS OLDER)",
    810: "SEX,UNLAWFUL(INC MUTUAL CONSENT, PENETRATION W/ FRGN OBJ",
    230: "ASSAULT WITH DEADLY WEAPON, AGGRAVATED ASSAULT",
    956: "LETTERS, LEWD  -  TELEPHONE CALLS, LEWD",
    341: "THEFT-GRAND ($950.01 & OVER)EXCPT,GUNS,FOWL,LIVESTK,PROD",
    930: "CRIMINAL THREATS - NO WEAPON DISPLAYED",
    668: "EMBEZZLEMENT, GRAND THEFT ($950.01 & OVER)",
    420: "THEFT FROM MOTOR VEHICLE - PETTY ($950 & UNDER)",
    813: "CHILD ANNOYING (17YRS & UNDER)",
    440: "THEFT PLAIN - PETTY ($950 & UNDER)",
    626: "INTIMATE PARTNER - SIMPLE ASSAULT",
    762: "LEWD CONDUCT",
    441: "THEFT PLAIN - ATTEMPT",
    310: "BURGLARY",
    331: "THEFT FROM MOTOR VEHICLE - GRAND ($950.01 AND OVER)",
    210: "ROBBERY",
    662: "BUNCO, GRAND THEFT",
    860: "BATTERY WITH SEXUAL CONTACT",
    236: "INTIMATE PARTNER - AGGRAVATED ASSAULT",
    820: "ORAL COPULATION",
    661: "UNAUTHORIZED COMPUTER ACCESS",
    901: "VIOLATION OF RESTRAINING ORDER",
    442: "SHOPLIFTING - PETTY THEFT ($950 & UNDER)",
    740: "VANDALISM - FELONY ($400 & OVER, ALL CHURCH VANDALISMS)",
    946: "OTHER MISCELLANEOUS CRIME",
    761: "BRANDISH WEAPON",
    649: "DOCUMENT FORGERY / STOLEN FELONY",
    845: "SEX OFFENDER REGISTRANT OUT OF COMPLIANCE",
    121: "RAPE, FORCIBLE",
    745: "VANDALISM - MISDEMEANOR ($399 OR UNDER)",
    627: "CHILD ABUSE (PHYSICAL) - SIMPLE ASSAULT",
    653: "CREDIT CARDS, FRAUD USE ($950.01 & OVER)",
    928: "THREATENING PHONE CALLS/LETTERS",
    815: "SEXUAL PENETRATION W/FOREIGN OBJECT",
    940: "EXTORTION",
    625: "OTHER ASSAULT",
    352: "PICKPOCKET",
    648: "ARSON",
    886: "DISTURBING THE PEACE",
    666: "BUNCO, ATTEMPT",
    921: "HUMAN TRAFFICKING - INVOLUNTARY SERVITUDE",
    805: "PIMPING",
    932: "PEEPING TOM",
    900: "VIOLATION OF COURT ORDER",
    903: "CONTEMPT OF COURT",
    439: "FALSE POLICE REPORT",
    954: "CONTRIBUTING",
    434: "FALSE IMPRISONMENT",
    235: "CHILD ABUSE (PHYSICAL) - AGGRAVATED ASSAULT",
    220: "ATTEMPTED ROBBERY",
    654: "CREDIT CARDS, FRAUD USE ($950 & UNDER",
    922: "CHILD STEALING",
    760: "LEWD/LASCIVIOUS ACTS WITH CHILD",
    670: "EMBEZZLEMENT, PETTY THEFT ($950 & UNDER)",
    850: "INDECENT EXPOSURE",
    237: "CHILD NEGLECT (SEE 300 W.I.C.)",
    763: "STALKING",
    345: "DISHONEST EMPLOYEE - GRAND THEFT",
    888: "TRESPASSING",
    320: "BURGLARY, ATTEMPTED",
    122: "RAPE, ATTEMPTED",
    753: "DISCHARGE FIREARMS/SHOTS FIRED",
    822: "HUMAN TRAFFICKING - COMMERCIAL SEX ACTS",
    520: "VEHICLE - ATTEMPT STOLEN",
    806: "PANDERING",
    906: "FIREARMS RESTRAINING ORDER (FIREARMS RO)",
    437: "RESISTING ARREST",
    410: "BURGLARY FROM VEHICLE, ATTEMPTED",
    350: "THEFT, PERSON",
    623: "BATTERY POLICE (SIMPLE)",
    522: "VEHICLE, STOLEN - OTHER (MOTORIZED SCOOTERS, BIKES, ETC)",
    450: "THEFT FROM PERSON - ATTEMPT",
    890: "FAILURE TO YIELD",
    755: "BOMB SCARE",
    231: "ASSAULT WITH DEADLY WEAPON ON POLICE OFFICER",
    664: "BUNCO, PETTY THEFT",
    251: "SHOTS FIRED AT INHABITED DWELLING",
    951: "DEFRAUDING INNKEEPER/THEFT OF SERVICES, $950 & UNDER",
    920: "KIDNAPPING - GRAND ATTEMPT",
    250: "SHOTS FIRED AT MOVING VEHICLE, TRAIN OR AIRCRAFT",
    470: "TILL TAP - GRAND THEFT ($950.01 & OVER)",
    902: "VIOLATION OF TEMPORARY RESTRAINING ORDER",
    647: "THROWING OBJECT AT MOVING VEHICLE",
    651: "DOCUMENT WORTHLESS ($200.01 & OVER)",
    910: "KIDNAPPING",
    110: "CRIMINAL HOMICIDE",
    351: "PURSE SNATCHING",
    421: "THEFT FROM MOTOR VEHICLE - ATTEMPT",
    444: "DISHONEST EMPLOYEE - PETTY THEFT",
    814: "CHILD PORNOGRAPHY",
    756: "WEAPONS POSSESSION/BOMBING",
    433: "DRIVING WITHOUT OWNER CONSENT (DWOC)",
    931: "REPLICA FIREARMS(SALE,DISPLAY,MANUFACTURE OR DISTRIBUTE)",
    435: "LYNCHING",
    438: "RECKLESS DRIVING",
    443: "SHOPLIFTING - ATTEMPT",
    660: "COUNTERFEIT",
    950: "DEFRAUDING INNKEEPER/THEFT OF SERVICES, OVER $950.01",
    622: "BATTERY ON A FIREFIGHTER",
    943: "CRUELTY TO ANIMALS",
    487: "BOAT - STOLEN",
    949: "ILLEGAL DUMPING",
    933: "PROWLER",
    865: "DRUGS, TO A MINOR",
    474: "THEFT, COIN MACHINE - PETTY ($950 & UNDER)",
    652: "DOCUMENT WORTHLESS ($200 & UNDER)",
    113: "MANSLAUGHTER, NEGLIGENT",
    446: "PETTY THEFT - AUTO REPAIR",
    475: "THEFT, COIN MACHINE - ATTEMPT",
    471: "TILL TAP - PETTY ($950 & UNDER)",
    451: "PURSE SNATCHING - ATTEMPT",
    436: "LYNCHING - ATTEMPTED",
    485: "BIKE - ATTEMPT STOLEN",
    944: "CONSPIRACY",
    349: "GRAND THEFT / AUTO REPAIR",
    942: "BRIBERY",
    347: "GRAND THEFT / INSURANCE FRAUD",
    353: "DRUNK ROLL",
    870: "CHILD ABANDONMENT",
    473: "THEFT, COIN MACHINE - GRAND ($950.01 & OVER)",
    880: "DISRUPT SCHOOL",
    452: "PICKPOCKET, ATTEMPT",
    924: "TELEPHONE PROPERTY - DAMAGE",
    840: "BEASTIALITY, CRIME AGAINST NATURE SEXUAL ASSAULT WITH ANIMAL",
    948: "BIGAMY",
    884: "FAILURE TO DISPERSE",
    904: "FIREARMS EMERGENCY PROTECTIVE ORDER (FIREARMS EPO)",
    830: "INCEST (SEXUAL ACTS BETWEEN BLOOD RELATIVES)",
    432: "BLOCKING DOOR INDUCTION CENTER",
    882: "INCITING A RIOT",
    445: "DISHONEST EMPLOYEE ATTEMPTED THEFT",
    926: "TRAIN WRECKING",
}


def get_prediction(seed=42):
    rd.seed(seed)
    current_date = datetime.now()
    current_month = current_date.month
    current_year = current_date.year
    current_day = current_date.day

    # Initialize the data dictionary
    data = {
        "AREA": [],
        "Crm Cd": [],
        "dates": [],
        "Risk": [],  # Include Risk column
        "Probability": [],  # New Probability column
    }

    # Track indices already marked as high risk
    high_risk_indices = set()

    # getting dates for the current month and the next two months
    dates = []
    for month_offset in range(3):
        target_month = current_month + month_offset
        target_year = current_year

        # Adjust year if month rolls over
        if target_month > 12:
            target_month -= 12
            target_year += 1

        # Generate dates for the target month
        for day in range(1, 32):
            try:
                future_date = datetime(target_year, target_month, day)
                if future_date > current_date:
                    dates.append(f"{day:02d}/{target_month:02d}/{target_year}")
            except ValueError:
                # Skip invalid dates like February 30
                continue

    print(f"Dates: {dates}")

    for date in dates:
        num_predictions = rd.randint(15, 20)
        for i in range(num_predictions):
            data["AREA"].append(rd.choice(area_range))
            data["Crm Cd"].append(rd.choice(crm_cd_range))
            data["dates"].append(date)
            data["Risk"].append("High")
            data["Probability"].append(
                round(rd.uniform(80, 100), 2)
            )  # Placeholder for probability

    # create dataframe
    df = pd.DataFrame(data)

    # Map AREA and Crm Cd to their descriptions
    df["AREA NAME"] = df["AREA"].map(area_mapping)
    df["Crm Cd Desc"] = df["Crm Cd"].map(crime_code_mapping)

    # Filter for high-risk rows
    high_risk_df = df[df["Risk"] == "High"]

    # Select specified columns
    high_risk_df = high_risk_df[
        ["dates", "AREA NAME", "Crm Cd Desc", "Risk", "Probability",]
    ]

    # Clean NaN values for JSON compatibility
    high_risk_df = high_risk_df.dropna()

    # Convert to JSON
    high_risk_json = high_risk_df.to_json(orient="records")

    # Save to file (optional)
    with open("high_risk_data.json", "w") as f:
        f.write(high_risk_json)

    return high_risk_json


# Generate predictions once and save the result
high_risk_json = get_prediction()
