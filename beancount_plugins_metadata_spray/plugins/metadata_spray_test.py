# metadata_sprayer_test

from beancount_plugins_metadata_spray.plugins import metadata_spray
from beancount import loader
from beancount.core import getters

import unittest


class TestMetadataSpray(unittest.TestCase):

    @loader.load_doc(expect_errors=False)
    def test_metadata_spray_account_including_parent(self, entries, errors, options_map):
        """
            plugin "beancount_plugins_metadata_spray.plugins.metadata_spray" "{
                'sprays': [{ 'spray_type': 'account_open',
                             'replace_type': 'return_error',
                             'pattern': 'Assets:MyBrokerage.*',
                             'metadata_dict': {'portfolio': 'tech'}
                             }]
                }"

            2018-10-20 open Assets:MyBrokerage
            2018-10-20 open Assets:MyBrokerage:HOOLI
            2018-10-20 open Assets:OtherBrokerage:HOOLI

        """
        self.assertEqual(0, len(errors))
        account_entries = getters.get_account_open_close(entries)
        self.assertEqual(
            account_entries['Assets:MyBrokerage'][0].meta['portfolio'],
            'tech')
        self.assertEqual(
            account_entries['Assets:MyBrokerage:HOOLI'][0].meta['portfolio'],
            'tech')
        self.assertFalse(
            'portfolio' in account_entries['Assets:OtherBrokerage:HOOLI'][0].meta)

    @loader.load_doc(expect_errors=False)
    def test_metadata_spray_account_excluding_parent(self, entries, errors, options_map):
        """
            plugin "beancount_plugins_metadata_spray.plugins.metadata_spray" "{
                'sprays': [{ 'spray_type': 'account_open',
                             'replace_type': 'return_error',
                             'pattern': 'Assets:MyBrokerage:.*',
                             'metadata_dict': {'portfolio': 'tech',
                                               'foo': 'bar'}
                             }]
                }"

            2018-10-20 open Assets:MyBrokerage
            2018-10-20 open Assets:MyBrokerage:HOOLI
            2018-10-20 open Assets:OtherBrokerage:HOOLI

        """
        self.assertEqual(0, len(errors))
        account_entries = getters.get_account_open_close(entries)
        self.assertFalse(
            'portfolio' in account_entries['Assets:MyBrokerage'][0].meta)
        self.assertEqual(
            account_entries['Assets:MyBrokerage:HOOLI'][0].meta['portfolio'],
            'tech')
        self.assertEqual(
            account_entries['Assets:MyBrokerage:HOOLI'][0].meta['foo'],
            'bar')
        self.assertFalse(
            'portfolio' in account_entries['Assets:OtherBrokerage:HOOLI'][0].meta)

    @loader.load_doc(expect_errors=True)
    def test_metadata_spray_account_overwrite_error(self, entries, errors, options_map):
        """
            plugin "beancount_plugins_metadata_spray.plugins.metadata_spray" "{
                'sprays': [{ 'spray_type': 'account_open',
                             'replace_type': 'return_error',
                             'pattern': 'Assets:MyBrokerage:.*',
                             'metadata_dict': {'portfolio': 'tech',
                                               'foo': 'bar'}
                             }]
                }"

            2018-10-20 open Assets:MyBrokerage:HOOLI
                portfolio: "alt"

        """
        self.assertEqual(1, len(errors))
        account_entries = getters.get_account_open_close(entries)
        self.assertEqual(
            account_entries['Assets:MyBrokerage:HOOLI'][0].meta['portfolio'],
            'alt')
        self.assertEqual(
            account_entries['Assets:MyBrokerage:HOOLI'][0].meta['foo'],
            'bar')

    @loader.load_doc(expect_errors=False)
    def test_metadata_spray_account_dont_overwrite(self, entries, errors, options_map):
        """
            plugin "beancount_plugins_metadata_spray.plugins.metadata_spray" "{
                'sprays': [{ 'spray_type': 'account_open',
                             'replace_type': 'dont_overwrite',
                             'pattern': 'Assets:MyBrokerage:.*',
                             'metadata_dict': {'portfolio': 'tech',
                                               'foo': 'bar'}
                             }]
                }"

            2018-10-20 open Assets:MyBrokerage:HOOLI
                portfolio: "alt"

        """
        self.assertEqual(0, len(errors))
        account_entries = getters.get_account_open_close(entries)
        self.assertEqual(
            account_entries['Assets:MyBrokerage:HOOLI'][0].meta['portfolio'],
            'alt')
        self.assertEqual(
            account_entries['Assets:MyBrokerage:HOOLI'][0].meta['foo'],
            'bar')

    @loader.load_doc(expect_errors=False)
    def test_metadata_spray_account_overwrite(self, entries, errors, options_map):
        """
            plugin "beancount_plugins_metadata_spray.plugins.metadata_spray" "{
                'sprays': [{ 'spray_type': 'account_open',
                             'replace_type': 'overwrite',
                             'pattern': 'Assets:MyBrokerage:.*',
                             'metadata_dict': {'portfolio': 'tech',
                                               'foo': 'bar'}
                             }]
                }"

            2018-10-20 open Assets:MyBrokerage:HOOLI
                portfolio: "alt"

        """
        self.assertEqual(0, len(errors))
        account_entries = getters.get_account_open_close(entries)
        self.assertEqual(
            account_entries['Assets:MyBrokerage:HOOLI'][0].meta['portfolio'],
            'tech')
        self.assertEqual(
            account_entries['Assets:MyBrokerage:HOOLI'][0].meta['foo'],
            'bar')

    @loader.load_doc(expect_errors=False)
    def test_metadata_spray_account_multiple(self, entries, errors, options_map):
        """
            plugin "beancount_plugins_metadata_spray.plugins.metadata_spray" "{
                'sprays': [{ 'spray_type': 'account_open',
                             'replace_type': 'return_error',
                             'pattern': 'Assets:MyBrokerage:.*',
                             'metadata_dict': {'portfolio': 'tech'}
                             },
                           { 'spray_type': 'account_open',
                             'replace_type': 'return_error',
                             'pattern': 'Assets:OtherBrokerage:.*',
                             'metadata_dict': {'portfolio': 'tech'}
                             }]
                }"

            2018-10-20 open Assets:MyBrokerage:HOOLI
            2018-10-20 open Assets:OtherBrokerage:HOOLI

        """
        self.assertEqual(0, len(errors))
        account_entries = getters.get_account_open_close(entries)
        self.assertEqual(
            account_entries['Assets:MyBrokerage:HOOLI'][0].meta['portfolio'],
            'tech')
        self.assertEqual(
            account_entries['Assets:OtherBrokerage:HOOLI'][
                0].meta['portfolio'],
            'tech')
