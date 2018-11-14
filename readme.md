
# Metadata-Spray Beancount Plugin

Metadata spray allows you to use a regex pattern to add metadata to beancount entries. It's useful if you have many accounts and sub-accounts and want to categorize things via metadata without manual entry.

## Usage

In general, the plugin works by writing a plugin directive of "beancount_plugins_metadata_spray.plugins.metadata_spray" where the options map is a collection of 'sprays'. Each spray has the following parameters:

 - _spray_type_: Currently just account open is supported.
 - _pattern_: The regex search pattern to be used.
 - _metadata_dict_: The metadata dictionary to insert in entries matching the pattern.
 - _replace_type_: guides how to handle scenarios where an individual metadata key already exists, either:
   - _return_error_: Don't overwrite, return an error. 
   - _dont_overwrite_: Don't overwrite (no error)
   - _overwrite_: overwrite with plugin-defined metadata

### Example: Account open entries

A beancount file that looks like:

```
plugin "beancount_plugins_metadata_spray.plugins.metadata_spray" "{
    'sprays': [{ 'spray_type': 'account_open',
                 'replace_type': 'dont_overwrite',
                 'pattern': 'Assets:MyBrokerage:.*',
                 'metadata_dict': {'portfolio': 'long',
                                   'subportfolio': 'tech'}
                 }]
    }"

2018-10-20 open Assets:MyBrokerage
2018-10-20 open Assets:MyBrokerage:HOOLI
2001-01-10 open Assets:MyBrokerage:AMSFT
1998-03-20 open Assets:MyBrokerage:NWBOT
    portfolio: 'reallylong'
2005-09-07 open Assets:OtherBrokerage:HOOLI
```

Will result in entries having metadata, appearing after beancount loader something similar to this:

```
2018-10-20 open Assets:MyBrokerage
2018-10-20 open Assets:MyBrokerage:HOOLI
    portfolio: 'long'
    subportfolio: 'tech'
2001-01-10 open Assets:MyBrokerage:AMSFT
    portfolio: 'long'
    subportfolio: 'tech'
1998-03-20 open Assets:MyBrokerage:NWBOT
    portfolio: 'reallylong'
    subportfolio: 'tech'
2005-09-07 open Assets:OtherBrokerage:HOOLI
```

## Development

### Testing

Assuming a local clone of this repo, `pip install -e path_to_/beancount-plugins-metadata-spray`, then run `pytest` in the `beancount-plugins-metadata-spray` folder.

### References

The general filestructure of this plugin was based off of @xentac's [beancount plugins](https://github.com/xentac/beancount-plugins-xentac) 