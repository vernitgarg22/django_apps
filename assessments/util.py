from datetime import datetime
from decimal import Decimal

from cod_utils.util import date_json


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

BSAColNames = {
    'PARCELNO': 'Parcel Number',
    'DISTRICT': 'District',
    'COUNCIL': 'City Council District',
    'ECF': 'ECF',
    'PROPADDR': 'Street Address',
    'PROPNO': 'Street Number',
    'PROPDIR': 'Street Direction',
    'PROPSTR': 'Street Name',
    'ZIPCODE': 'Zip Code',
    'TAXPAYER1': 'Tax Payer 1',
    'TAXPAYER2': 'Tax Payer 2',
    'TAXPADDR': 'Tax Payer Address',
    'TAXPCITY': 'Tax Payer City',
    'TAXPSTATE': 'Tax Payer State',
    'TAXPZIP': 'Tax Payer Zip Code',
    'propclass': 'Property Class',
    'PROPCLASS1': 'Property Class 1',
    'TAXSTATUS': 'Tax Status',
    'TAXSTATUS1': 'Tax Status 1',
    'zoning': 'Zoning',
    'TOTALSQFT': 'Total Sq Ft',
    'TOTALACREAGE': 'Total Acreage',
    'FRONTAGE': 'Frontage',
    'DEPTH': 'Depth',
    'useCode': 'Use Code',
    'PRE': 'PRE',
    'NEZ': 'NEZ',
    'MTT': 'MTT',
    'CIBFLAREA': 'CIB Floor Area',
    'CIBBLDGNO': 'CIB Building Number',
    'CIBYRBUILT': 'CIB Year Built',
    'RESFLAREA': 'Res Floor Area',
    'RESBLDGNO': 'Res Building Number',
    'RESYRBUILT': 'Res Year Built',
    'RESSYTLE': 'Res Style',
    'ISIMPROVED': 'Is Improved',
    'SALEPRICE': 'Sale Price',
    'SALEDATE': 'Sale Date',
    'ASV': 'Assessor Value',
    'ASV1': 'Assessor Value 1',
    'TXV': 'Taxable Value',
    'TXV1': 'Taxable Value 1',
    'SEV': 'SEV',
    'landvalue': 'Land Value',
    'landMap': 'Land Map Number',
    'RELATED': 'Related Parcl Number',
    'AKA': 'AKA',
    'SUBDIVISION': 'Subdivision',
    'RP': 'RP',
    'STATUS': 'Status',
    'LEGALDESC': 'Legal Description',
}


def clean_parcel_val(val):
    """
    Clean up a parcel value
    """
    if type(val) is str:
        val = val.strip()
    elif type(val) is datetime:
        val = date_json(val)
    elif type(val) is Decimal:
        val = float(val)
    return val

def get_parcel_descriptions():
    """
    Return a dict of descriptions of parcel columns
    """

    return BSAColNames
