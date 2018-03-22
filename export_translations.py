#!/usr/bin/env python
import os
import sys
import requests
from requests.auth import HTTPBasicAuth

import django
from django.conf import settings


# REVIEW:  remove all medical marijuana links?
# REVIEW:  remove all FAQ links?  or change them to actually pull the contents of the faq content (not the page that the faq lives in)


server = "http://detroitmi.theneighborhoods.org"
urls = [
    "/fintreasury",
    "/businessincometax",
    "/doglicense",
    "/BSEED",
    "/Government/Departments-and-Agencies/Law-Department",
    "/Government/Departments-and-Agencies/Public-Works/Contact-us",
    "/Government/Departments-and-Agencies/Public-Works/Curbside-Bulk-Waste-Pickup",
    "/Government/Departments-and-Agencies/Public-Works/Recycle",
    "/How-Do-I/Apply-for-Licenses/Business-License-Checklist",
    "/How-Do-I/Apply-for-Permits/Zoning-Permit-Information",
    "/How-Do-I/Do-Business-with-the-City/Open-Bids-for-the-City-of-Detroit",
    "/IncomeTax",
    "/Supplier",
    "/Boards/BoardOfPoliceCommissioners",
    "/dwsd",
    "/projectcleanslate",
    "/Correspondence",
    "/DACC",
    "/Demolition",
    "/Detroit-Demolition-Program/View-All-Demolitions",
    "/Government/Departments-and-Agencies/Office-of-the-Chief-Financial-Office/Office-of-the-Assessor",
    "/Government/Departments-and-Agencies/Water-and-Sewerage-Department/About-DWSD",
    "/Government/Departments-and-Agencies/Water-and-Sewerage-Department/Learn-About-Your-Water-and-Sewer-Bill",
    "/How-Do-I/Apply-for-Permits/Zoning-Permit-Forms",
    "/How-Do-I/File/Blight-Complaint",
    "/How-Do-I/Find-Community-Services/Arson-Awareness",
    "/How-Do-I/Find/Adams-Butzel-Complex",
    "/How-Do-I/Find/Detroit-Parks-Recreation/Parks-Recreation-Forms",
    "/How-Do-I/Medical-Marihuana-Information",
    "/How-Do-I/Pay/Property-Taxes-FAQs",
    "/How-Do-I/Pay/Property-Taxes-Information",
    "/How-Do-I/Report/Crime",
    "/MedicalMarihuana",
    "/PublicWorks",
    "/Purchasing",
    "/elections",
    "/employment",
    "/health",
    "/parking",
    "/recreation",
    "/rental",
    "/rental/property-registration",
    "/Calendar-and-Events",
    "/CampauBanglatown",
    "/DDOT",
    "/Detroit-Opportunities",
    "/Detroit-Opportunities/Find-A-Job",
    "/Detroit-Opportunities/Help-with-your-Home",
    "/Detroit-Opportunities/Programs-for-Youth",
    "/Detroit-Opportunities/Start-or-Grow-Your-Business",
    "/Detroit-Opportunities/Start-or-Grow-Your-Business/Contractor-for-Rehabbed-and-Ready-Program",
    "/Drainage",
    "/DWSDCustomerCare",
    "/DWSDkiosk",
    "/DWSDSkipTheLine",
    "/Government/Boards/Board-of-Electrical-Examiners-Forms",
    "/Government/City-Clerk",
    "/Government/City-Council",
    "/Government/City-Council/Andre-Spivey",
    "/Government/City-Council/Brenda-Jones",
    "/Government/City-Council/City-Council-Sessions",
    "/Government/City-Council/Gabe-Leland",
    "/Government/City-Council/James-Tate",
    "/Government/City-Council/Janee-L-Ayers",
    "/Government/City-Council/Mary-Sheffield",
    "/Government/City-Council/Raquel-Castaneda-Lopez",
    "/Government/City-Council/Scott-Benson",
    "/Government/Commissions",
    "/Government/Departments-and-Agencies/Detroit-Department-of-Transportation/DDOT-News-and-Alerts",
    "/Government/Departments-and-Agencies/Detroit-Health-Department/Detroit-ID",
    "/Government/Departments-and-Agencies/Detroit-Health-Department/Food-Safety",
    "/Government/Departments-and-Agencies/Detroit-Health-Department/Immunizations",
    "/Government/Departments-and-Agencies/Detroit-Health-Department/Sexually-Transmitted-Diseases",
    "/Government/Departments-and-Agencies/Planning-and-Development-Department",
    "/Government/Departments-and-Agencies/Planning-and-Development-Department/Staff-Info",
    "/Government/Detroit-Police-Commissioners-Meetings",
    "/Government/Mayors-Office",
    "/Government/Mayors-Office/Administration",
    "/How-Do-I/Appeal/Property-Assessment-Forms",
    "/How-Do-I/Apply-for-Licenses/Boiler-License-Information",
    "/How-Do-I/Apply-for-Licenses/Buildings-License-Information",
    "/How-Do-I/Apply-for-Licenses/Business-License-Forms",
    "/How-Do-I/Apply-for-Permits/Building-Inspection-Information",
    "/How-Do-I/Apply-for-Permits/Building-Permit-FAQ",
    "/How-Do-I/Apply-for-Permits/Building-Permit-Information",
    "/How-Do-I/Apply-for-Permits/Gun-Permits-Information",
    "/How-Do-I/Apply-for-Permits/Special-Events-Information",
    "/How-Do-I/Apply-for-Permits/Zoning-Map-Index",
    "/How-Do-I/Construction-Division-Information",
    "/How-Do-I/Do-Business-with-the-City/Building-Authority-Advertisements",
    "/How-Do-I/Do-Business-with-the-City/Planning-Development-RFQs",
    "/How-Do-I/File/Income-Tax-Forms",
    "/How-Do-I/File/Income-Tax-Information",
    "/How-Do-I/Find-Community-Services/Keep-the-Water-On",
    "/How-Do-I/Find-Detroit-Archives/City-Clerks-Archives-and-Records-Information",
    "/How-Do-I/Find-Transportation/Buy-A-Pass",
    "/How-Do-I/Find/Birth-and-Death-Certificates",
    "/How-Do-I/Find/City-Employee-Information",
    "/How-Do-I/Find/Detroit-Animal-Care-and-Control",
    "/How-Do-I/Find/Detroit-Parks-Recreation/Hart-Plaza",
    "/How-Do-I/Find/DPD-Jobs",
    "/How-Do-I/Find/DWSD-Alerts-and-News",
    "/How-Do-I/Find/DWSD-Associations",
    "/How-Do-I/Find/Employee-Forms",
    "/How-Do-I/Find/Hotline-Numbers",
    "/How-Do-I/FInd/Municipal-Parking-FAQ",
    "/How-Do-I/Find/Payment-Plan",
    "/How-Do-I/Find/Police-Precincts",
    "/How-Do-I/Find/properties/Properties-FAQs",
    "/How-Do-I/Find/Recycling-Information",
    "/How-Do-I/Find/Refuse-Collection",
    "/How-Do-I/Find/Schedule-An-Appointment",
    "/How-Do-I/Find/Water-Sewer-and-Drainage-Rates-101",
    "/How-Do-I/Locate-Transportation/Bus-Schedules",
    "/How-Do-I/Locate-Transportation/Bus-Schedules-Information",
    "/How-Do-I/Locate-Transportation/Metro-Lift-Requirements",
    "/How-Do-I/Locate-Transportation/Transporation-Fares",
    "/How-Do-I/Mobile-Apps/ImproveDetroit",
    "/How-Do-I/My-District",
    "/How-Do-I/Neighborhood-Police-Officer-NPO-program",
    "/How-Do-I/Neighborhood-Police-Officer-NPO-program/7TH-PRECINCT-NPO",
    "/How-Do-I/Neighborhood-Police-Officer-NPO-program/8TH-PRECINCT-NPO",
    "/How-Do-I/Neighborhood-Police-Officer-NPO-program/9TH-PRECINCT-NPO",
    "/How-Do-I/Neighborhood-Police-Officer-NPO-program/GAMING-NPO",
    "/How-Do-I/Pay/Blight-Ticket-FAQ",
    "/How-Do-I/Pay/Pay-Parking-Ticket",
    "/How-Do-I/Pay/Police-Records-and-Reports-Information",
    "/How-Do-I/Pay/Water-Bill-Locations",
    "/How-Do-I/Property-Assessment-Documents",
    "/How-Do-I/Register/Register-A-Rental-Property",
    "/How-Do-I/Report/Abandoned-Vehicle",
    "/How-Do-I/Report/Dead-Animal-Removal",
    "/How-Do-I/Request-a-Service/Council-Awards-and-Resolutions",
    "/How-Do-I/Request-a-Service/DPW-Container-Services",
    "/How-Do-I/View-City-of-Detroit-Reports/Legislative-Policy-Division-Reports",
    "/How-Do-I/Volunteer/MotorCity-Makeover-Information",
    "/Mayors-Help-Desk",
    "/MediaServices",
    "/Neighborhoods",
    "/Police",
    "/rental/Schedule-Property-Inspection",
    "/Serve-Detroit",
    "/Calendar-Events",
    "/Detroit-Dashboard",
    "/Government/City-Council/George-Cushingberry",
    "/Government/Departments",
    "/How-Do-I/Appeal",
    "/How-Do-I/Apply-for-Licenses",
    "/How-Do-I/Apply-for-Permits",
    "/How-Do-I/Do-Business-with-the-City",
    "/How-Do-I/File",
    "/How-Do-I/Find",
    "/How-Do-I/Find-Community-Services",
    "/How-Do-I/Find-Detroit-Archives",
    "/How-Do-I/Find/Medical-Marihuana-FAQs",
    "/How-Do-I/Grants",
    "/How-Do-I/Index-A-to-Z/A",
    "/How-Do-I/Index-A-to-Z/P",
    "/How-Do-I/Pay",
    "/How-Do-I/Register",
    "/How-Do-I/Report",
    "/How-Do-I/Request-a-Service",
    "/How-Do-I/View-City-of-Detroit-Reports",
    "/How-Do-I",
    "/2016-Crime-Statistics",
    "/properties",
    "/How-Do-I/Locate-Transportation/Public-Notices",
    "/How-Do-I/Obtain-Grant-Information/Home-Repair-Program-Information",
    "/How-Do-I/Obtain-Grant-Information/Renaissance-Zones",
    "/How-Do-I/Pay/Delinquent-Property-Tax-Information",
    "/How-Do-I/Request-a-Service/Street-Maintenance",
    "/How-Do-I/Request-a-Service/Tree-Services",
    "/How-Do-I/View-Publications-and-Newsletters/Construction-Codes",
    "/youthprograms",
    "/How-Do-I/MobileApps",
    "/Government",
    "/Government/Boards",
    "/How-Do-I/Locate-Transportation",
    "/News",
]

output_errs = True


def report_err(msg):
    if output_errs:
        print(msg)

def in_review(content):

    tmp_content = str(content)

    for word in [ 'TODO', 'REVIEW' ]:
        if word in tmp_content:
            return True

    return False

def do_export(url):

    auth_values = tuple(settings.CREDENTIALS['DETROITMI'].values())

    response = requests.get(url + "?_format=json", auth=HTTPBasicAuth(*auth_values))
    if response.status_code != 200:
        report_err("url {} got status code {}".format(url, response.status_code))
        return;

    json = response.json()

    if in_review(json):
        report_err("url {} is still in REVIEW".format(url))
        return

    print("url: " + url)

    print(json)
    print("")


if __name__ == '__main__':

    os.environ['DJANGO_SETTINGS_MODULE'] = 'django_apps.settings'
    django.setup()

    for url in urls:

        do_export(url = server + url)
