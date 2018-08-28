#!/usr/bin/env python
import os
import sys
import json
from datetime import date
from datetime import datetime
import requests
from requests.auth import HTTPBasicAuth

import django
from django.conf import settings


import pdb


# REVIEW:  remove all medical marijuana links?


server = "http://detroitmi.theneighborhoods.org"


# "/Government/Boards",
# "/Government/Commissions",
# "/How-Do-I/Neighborhood-Police-Officer-NPO-program/7TH-PRECINCT-NPO",
# "/How-Do-I/Neighborhood-Police-Officer-NPO-program/8TH-PRECINCT-NPO",
# "/How-Do-I/Neighborhood-Police-Officer-NPO-program/9TH-PRECINCT-NPO",
# "/How-Do-I/Neighborhood-Police-Officer-NPO-program/GAMING-NPO",
# "/How-Do-I/Do-Business-with-the-City/Planning-Development-RFQs",
# "/Calendar-and-Events",
# "/Calendar-Events",
# "/Government/City-Council/George-Cushingberry",

# "/Detroit-Dashboard",


urls = [
    "/2016-Crime-Statistics",
    "/Boards/BoardOfPoliceCommissioners",
    "/BSEED",
    "/businessincometax",
    "/CampauBanglatown",
    "/Correspondence",
    "/DACC",
    "/DDOT",
    "/Demolition",
    "/Detroit-Demolition-Program/View-All-Demolitions",
    "/Detroit-Opportunities",
    "/Detroit-Opportunities/Find-A-Job",
    "/Detroit-Opportunities/Help-with-your-Home",
    "/Detroit-Opportunities/Programs-for-Youth",
    "/Detroit-Opportunities/Start-or-Grow-Your-Business",
    "/Detroit-Opportunities/Start-or-Grow-Your-Business/Contractor-for-Rehabbed-and-Ready-Program",
    "/doglicense",
    "/Drainage",
    "/dwsd",
    "/DWSDCustomerCare",
    "/DWSDkiosk",
    "/DWSDSkipTheLine",
    "/elections",
    "/employment",
    "/fintreasury",
    "/Government/Boards/Board-of-Electrical-Examiners-Forms",
    "/Government/City-Clerk",
    "/Government/City-Council",
    "/Government/City-Council/Andre-Spivey",
    "/Government/city-council/city-council-district-4/task-forces",
    "/Government/City-Council/Brenda-Jones",
    "/Government/city-council/city-council-president/skilled-trades-task-force",
    "/Government/City-Council/City-Council-Sessions",
    "/Government/City-Council/Gabe-Leland",
    "/Government/City-Council/James-Tate",
    "/Government/city-council/city-council-district-1/task-force",
    "/Government/City-Council/Janee-L-Ayers",
    "/Government/city-council/city-council-large/returning-citizens-task-force",
    "/Government/city-council/city-council-large/letter-residents-detroit",
    "/Government/City-Council/Mary-Sheffield",
    "/government/city-council/city-council-district-5/district-5-neighborhood-police",
    "/government/city-council/city-council-district-5/statements",
    "/Government/City-Council/Raquel-Castaneda-Lopez",
    "/Government/city-council/city-council-district-6/immigation-task-force",
    "/Government/City-Council/Scott-Benson",
    "/Government/Departments",
    "/Government/Departments-and-Agencies/Detroit-Department-of-Transportation/DDOT-News-and-Alerts",
    "/Government/Departments-and-Agencies/Detroit-Health-Department/Detroit-ID",
    "/Government/Departments-and-Agencies/Detroit-Health-Department/Food-Safety",
    "/Government/Departments-and-Agencies/Detroit-Health-Department/Immunizations",
    "/Government/Departments-and-Agencies/Detroit-Health-Department/Sexually-Transmitted-Diseases",
    "/Government/Departments-and-Agencies/Law-Department",
    "/Government/Departments-and-Agencies/Office-of-the-Chief-Financial-Office/Office-of-the-Assessor",
    "/Government/Departments-and-Agencies/Planning-and-Development-Department",
    "/Government/Departments-and-Agencies/Planning-and-Development-Department/Staff-Info",
    "/Government/Departments-and-Agencies/Public-Works/Contact-us",
    "/Government/Departments-and-Agencies/Public-Works/Curbside-Bulk-Waste-Pickup",
    "/Government/Departments-and-Agencies/Public-Works/Recycle",
    "/Government/Departments-and-Agencies/Water-and-Sewerage-Department/About-DWSD",
    "/Government/Departments-and-Agencies/Water-and-Sewerage-Department/Learn-About-Your-Water-and-Sewer-Bill",
    "/Government/Detroit-Police-Commissioners-Meetings",
    "/Government/Mayors-Office",
    "/Government/Mayors-Office/Administration",
    "/health",
    "/How-Do-I",
    "/How-Do-I/Appeal",
    "/How-Do-I/Appeal/Property-Assessment-Forms",
    "/How-Do-I/Apply-for-Licenses",
    "/How-Do-I/Apply-for-Licenses/Boiler-License-Information",
    "/How-Do-I/Apply-for-Licenses/Buildings-License-Information",
    "/How-Do-I/Apply-for-Licenses/Business-License-Checklist",
    "/How-Do-I/Apply-for-Licenses/Business-License-Forms",
    "/How-Do-I/Apply-for-Permits",
    "/How-Do-I/Apply-for-Permits/Building-Inspection-Information",
    "/How-Do-I/Apply-for-Permits/Building-Permit-FAQ",
    "/How-Do-I/Apply-for-Permits/Building-Permit-Information",
    "/How-Do-I/Apply-for-Permits/Gun-Permits-Information",
    "/How-Do-I/Apply-for-Permits/Special-Events-Information",
    "/How-Do-I/Apply-for-Permits/Zoning-Map-Index",
    "/How-Do-I/Apply-for-Permits/Zoning-Permit-Forms",
    "/How-Do-I/Apply-for-Permits/Zoning-Permit-Information",
    "/How-Do-I/Construction-Division-Information",
    "/How-Do-I/Do-Business-with-the-City",
    "/How-Do-I/Do-Business-with-the-City/Building-Authority-Advertisements",
    "/How-Do-I/Do-Business-with-the-City/Open-Bids-for-the-City-of-Detroit",
    "/How-Do-I/File",
    "/How-Do-I/File/Blight-Complaint",
    "/How-Do-I/File/Income-Tax-Forms",
    "/How-Do-I/File/Income-Tax-Information",
    "/How-Do-I/Find",
    "/How-Do-I/Find-Community-Services",
    "/How-Do-I/Find-Community-Services/Arson-Awareness",
    "/How-Do-I/Find-Community-Services/Keep-the-Water-On",
    "/How-Do-I/Find-Detroit-Archives",
    "/How-Do-I/Find-Detroit-Archives/City-Clerks-Archives-and-Records-Information",
    "/How-Do-I/Find-Transportation/Buy-A-Pass",
    "/How-Do-I/Find/Adams-Butzel-Complex",
    "/How-Do-I/Find/Birth-and-Death-Certificates",
    "/How-Do-I/Find/City-Employee-Information",
    "/How-Do-I/Find/Detroit-Animal-Care-and-Control",
    "/How-Do-I/Find/Detroit-Parks-Recreation/Hart-Plaza",
    "/How-Do-I/Find/Detroit-Parks-Recreation/Parks-Recreation-Forms",
    "/How-Do-I/Find/DPD-Jobs",
    "/How-Do-I/Find/DWSD-Alerts-and-News",
    "/How-Do-I/Find/DWSD-Associations",
    "/How-Do-I/Find/Employee-Forms",
    "/How-Do-I/Find/Hotline-Numbers",
    "/How-Do-I/Find/Medical-Marihuana-FAQs",
    "/How-Do-I/FInd/Municipal-Parking-FAQ",
    "/How-Do-I/Find/Payment-Plan",
    "/How-Do-I/Find/Police-Precincts",
    "/How-Do-I/Find/properties/Properties-FAQs",
    "/How-Do-I/Find/Recycling-Information",
    "/How-Do-I/Find/Refuse-Collection",
    "/How-Do-I/Find/Schedule-An-Appointment",
    "/How-Do-I/Find/Water-Sewer-and-Drainage-Rates-101",
    "/How-Do-I/Grants",
    "/How-Do-I/Locate-Transportation",
    "/How-Do-I/Locate-Transportation/Bus-Schedules",
    "/How-Do-I/Locate-Transportation/Bus-Schedules-Information",
    "/How-Do-I/Locate-Transportation/Metro-Lift-Requirements",
    "/How-Do-I/Locate-Transportation/Transportation-Fares",
    "/How-Do-I/Medical-Marihuana-Information",
    "/ImproveDetroit",
    "/How-Do-I/MobileApps",
    "/How-Do-I/My-District",
    "/How-Do-I/Neighborhood-Police-Officer-NPO-program",
    "/How-Do-I/Obtain-Grant-Information/Home-Repair-Program-Information",
    "/How-Do-I/Obtain-Grant-Information/Renaissance-Zones",
    "/How-Do-I/Pay",
    "/How-Do-I/Pay/Blight-Ticket-FAQ",
    "/How-Do-I/Pay/Delinquent-Property-Tax-Information",
    "/How-Do-I/Pay/Pay-Parking-Ticket",
    "/How-Do-I/Pay/Police-Records-and-Reports-Information",
    "/How-Do-I/Pay/Property-Taxes-FAQs",
    "/How-Do-I/Pay/Property-Taxes-Information",
    "/How-Do-I/Pay/Water-Bill-Locations",
    "/How-Do-I/Property-Assessment-Documents",
    "/How-Do-I/Register",
    "/How-Do-I/Register/Register-A-Rental-Property",
    "/How-Do-I/Report",
    "/How-Do-I/Report/Abandoned-Vehicle",
    "/How-Do-I/Report/Crime",
    "/How-Do-I/Report/Dead-Animal-Removal",
    "/How-Do-I/Request-a-Service",
    "/How-Do-I/Request-a-Service/Council-Awards-and-Resolutions",
    "/How-Do-I/Request-a-Service/DPW-Container-Services",
    "/How-Do-I/Request-a-Service/Street-Maintenance",
    "/How-Do-I/Request-a-Service/Tree-Services",
    "/How-Do-I/View-City-of-Detroit-Reports",
    "/How-Do-I/View-City-of-Detroit-Reports/Legislative-Policy-Division-Reports",
    "/How-Do-I/View-Publications-and-Newsletters/Construction-Codes",
    "/How-Do-I/Volunteer/MotorCity-Makeover-Information",
    "/IncomeTax",
    "/Mayors-Help-Desk",
    "/MediaServices",
    "/MedicalMarihuana",
    "/Neighborhoods",
    "/News",
    "/parking",
    "/Police",
    "/projectcleanslate",
    "/properties",
    "/PublicWorks",
    "/Purchasing",
    "/recreation",
    "/rental",
    "/rental/property-registration",
    "/rental/Schedule-Property-Inspection",
    "/Serve-Detroit",
    "/Supplier",
    "/youthprograms",
    "/government/city-clerk",
    "/government/city-clerk/appear-council",
    "/government/city-clerk/banner-permits-information",
    "/government/city-clerk/city-clerk-archive-records-fees",
    "/government/city-clerk/city-clerks-archives-and-records-information",
    "/government/city-clerk/city-council-proceedings-2000-2014-information",
    "/government/city-clerk/city-of-detroit-charter-information",
    "/government/city-clerk/lobbyist-registration-and-reporting-information",
    "/government/city-clerk/elections/become-election-day-pollworker",
    "/government/city-clerk/elections/election-information",
    "/government/city-clerk/elections/election-results",
    "/government/city-clerk/elections/m-100-automark-voting-system",
    "/government/city-clerk/elections/request-absentee-ballot",
]

# # city council urls
# city_council_urls = [
#     "/Government/City-Council",
#     "/government/city-council/city-council-president",
#     "/Government/city-council/city-council-president/skilled-trades-task-force",
#     "/government/city-council/city-council-large",
#     "/government/city-council/city-council-large/returning-citizens-task-force",
#     "/Government/city-council/city-council-large/letter-residents-detroit",
#     "/government/city-council/city-council-district-1",
#     "/government/city-council/city-council-district-1/task-force",
#     "/government/city-council/city-council-district-2",
#     "/government/city-council/city-council-district-2/mental-health-task-force",
#     "/government/city-council/city-council-district-3",
#     "/government/city-council/city-council-district-3/green-task-force",
#     "/government/city-council/city-council-district-4",
#     "/government/city-council/city-council-district-4/task-forces",
#     "/government/city-council/city-council-district-5",
#     "/government/city-council/city-council-district-5/district-5-neighborhood-police",
#     "/government/city-council/city-council-district-5/statements",
#     "/government/city-council/city-council-district-6",
#     "/government/city-council/city-council-district-6/immigation-task-force",
#     "/government/city-council/city-council-district-7",
#     "/government/city-council/city-council-standing-committees-information",
#     "/government/city-council/council-awards-and-resolutions",
#     "/government/city-council/legislative-policy-division",
#     "/government/city-council/legislative-policy-division/fiscal-analysis-reports",
# ]

ddot_urls = [
    "/departments/detroit-department-transportation",
    "/departments/detroit-department-transportation/bus-schedules",
    "/departments/detroit-department-transportation/buy-pass",
    "/departments/detroit-department-transportation/metrolift-ada-paratransit-services",
    "/departments/detroit-department-transportation/transportation-fares",
]

# urls = ddot_urls


dfd_urls = [
    "/departments/detroit-fire-department/arson-awareness",
]

# urls = dfd_urls


dpd_urls = [
    "/departments/police-department",
    "/departments/police-department/2016-crime-statistics",
    "/departments/police-department/abandoned-vehicle",
    "/departments/police-department/detroit-police-department-jobs",
    "/departments/police-department/detroit-police-department-records-and-reports",
    "/departments/police-department/gun-permits-information",
    "/departments/police-department/precincts-and-neighborhood-police-officers",
    "/departments/police-department/report-crime",
]

# urls = dpd_urls


bseed_urls = [
    "/departments/buildings-safety-engineering-and-environmental-department",
    "/departments/buildings-safety-engineering-and-environmental-department/building-permit-information",
    "/departments/buildings-safety-engineering-and-environmental-department/business-license-center",
    "/departments/buildings-safety-engineering-and-environmental-department/business-licenses-checklist",
    "/departments/buildings-safety-engineering-and-environmental-department/construction",
    "/departments/buildings-safety-engineering-and-environmental-department/construction/boiler",
    "/departments/buildings-safety-engineering-and-environmental-department/construction/building",
    "/departments/buildings-safety-engineering-and-environmental-department/construction/building-codes",
    "/departments/buildings-safety-engineering-and-environmental-department/medical-marijuana",
    "/departments/buildings-safety-engineering-and-environmental-department/property-maintenance-division",
    "/departments/buildings-safety-engineering-and-environmental-department/property-maintenance-division/certificate-compliance",
    "/departments/buildings-safety-engineering-and-environmental-department/property-maintenance-division/certificate-compliance/quick-steps-obtain-certificate",
    "/departments/buildings-safety-engineering-and-environmental-department/zoning",
]

# urls = bseed_urls


pdd_urls = [
    "/departments/planning-and-development-department",
    "/departments/planning-and-development-department/citywide-initiatives/home-repair-program-information",
    "/departments/planning-and-development-department/east-design-region/campau-banglatown",
]

# urls = pdd_urls


dah_urls = [
    "/departments/department-appeals-and-hearings/blight-ticket-information",
]

# urls = dah_urls

city_clerk_urls = [
    "/government/city-clerk",
    "/government/city-clerk/appear-council",
    "/government/city-clerk/banner-permits-information",
    "/government/city-clerk/city-clerk-archive-records-fees",
    "/government/city-clerk/city-council-proceedings-2000-2014-information",
    "/government/city-clerk/city-detroit-charter-information",
    "/government/city-clerk/elections",
    "/government/city-clerk/elections/become-election-day-pollworker",
    "/government/city-clerk/elections/election-information",
    "/government/city-clerk/elections/election-results",
    "/government/city-clerk/elections/m-100-automark-voting-system",
    "/government/city-clerk/elections/request-absentee-ballot",
    "/government/city-clerk/lobbyist-registration-and-reporting-information",
]

# urls = city_clerk_urls


mayors_office_urls = [
    "/government/mayors-office",
    "/government/mayors-office/mayor",
    "/government/mayors-office/police-chief",
    "/government/mayors-office/chief-staff",
    "/government/mayors-office/corporation-counsel",
    "/government/mayors-office/chief-financial-officer",
    "/government/mayors-office/chief-information-officer",
    "/government/mayors-office/correspondence",
    "/government/mayors-office/group-executive-operations",
    "/government/mayors-office/detroit-neighborhood-initiative",
    "/government/mayors-office/detroit-opportunities",
    "/government/mayors-office/detroit-opportunities/detroit-experiences",
    "/government/mayors-office/detroit-opportunities/find-job",
    "/government/mayors-office/water-and-sewerage-director",
    "/government/mayors-office/group-executive-jobs-and-economic-growth",
    "/government/mayors-office/group-executive-neighborhoods",
    "/government/mayors-office/transportation-director",
    "/government/mayors-office/goal-detroit",
    "/government/mayors-office/human-resources-director",
    "/government/mayors-office/chief-learning-officer",
    "/government/mayors-office/director-and-health-officer",
    "/government/mayors-office/lean-training",
    "/government/mayors-office/mayors-help-desk",
    "/government/mayors-office/office-immigrant-affairs",
    "/government/mayors-office/office-immigrant-affairs/community-resources",
    "/government/mayors-office/office-immigrant-affairs/economic-empowerment",
    "/government/mayors-office/office-immigrant-affairs/education-esl-services",
    "/government/mayors-office/office-immigrant-affairs/employment-resources",
    "/government/mayors-office/office-immigrant-affairs/health-care",
    "/government/mayors-office/office-immigrant-affairs/housing",
    "/government/mayors-office/office-immigrant-affairs/legal-help",
    "/government/mayors-office/office-immigrant-affairs/mayors-welcoming-letter",
    "/government/mayors-office/office-immigrant-affairs/social-services",
    "/government/mayors-office/office-immigrant-affairs/start-business",
    "/government/mayors-office/office-immigrant-affairs/transportation",
    "/government/mayors-office/office-immigrant-affairs/think-detroit",
    "/government/mayors-office/office-sustainability",
    "/government/mayors-office/office-sustainability/current-focus-areas",
    "/government/mayors-office/office-sustainability/mission-and-vision",
    "/government/mayors-office/office-sustainability/sustainability-action-agenda",
    "/government/mayors-office/properties",
    "/government/mayors-office/real-estate-development",
    "/government/mayors-office/real-estate-development/development-financing",
    "/government/mayors-office/real-estate-development/development-how",
    "/government/mayors-office/real-estate-development/development-success-stories",
    "/government/mayors-office/real-estate-development/why-detroit",
    "/government/mayors-office/tax-preparation-checklist",
]

# urls = mayors_office_urls


dwsd_urls = [
    "/departments/water-and-sewerage-department",
    "/departments/water-and-sewerage-department/customer-care",
    "/departments/water-and-sewerage-department/customer-care/how-am-i-charged",
    "/departments/water-and-sewerage-department/customer-care/learn-about-your-water-and-sewer-bill",
    "/departments/water-and-sewerage-department/customer-care/where-do-i-pay",
    "/departments/water-and-sewerage-department/drainage-charge",
    "/departments/water-and-sewerage-department/resources/about-dwsd",
    "/departments/water-and-sewerage-department/resources/dwsd-associations",
    "/departments/water-and-sewerage-department/resources/payment-kiosks",
    "/departments/water-and-sewerage-department/resources/payment-plan",
]

# urls = dwsd_urls


media_services_urls = [
    "/departments/media-services-department",
    "/departments/media-services-department/special-events",
]

# urls = media_services_urls


ocfo_urls = [
    "/departments/office-chief-financial-officer/ocfo-divisions/office-assessor",
    "/departments/office-chief-financial-officer/ocfo-divisions/office-assessor/property-tax-assistance",
    "/departments/office-chief-financial-officer/ocfo-divisions/office-assessor/renaissance-zones",
    "/departments/office-chief-financial-officer/ocfo-divisions/office-contracting-and-procurement",
    "/departments/office-chief-financial-officer/ocfo-divisions/office-contracting-and-procurement/open-bids-city-detroit",
    "/departments/office-chief-financial-officer/ocfo-divisions/office-contracting-and-procurement/supplier-portal-information-and-instructions",
    "/departments/office-chief-financial-officer/ocfo-divisions/office-treasury/delinquent-property-tax-information",
    "/departments/office-chief-financial-officer/ocfo-divisions/office-treasury/income-tax",
    "/departments/office-chief-financial-officer/ocfo-divisions/office-treasury/income-tax/business-income-tax",
    "/departments/office-chief-financial-officer/ocfo-divisions/office-treasury/pay-property-tax",
]

# urls = ocfo_urls


don_urls = [
    "/departments/department-neighborhoods",
    "/departments/department-neighborhoods/motorcity-makeover-information",
    "/departments/department-neighborhoods/serve-detroit",
]

# urls = don_urls


dpw_urls = [
    "/departments/department-public-works",
    "/departments/department-public-works/contact-us",
    "/departments/department-public-works/dead-animal-removal",
    "/departments/department-public-works/refuse-collection",
    "/departments/department-public-works/refuse-collection/bulk-yard-waste/curbside-bulk-waste-pickup",
    "/departments/department-public-works/refuse-collection/recycle",
    "/departments/department-public-works/street-maintenance",
]

# urls = dpw_urls


health_urls = [
    "/departments/health-department",
    "/departments/health-department/birth-and-death-certificates",
    "/departments/health-department/detroit-animal-care-and-control",
    "/departments/health-department/detroit-id",
    "/departments/health-department/detroit-id/schedule-appointment",
    "/departments/health-department/food-safety",
    "/departments/health-department/immunizations",
    "/departments/health-department/sexually-transmitted-diseases-clinic",
]

# urls = health_urls


hrd_urls = [
    "/departments/human-resources-department/apply-job",
    "/departments/human-resources-department/city-employee-information",
    "/departments/human-resources-department/employee-forms",
]

# urls = hrd_urls


board_urls = [
    "/government/boards/board-electrical-examiners",
    "/government/boards/board-police-commissioners",
]

urls = board_urls


faq_urls = [
    "/node/1231",
    "/node/1521",
    "/node/1581",
    "/node/2471",
    "/node/2481",
    "/node/2501",
    "/node/2586",
    "/node/3361",
    "/node/3866",
    "/node/3886",
    "/node/4576",
    "/node/501",
    "/node/6476",
    "/node/9466",
    "/node/9871",
]

# urls = faq_urls


already_exported = [
    "http://detroitmi.theneighborhoods.org/government/boards/board-of-police-commissioners",
    "http://detroitmi.theneighborhoods.org/departments/buildings-safety-engineering-and-environmental-department",
    "http://detroitmi.theneighborhoods.org/departments/planning-and-development-department/east-design-region/campau-banglatown",
    "http://detroitmi.theneighborhoods.org/government/mayors-office/correspondence",
    "http://detroitmi.theneighborhoods.org/departments/health-department/detroit-animal-care-and-control",
    "http://detroitmi.theneighborhoods.org/departments/detroit-department-of-transportation",
    "http://detroitmi.theneighborhoods.org/departments/detroit-building-authority/detroit-demolition-program/view-all-demolitions",
    "http://detroitmi.theneighborhoods.org/government/mayors-office/detroit-opportunities/find-job",
    "http://detroitmi.theneighborhoods.org/departments/detroit-water-and-sewerage-department/stormwater-drainage/what-drainage",
    "http://detroitmi.theneighborhoods.org/departments/detroit-water-and-sewerage-department",
    "http://detroitmi.theneighborhoods.org/departments/detroit-water-and-sewerage-department/dwsd-customer-care",
    "http://detroitmi.theneighborhoods.org/departments/detroit-water-and-sewerage-department/dwsd-customer-care/payment-kiosks",
    "http://detroitmi.theneighborhoods.org/departments/detroit-water-and-sewerage-department/dwsd-customer-care/skip-the-line",
    "http://detroitmi.theneighborhoods.org/government/city-clerk/elections",
    "http://detroitmi.theneighborhoods.org/departments/human-resources-department/apply-for-job",
    "http://detroitmi.theneighborhoods.org/departments/office-of-the-chief-financial-officer/office-of-treasury/pay-property-tax",
    "http://detroitmi.theneighborhoods.org/government/boards/board-of-electrical-examiners",
    "http://detroitmi.theneighborhoods.org/government/city-clerk",
    "http://detroitmi.theneighborhoods.org/government/city-council",
    "http://detroitmi.theneighborhoods.org/departments/health-department/detroit-id",
    "http://detroitmi.theneighborhoods.org/departments/health-department/food-safety",
    "http://detroitmi.theneighborhoods.org/departments/health-department/immunizations",
    "http://detroitmi.theneighborhoods.org/departments/law-department",
    "http://detroitmi.theneighborhoods.org/departments/planning-and-development-department",
    "http://detroitmi.theneighborhoods.org/departments/department-of-public-works/contact-us",
    "http://detroitmi.theneighborhoods.org/departments/department-of-public-works/refuse-collection/bulk-yard-waste/curbside-bulk-waste-pickup",
    "http://detroitmi.theneighborhoods.org/departments/department-of-public-works/refuse-collection/recycle",
    "http://detroitmi.theneighborhoods.org/departments/detroit-water-and-sewerage-department/about-dwsd",
    "http://detroitmi.theneighborhoods.org/departments/detroit-water-and-sewerage-department/dwsd-customer-care/learn-about-your-bill",
    "http://detroitmi.theneighborhoods.org/government/mayors-office",
    "http://detroitmi.theneighborhoods.org/departments/health-department",
    "http://detroitmi.theneighborhoods.org/how-do-i/appeal",
    "http://detroitmi.theneighborhoods.org/government/property-assessment-forms",
    "http://detroitmi.theneighborhoods.org/departments/buildings-safety-engineering-and-environmental-department/construction/boiler-inspection-team",
    "http://detroitmi.theneighborhoods.org/departments/buildings-safety-engineering-and-environmental-department/business-license-center",
    "http://detroitmi.theneighborhoods.org/departments/buildings-safety-engineering-and-environmental-department/business-licenses-checklist",
    "http://detroitmi.theneighborhoods.org/departments/buildings-safety-engineering-and-environmental-department/construction/building-inspection-information",
    "http://detroitmi.theneighborhoods.org/departments/buildings-safety-engineering-and-environmental-department/building-permit-information/building-permit-requirements",
    "http://detroitmi.theneighborhoods.org/departments/detroit-police-department/gun-permits-information",
    "http://detroitmi.theneighborhoods.org/departments/media-services-department/special-events",
    "http://detroitmi.theneighborhoods.org/departments/buildings-safety-engineering-and-environmental-department/zoning",
    "http://detroitmi.theneighborhoods.org/departments/buildings-safety-engineering-and-environmental-department/construction",
    "http://detroitmi.theneighborhoods.org/how-do-i/do-business-with-the-city",
    "http://detroitmi.theneighborhoods.org/departments/detroit-building-authority",
    "http://detroitmi.theneighborhoods.org/departments/office-of-the-chief-financial-officer/office-of-contracting-and-procurement/open-bids-for-the-city-of-detroit",
    "http://detroitmi.theneighborhoods.org/departments/office-of-the-chief-financial-officer/office-of-treasury/income-tax",
    "http://detroitmi.theneighborhoods.org/departments/detroit-fire-department/arson-awareness",
    "http://detroitmi.theneighborhoods.org/government/city-clerk/city-clerks-archives-and-records-information",
    "http://detroitmi.theneighborhoods.org/departments/detroit-department-of-transportation/buy-pass",
    "http://detroitmi.theneighborhoods.org/departments/detroit-parks-recreation/community-recreation-centers/butzel-family-center",
    "http://detroitmi.theneighborhoods.org/departments/health-department/birth-and-death-certificates",
    "http://detroitmi.theneighborhoods.org/departments/detroit-parks-recreation",
    "http://detroitmi.theneighborhoods.org/departments/detroit-police-department/detroit-police-department-jobs",
    "http://detroitmi.theneighborhoods.org/departments/detroit-water-and-sewerage-department/dwsd-customer-care/payment-plan",
    "http://detroitmi.theneighborhoods.org/how-do-i/find-information/properties-faq",
    "http://detroitmi.theneighborhoods.org/departments/department-of-public-works/refuse-collection",
    "http://detroitmi.theneighborhoods.org/departments/health-department/detroit-id/schedule-appointment",
    "http://detroitmi.theneighborhoods.org/departments/detroit-water-and-sewerage-department/water-sewer-and-drainage-rates-101",
    "http://detroitmi.theneighborhoods.org/departments/detroit-department-of-transportation/bus-schedules",
    "http://detroitmi.theneighborhoods.org/departments/detroit-department-of-transportation/metro-lift-requirements",
    "http://detroitmi.theneighborhoods.org/departments/detroit-department-of-transportation/transportation-fares",
    "http://detroitmi.theneighborhoods.org/ImproveDetroit",
    "http://detroitmi.theneighborhoods.org/departments/detroit-police-department/precincts-and-neighborhood-police-officers",
    "http://detroitmi.theneighborhoods.org/departments/planning-and-development-department/citywide-initiatives/home-repair-program-information",
    "http://detroitmi.theneighborhoods.org/departments/office-of-the-chief-financial-officer/office-of-treasury/delinquent-property-tax-information",
    "http://detroitmi.theneighborhoods.org/departments/municipal-parking-department/pay-parking-ticket",
    "http://detroitmi.theneighborhoods.org/departments/detroit-police-department/detroit-police-department-records-and-reports",
    "http://detroitmi.theneighborhoods.org/node/1581",
    "http://detroitmi.theneighborhoods.org/how-do-i/register",
    "http://detroitmi.theneighborhoods.org/departments/detroit-police-department/abandoned-vehicle",
    "http://detroitmi.theneighborhoods.org/departments/detroit-police-department/report-crime",
    "http://detroitmi.theneighborhoods.org/departments/department-of-public-works/dead-animal-removal",
    "http://detroitmi.theneighborhoods.org/government/city-council/council-awards-and-resolutions",
    "http://detroitmi.theneighborhoods.org/departments/department-of-public-works/refuse-collection/dpw-container-services",
    "http://detroitmi.theneighborhoods.org/departments/department-of-public-works/street-maintenance",
    "http://detroitmi.theneighborhoods.org/departments/general-services-department/tree-services",
    "http://detroitmi.theneighborhoods.org/government/city-council/legislative-policy-division/legislative-policy-division-reports",
    "http://detroitmi.theneighborhoods.org/departments/department-of-neighborhoods/motorcity-makeover-information",
    "http://detroitmi.theneighborhoods.org/government/mayors-office/mayors-help-desk",
    "http://detroitmi.theneighborhoods.org/departments/media-services-department",
    "http://detroitmi.theneighborhoods.org/departments/department-of-neighborhoods",
    "http://detroitmi.theneighborhoods.org/departments/detroit-police-department",
    "http://detroitmi.theneighborhoods.org/departments/law-department/project-clean-slate",
    "http://detroitmi.theneighborhoods.org/government/mayors-office/properties",
    "http://detroitmi.theneighborhoods.org/departments/department-of-public-works",
    "http://detroitmi.theneighborhoods.org/departments/office-of-the-chief-financial-officer/office-of-contracting-and-procurement",
    "http://detroitmi.theneighborhoods.org/departments/buildings-safety-engineering-and-environmental-department/property-maintenance-division",
    "http://detroitmi.theneighborhoods.org/departments/buildings-safety-engineering-and-environmental-department/property-maintenance-division/certificate-of-compliance/quick-steps-obtain-certificate-of-compliance",
    "http://detroitmi.theneighborhoods.org/departments/office-of-the-chief-financial-officer/office-of-contracting-and-procurement/supplier-portal-information-and-instructions",
    "http://detroitmi.theneighborhoods.org/node/4576",
    "http://detroitmi.theneighborhoods.org/node/1231",
    "http://detroitmi.theneighborhoods.org/node/2586",
    "http://detroitmi.theneighborhoods.org/node/6476",
    "http://detroitmi.theneighborhoods.org/node/3361",
    "http://detroitmi.theneighborhoods.org/node/3886",
    "http://detroitmi.theneighborhoods.org/node/2471",
    "http://detroitmi.theneighborhoods.org/node/1521",
    "http://detroitmi.theneighborhoods.org/node/3866",
    "http://detroitmi.theneighborhoods.org/node/2481",
    "http://detroitmi.theneighborhoods.org/node/2501",
]


class ContentExporter():

    output_errs = False
    error_cnt = {}
    urls_exported = {}

    @staticmethod
    def report_err(msg, desc):
        if ContentExporter.output_errs:
            print("ERROR:  " + msg)
        cnt = ContentExporter.error_cnt.get(desc, 1)
        ContentExporter.error_cnt[desc] = cnt + 1

    @staticmethod
    def report_err_cnt():
        if ContentExporter.output_errs:
            print('\n**************************************************************************************\n')
            print('errors:  ' + str(ContentExporter.error_cnt))
            print('num successful exports: ' + str(len(ContentExporter.urls_exported)))

    @staticmethod
    def in_review(content):

        for key in [ 'field_need_review', 'field_need_reviewed' ]:
            if content.get(key) and content[key][0]['value']:
                # pdb.set_trace()
                return True

        tmp_content = str(content)
        for word in [ 'TODO', 'REVIEW' ]:
            if word in tmp_content:
                # pdb.set_trace()
                return True

        return False

    @staticmethod
    def needs_translation(content):

        if not content:
            pdb.set_trace()
            return True

        changed = content.get('changed')
        if not changed:
            pdb.set_trace()
            return True

        tmp = changed[0]['value']
        date_changed = datetime.strptime(tmp[0 : 10], '%Y-%m-%d').date()

        for key in [ "field_dept_translation_date", "field_gov_translation_date" ]:

            if content.get(key):

                tmp = content[key][0]['value']
                translation_date = datetime.strptime(tmp, '%Y-%m-%d').date()
                if translation_date < date_changed:
                    return True
                else:

                    # pdb.set_trace()

                    return False

        return True

    @staticmethod
    def get_div(content, content_id, start=0):

        # Try to find the identifier
        id_pos = content.find(content_id, start)
        if id_pos == -1:
            return [None, None]

        # Now try to find the beginning of the div containing it
        begin = content.rfind("<div", 0, id_pos)
        if begin == -1:
            pdb.set_trace()
            return [None, None]

        # Find end of <div tag
        content_begin = content.find(">", begin + 4)
        if content_begin == -1:
            pdb.set_trace()
            return [None, None]

        # Finally, try to find closing </div>
        end = content.find("</div>", content_begin + 1)
        if end == -1:
            pdb.set_trace()
            return [None, None]

        sub_string = content[content_begin + 1 : end]
        return [ sub_string, end ]

    @staticmethod
    def export_faq_pair(faq_pair):

        target_id = faq_pair['target_id']

        url = "{}/rest/translation/paragraph/{}".format(server, target_id)

        response = requests.get(url + "?_format=json")
        if response.status_code != 200:
            ContentExporter.report_err("url {} got status code {}".format(url, response.status_code), response.status_code)
            return;

        json = response.json()
        content = json[0]['bp_accordion_section']

        faq_pairs = []
        start = 0

        while True:

            question, start = ContentExporter.get_div(content=content, content_id="field--name-bp-accordion-section-title", start=start)
            answer, start = ContentExporter.get_div(content=content, content_id="field--name-bp-text", start=start)

            if not question or not answer:
                return faq_pairs

            faq_pairs.append( { "question": question, "answer": answer } )

    @staticmethod
    def handle_howdoi(url, data):

        if "how-do-i" not in url.lower():
            return None

        for key in ['field_department']:

            related = data.get(key)
            if related:
                tmp_url = related[0].get('url', '')
                if tmp_url:
                    return tmp_url

        # we did not find good related content, so don't try to retrieve any
        return None

    @staticmethod
    def handle_faq(data):

        field_faq_refer = data.get('field_faq_refer')
        if field_faq_refer:
            url = field_faq_refer[0].get('url')
            if url:
                urls.append(url)

    @staticmethod
    def cleanup_url(url):

        pos = url.find('?')
        if pos > 0:
            url = url[0 : pos]
        return url

    @staticmethod
    def get_response_url(url, response):

        tmp = response.url
        if "/node/" not in tmp:
            url = tmp
        return url

    @staticmethod
    def get_data(url):

        auth_values = tuple(settings.CREDENTIALS['DETROITMI'].values())

        url = "{}{}".format(server, url)

        response = requests.get(url + "?_format=json", auth=HTTPBasicAuth(*auth_values))
        if response.status_code != 200:
            ContentExporter.report_err("url {} got status code {}".format(url, response.status_code), response.status_code)
            return [None, None];

        url = response.url

        # Have we already exported this content?
        tmp_url = ContentExporter.cleanup_url(response.url)
        if ContentExporter.urls_exported.get(tmp_url):
            ContentExporter.report_err("url {} has already been exported".format(tmp_url), "Duplicate URL")
            return [None, None];

        data = response.json()
        tmp_url = ContentExporter.handle_howdoi(url, data)
        ContentExporter.handle_faq(data)
        if tmp_url:
            return ContentExporter.get_data(url=tmp_url)
        else:
            return url, data

    @staticmethod
    def do_export(url):

        url, data = ContentExporter.get_data(url=url)
        if not url:
            return

        if not ContentExporter.needs_translation(data):
            ContentExporter.report_err("url {} does not need translation".format(url), "No translation needed")
            return

        if ContentExporter.in_review(data):
            ContentExporter.report_err("url {} is still in REVIEW".format(url), "REVIEW status")
            return

        # Handle any faq pairs
        for idx, faq_pair in enumerate(data.get('field_faq_pair', [])):

            if faq_pair['target_type'] == 'paragraph':

                parsed_faq_pairs = ContentExporter.export_faq_pair(faq_pair=faq_pair)
                data['field_faq_pair'][idx]['content'] = parsed_faq_pairs

            else:
                pdb.set_trace()

        url = ContentExporter.cleanup_url(url)
        print("url: " + url)

        has_some_required = False
        required_keys = set(data.keys()).intersection(["description", "summary", "field_faq_pair"])
        for key in required_keys:

            if data.get(key):
                has_some_required = True

        if not has_some_required:
            ContentExporter.report_err("url {} was missing required data".format(url), "Missing required data")
            return 

        print(json.dumps(data))
        ContentExporter.urls_exported[url] = True
        print("")

        if ContentExporter.output_errs:
            return


        # also print the json to an individual file for each url
        url_encoded = url[37 : ].replace("/", "%2F")
        url_encoded = ContentExporter.cleanup_url(url_encoded)

        with open(url_encoded + ".txt", 'w') as output:

            output.write(ContentExporter.cleanup_url(url) + "\n\n")
            output.write(json.dumps(data))


if __name__ == '__main__':

    if len(sys.argv) == 2:
        ContentExporter.output_errs = sys.argv[1] == '--debug=true'

    os.environ['DJANGO_SETTINGS_MODULE'] = 'django_apps.settings'
    django.setup()

    # for url in already_exported:

    #     ContentExporter.urls_exported[url] = True

    for url in urls:

        ContentExporter.do_export(url=url)

    ContentExporter.report_err_cnt()
