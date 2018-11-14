# metadata_spray.py

import collections
import re

from beancount.core import data
from beancount.core import account
from beancount.core import getters
from beancount.core.data import Custom

__plugins__ = ('metadata_spray_entries',)

MetadataSprayError = collections.namedtuple(
    'MetadataSprayError', 'source message entry')

# Supported spray types
MetadataSprayTypes = ['account_open']

# Metadata Replace Types
# ---
# This dictates how the metadata spray will deal with situations
# where a type of metadata already exists.
# Generally the default is to return an error,
# but the options to either not overwrite metadata or
# replace all also exist.
MetadataSprayReplaceType = ['return_error', 'dont_overwrite', 'overwrite']

metadata_spray_error_meta = data.new_metadata('<metadata_spray>', 0)


def metadata_spray(entry,
                   replace_type,
                   metadata_dict):
    errors = []
    entry_meta = entry[0].meta

    for metadata_key in metadata_dict:
        if metadata_key in entry_meta:
            if replace_type == 'return_error':
                errors.append(
                    MetadataSprayError(
                        metadata_spray_error_meta,
                        "Existing metadata {} found in entry, skipping",
                        metadata_key))
                continue
            elif replace_type == 'dont_overwrite':
                continue

        entry_meta[metadata_key] = metadata_dict[metadata_key]

    return entry_meta, errors


def metadata_spray_account_open(entries,
                                replace_type,
                                pattern,
                                metadata_dict):
    errors = []
    account_entries = getters.get_account_open_close(entries)
    regexer = re.compile(pattern)

    for account_ in account_entries:
        # Only operate on account Open entries
        entry = account_entries[account_]
        if(getattr(entry[0].__class__, '__name__') != 'Open'):
            continue

        if(regexer.match(account_)):
            spray_meta, spray_errors = metadata_spray(
                entry,
                replace_type,
                metadata_dict)
            spray_entry = data.Open(spray_meta,
                                    entry[0].date,
                                    entry[0].account,
                                    None,
                                    None)

            # Modify entries and update errors
            entry_index = entries.index(entry[0])
            entries[entry_index] = spray_entry
            errors += spray_errors

    return entries, errors


def metadata_spray_entries(entries, options_map, config_str):
    """
    Insert metadata on
    """
    errors = []

    config_obj = eval(config_str, {}, {})
    sprays = config_obj['sprays']
    for spray in sprays:

        if ('spray_type' not in spray) or \
                ('replace_type' not in spray):
            errors.append(
                MetadataSprayError(metadata_spray_error_meta,
                                   "Missing spray or replace type, \
                    skipping this spray operation")
            )
            continue

        spray_type = spray['spray_type']
        if spray_type not in MetadataSprayTypes:
            errors.append(
                MetadataSprayError(metadata_spray_error_meta,
                                   "Invalid spray type: {} \
                                skipping this spray operation",
                                   spray_type))
            continue

        replace_type = spray['replace_type']
        if(replace_type not in MetadataSprayReplaceType):
            errors.append(
                MetadataSprayError(metadata_spray_error_meta,
                                   "Invalid spray type: {} \
                                skipping this spray operation",
                                   spray_type))
            continue

        if spray_type == 'account_open':
            entries, new_errors = metadata_spray_account_open(
                entries,
                replace_type,
                spray['pattern'],
                spray['metadata_dict'])
            errors += new_errors

    return entries, errors
