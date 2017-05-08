ColNames = {
    "pnum": "parcel number",
    "relatedpnum": "related parcel",
    "propstreetcombined": "address",
    "ownername1": "owner",
    "ownername2": "additional owner",
    "ownerstreetaddr": "owner address",
    "ownercity": "owner city",
    "ownerstate": "owner state",
    "ownerzip": "owner zip",
    "xstreetname_0": "cross street",
    "xstreetname_1": "cross street",

    "resb_numresb": "residential buildings",
    "resb_occ": "residential building occupant",
    "resb_styhgt": "residential height",
    "resb_yearbuilt": "residential year built",
    "resb_bldgclass": "residential buidling class",
    "resb_plusminus": "",
    "resb_style": "residential building style",
    "resb_effage": "",
    "resb_depr": "",
    "resb_heat": "",
    "resb_nbed": "number of bedrooms",
    "resb_fullbaths": "full baths",
    "resb_halfbaths": "half baths",
    "resb_gartype": "garage type",
    "resb_fireplaces": "number of fire places",
    "resb_exterior": "exterior",
    "resb_floorarea": "floor area",
    "resb_groundarea": "ground area",
    "resb_basementarea": "basement area",
    "resb_garagearea": "garage area",
    "resb_avestyht": "",
    "resb_pricefloor": "",
    "resb_priceground": "",
    "resb_calcvalue": "",
    "resb_value": "",

    "cib_numcib": "commercial buildings",
    "cib_occ": "commercial occupant",
    "cib_yearbuilt": "year built",
    "cib_bldgclass": "commercial building class",
    "cib_effage": "",
    "cib_stories": "number of stories",
    "cib_floorarea": "floor area",
    "cib_pricefloor": "",
    "cib_calcvalue": "",
    "cib_value": "",
    "cibbedrooms": "",
    "cibunits": "number of units",
}


def clean_parcel_val(val):
    """
    Clean up a parcel value
    """
    if type(val) is str:
        val = val.strip()
    return val

def get_parcel_descriptions():
    """
    Return a dict of descriptions of parcel columns
    """
    descriptions = {}
    for col, desc in ColNames.items():
        if not desc:
            desc = col
        descriptions[col] = desc
    return descriptions