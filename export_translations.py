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
# "/Calendar-and-Events",
# "/Calendar-Events",
# "/Government/City-Council/George-Cushingberry",


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
    "/Detroit-Dashboard",
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
    "/Government/City-Council/Brenda-Jones",
    "/Government/City-Council/City-Council-Sessions",
    "/Government/City-Council/Gabe-Leland",
    "/Government/City-Council/James-Tate",
    "/Government/City-Council/Janee-L-Ayers",
    "/Government/City-Council/Mary-Sheffield",
    "/Government/City-Council/Raquel-Castaneda-Lopez",
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
    "/How-Do-I/Do-Business-with-the-City/Planning-Development-RFQs",
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
    "/How-Do-I/Index-A-to-Z/A",
    "/How-Do-I/Index-A-to-Z/P",
    "/How-Do-I/Locate-Transportation",
    "/How-Do-I/Locate-Transportation/Bus-Schedules",
    "/How-Do-I/Locate-Transportation/Bus-Schedules-Information",
    "/How-Do-I/Locate-Transportation/Metro-Lift-Requirements",
    "/How-Do-I/Locate-Transportation/Public-Notices",
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
                return True

        tmp_content = str(content)
        for word in [ 'TODO', 'REVIEW' ]:
            if word in tmp_content:
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
    def get_data(url):

        auth_values = tuple(settings.CREDENTIALS['DETROITMI'].values())

        url = "{}{}".format(server, url)

        response = requests.get(url + "?_format=json", auth=HTTPBasicAuth(*auth_values))
        if response.status_code != 200:
            ContentExporter.report_err("url {} got status code {}".format(url, response.status_code), response.status_code)
            return [None, None];

        url = response.url

        # Have we already exported this content?
        if ContentExporter.urls_exported.get(response.url):
            ContentExporter.report_err("url {} has already been exported".format(url), "Duplicate URL")
            return [None, None];

        data = response.json()
        tmp_url = ContentExporter.handle_howdoi(url, data)
        ContentExporter.handle_faq(data)
        if tmp_url:
            return ContentExporter.get_data(url=tmp_url)
        else:
            return url, data

    @staticmethod
    def cleanup_url(url):

        pos = url.find('?')
        if pos > 0:
            url = url[0 : pos]
        return url

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

        print("url: " + ContentExporter.cleanup_url(url))

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


if __name__ == '__main__':

    if len(sys.argv) == 2:
        ContentExporter.output_errs = sys.argv[1] == '--debug=true'

    os.environ['DJANGO_SETTINGS_MODULE'] = 'django_apps.settings'
    django.setup()

    for url in urls:

        ContentExporter.do_export(url=url)

    ContentExporter.report_err_cnt()
