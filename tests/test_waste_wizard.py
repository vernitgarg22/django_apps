from django.test import Client
from django.test import TestCase

import cod_utils.util

from tests import test_util

from waste_wizard.models import WasteItem


def cleanup_db():
    test_util.cleanup_model(WasteItem)


class WasteWizardTests(TestCase):

    def setUp(self):
        """
        Set up each unit test, including making sure database is properly cleaned up before each test
        """
        cleanup_db()

    def test_waste_item_model(self):
        item = WasteItem(description='test item', destination='trash')
        str_desc = str(item)
        self.assertTrue(str_desc.find('test item') >= 0 and str_desc.find('trash') >= 0)

    def test_get_search_page(self):

        c = Client()

        response = c.get('/waste_wizard/')
        self.assertTrue(response.status_code == 200)
        # TODO remove csrf token from response? it changes with each call, so it breaks the comparison
        # expected = b'\n\n<html>\n    <head>\n        <link rel="stylesheet" type="text/css" href="/static/waste_wizard/style.css" />\n\n        <script src="https://code.jquery.com/jquery-1.12.4.js"></script>\n        <script src="https://code.jquery.com/ui/1.12.1/jquery-ui.js"></script>\n\n        <script>\n          $( function() {\n            var availableTags = [];\n            $( "#id_description" ).autocomplete({\n              source: availableTags\n            });\n          } );\n        </script>\n\n    </head>\n    <body>\n\n        <div style="padding-bottom: 20px">\n            <a href="/waste_wizard/items">Items Index</a>\n        </div>\n\n        <div style="clear: both;">\n            <form action="/waste_wizard/results/" method="post">\n                <input type=\'hidden\' name=\'csrfmiddlewaretoken\' value=\'vEg0Qc1ilCGgBx8wQvEq4pQkmW1QN6VE\' />\n                <tr><th><label for="id_description">Search for a waste item:</label></th><td><input id="id_description" maxlength="100" name="description" type="text" /></td></tr>\n                <input type="submit" value="Search" />\n            </form>\n        </div>\n\n    </body>\n</html>\n'
        # self.assertTrue(response.content == expected, "Waste wizard shows search page")

    def test_list_no_items(self):

        c = Client()

        response = c.get('/waste_wizard/items/')
        self.assertTrue(response.status_code == 200)
        expected = b'\n\n<html>\n    <head>\n        <link rel="stylesheet" type="text/css" href="/static/waste_wizard/style.css" />\n    </head>\n    <body>\n\n        <a class="back_link" href="/waste_wizard/">Back</a>\n\n        <div class="item_topics">\n            Waste Item Topics\n        </div>\n\n        \n\n    </body>\n</html>\n'
        self.assertTrue(response.content == expected, "Waste wizard lists empty items page")

    def test_list_item(self):

        c = Client()
        item = WasteItem(description='test item', destination='trash', notes='test item')
        item.save()

        response = c.get('/waste_wizard/items/')
        self.assertTrue(response.status_code == 200)
        expected = b'\n\n<html>\n    <head>\n        <link rel="stylesheet" type="text/css" href="/static/waste_wizard/style.css" />\n    </head>\n    <body>\n\n        <a class="back_link" href="/waste_wizard/">Back</a>\n\n        <div class="item_topics">\n            Waste Item Topics\n        </div>\n\n        \n            <div class="item_list_row">\n                <div class="item_list_first">\n                    \n    T\n    <ul>\n        \n            <li><a href="/waste_wizard/detail/test%20item/">test item</a></li>\n        \n    </ul>\n\n                </div>\n                <div>\n                    \n                </div>\n            </div>\n        \n\n    </body>\n</html>\n'
        self.assertTrue(response.content == expected, "Waste wizard lists items page with 1 item")

    def test_get_results(self):

        c = Client()
        item = WasteItem(description='test item', destination='trash', notes='test item')
        item.save()

        response = c.get('/waste_wizard/results/')
        self.assertTrue(response.status_code == 200)
        # TODO remove csrf token from response? it changes with each call, so it breaks the comparison
        # expected = b'\n\n<html>\n    <head>\n        <link rel="stylesheet" type="text/css" href="/static/waste_wizard/style.css" />\n\n        <script src="https://code.jquery.com/jquery-1.12.4.js"></script>\n        <script src="https://code.jquery.com/ui/1.12.1/jquery-ui.js"></script>\n\n        <script>\n          $( function() {\n            var availableTags = ["", "test item"];\n            $( "#id_description" ).autocomplete({\n              source: availableTags\n            });\n          } );\n        </script>\n\n    </head>\n    <body>\n\n        <a class="back_link" href="/waste_wizard/">New Search</a>\n\n        \n            <table>\n                <thead>\n                    <tr>\n                        <th class="description">Waste Item</th>\n                        <th class="destination">Destination</th>\n                        <th class="notes">Notes</th>\n                    </tr>\n                </thead>\n                <tbody>\n                    \n                        <tr>\n                            <td class="description">\n                                <a href="/waste_wizard/detail/test%20item/">test item</a>\n                            </td>\n                            <td class="destination">Trash</td>\n                            <td class="notes">test item</td>\n                        </tr>\n                    \n                </tbody>\n            </table>\n            \n\n        <form action="/waste_wizard/results/" method="post">\n            <input type=\'hidden\' name=\'csrfmiddlewaretoken\' value=\'hhQ2WFWtJ8ZWcoSVyqSIlSmCKavYcCvU\' />\n            <tr><th><label for="id_description">Search for another waste item:</label></th><td><input id="id_description" maxlength="100" name="description" type="text" /></td></tr>\n            <input type="submit" value="Search" />\n        </form>\n\n    </body>\n</html>\n'
        # self.assertTrue(response.content == expected, "Waste wizard lists results page with 1 item")

    def test_post_results(self):

        c = Client()
        item = WasteItem(description='test item', destination='trash', notes='test item')
        item.save()

        response = c.post('/waste_wizard/results/', { "description": "test item"} )
        self.assertTrue(response.status_code == 200)
        # TODO remove csrf token from response? it changes with each call, so it breaks the comparison
        # expected = b'\n\n<html>\n    <head>\n        <link rel="stylesheet" type="text/css" href="/static/waste_wizard/style.css" />\n\n        <script src="https://code.jquery.com/jquery-1.12.4.js"></script>\n        <script src="https://code.jquery.com/ui/1.12.1/jquery-ui.js"></script>\n\n        <script>\n          $( function() {\n            var availableTags = ["", "test item"];\n            $( "#id_description" ).autocomplete({\n              source: availableTags\n            });\n          } );\n        </script>\n\n    </head>\n    <body>\n\n        <a class="back_link" href="/waste_wizard/">New Search</a>\n\n        \n            <table>\n                <thead>\n                    <tr>\n                        <th class="description">Waste Item</th>\n                        <th class="destination">Destination</th>\n                        <th class="notes">Notes</th>\n                    </tr>\n                </thead>\n                <tbody>\n                    \n                        <tr>\n                            <td class="description">\n                                <a href="/waste_wizard/detail/test%20item/">test item</a>\n                            </td>\n                            <td class="destination">Trash</td>\n                            <td class="notes">test item</td>\n                        </tr>\n                    \n                </tbody>\n            </table>\n            \n\n        <form action="/waste_wizard/results/" method="post">\n            <input type=\'hidden\' name=\'csrfmiddlewaretoken\' value=\'hhQ2WFWtJ8ZWcoSVyqSIlSmCKavYcCvU\' />\n            <tr><th><label for="id_description">Search for another waste item:</label></th><td><input id="id_description" maxlength="100" name="description" type="text" /></td></tr>\n            <input type="submit" value="Search" />\n        </form>\n\n    </body>\n</html>\n'
        # self.assertTrue(response.content == expected, "Waste wizard lists results page with 1 item")

    def test_post_results_no_description(self):

        c = Client()
        item = WasteItem(description='test item', destination='trash', notes='test item')
        item.save()

        response = c.post('/waste_wizard/results/')
        self.assertTrue(response.status_code == 200)
        expected = b'Please try your search again'
        self.assertTrue(response.content == expected, "Waste wizard lists results page with 1 item")

    def test_post_results_none(self):

        c = Client()

        response = c.post('/waste_wizard/results/', { "description": "dummy" } )
        self.assertTrue(response.status_code == 200)
        # TODO remove csrf token from response? it changes with each call, so it breaks the comparison
        # expected = b'\n\n<html>\n    <head>\n        <link rel="stylesheet" type="text/css" href="/static/waste_wizard/style.css" />\n\n        <script src="https://code.jquery.com/jquery-1.12.4.js"></script>\n        <script src="https://code.jquery.com/ui/1.12.1/jquery-ui.js"></script>\n\n        <script>\n          $( function() {\n            var availableTags = [];\n            $( "#id_description" ).autocomplete({\n              source: availableTags\n            });\n          } );\n        </script>\n\n    </head>\n    <body>\n\n        <a class="back_link" href="/waste_wizard/">New Search</a>\n\n        \n            <p>No waste items were found.</p>\n        \n\n        <form action="/waste_wizard/results/" method="post">\n            <input type=\'hidden\' name=\'csrfmiddlewaretoken\' value=\'MHC8yCaaJdsF56QmVEDQX3wjvk9IkORL\' />\n            <tr><th><label for="id_description">Search for another waste item:</label></th><td><input id="id_description" maxlength="100" name="description" type="text" /></td></tr>\n            <input type="submit" value="Search" />\n        </form>\n\n    </body>\n</html>\n'
        # self.assertTrue(response.content == expected, "Waste wizard lists results page with 1 item")

    def test_post_results_keywords(self):

        c = Client()
        item = WasteItem(description='test item', destination='trash', notes='test item', keywords='dummy')
        item.save()

        response = c.post('/waste_wizard/results/', { "description": "dummy" } )
        self.assertTrue(response.status_code == 200)
        # TODO remove csrf token from response? it changes with each call, so it breaks the comparison
        # expected = b'\n\n<html>\n    <head>\n        <link rel="stylesheet" type="text/css" href="/static/waste_wizard/style.css" />\n\n        <script src="https://code.jquery.com/jquery-1.12.4.js"></script>\n        <script src="https://code.jquery.com/ui/1.12.1/jquery-ui.js"></script>\n\n        <script>\n          $( function() {\n            var availableTags = ["dummy", "test item"];\n            $( "#id_description" ).autocomplete({\n              source: availableTags\n            });\n          } );\n        </script>\n\n    </head>\n    <body>\n\n        <a class="back_link" href="/waste_wizard/">New Search</a>\n\n        \n            <table>\n                <thead>\n                    <tr>\n                        <th class="description">Waste Item</th>\n                        <th class="destination">Destination</th>\n                        <th class="notes">Notes</th>\n                    </tr>\n                </thead>\n                <tbody>\n                    \n                        <tr>\n                            <td class="description">\n                                <a href="/waste_wizard/detail/test%20item/">test item</a>\n                            </td>\n                            <td class="destination">Trash</td>\n                            <td class="notes">test item</td>\n                        </tr>\n                    \n                </tbody>\n            </table>\n            \n\n        <form action="/waste_wizard/results/" method="post">\n            <input type=\'hidden\' name=\'csrfmiddlewaretoken\' value=\'P1kZ7tZ0K5FZGuw5lE6PRhwrZB3guosJ\' />\n            <tr><th><label for="id_description">Search for another waste item:</label></th><td><input id="id_description" maxlength="100" name="description" type="text" /></td></tr>\n            <input type="submit" value="Search" />\n        </form>\n\n    </body>\n</html>\n'
        # self.assertTrue(response.content == expected, "Waste wizard lists results page with 1 item")

    def test_get_detail(self):

        c = Client()
        item = WasteItem(description='test item', destination='trash', notes='test item')
        item.save()

        response = c.get('/waste_wizard/detail/test%20item/')
        self.assertTrue(response.status_code == 200)
        expected = b'\n\n<html>\n    <head>\n        <link rel="stylesheet" type="text/css" href="/static/waste_wizard/style.css" />\n    </head>\n    <body>\n\n        <a class="back_link" href="/waste_wizard/">New Search</a>\n\n        <table class="waste_item_detail">\n            <tbody>\n                <tr>\n                    <td>Waste Item</td>\n                    <td>test item</td>\n                </tr>\n                <tr>\n                    <td>Destination</td>\n                    <td>Trash</td>\n                </tr>\n                \n                    <tr>\n                        <td>Notes</td>\n                        <td>test item</td>\n                    </tr>\n                \n                <tr>\n                    <td></td>\n                    <td>\n                        \n                    </td>\n                </tr>\n            </tbody>\n        </table>\n\n    </body>\n</html>\n'
        self.assertTrue(response.content == expected, "Waste wizard lists results page with 1 item")

    def test_get_detail_404(self):

        c = Client()

        response = c.get('/waste_wizard/detail/test%20item/')
        self.assertTrue(response.status_code == 404)
