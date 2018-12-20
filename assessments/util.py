from datetime import datetime
from decimal import Decimal

from cod_utils.util import date_json


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
    'SEV': 'State Equalized Value',
    'landvalue': 'Land Value',
    'landMap': 'Land Map Number',
    'RELATED': 'Related Parcel Number',
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
