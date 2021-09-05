# This file contains configuration for production environment
# read more here http://exploreflask.com/en/latest/configuration.html
DEBUG = False

"""
We need this to have the json payloads encoded in UTF-8 (for ç, ã, é, etc.)

'If this is disabled, the JSON will be returned as a Unicode string, or encoded as UTF-8 by jsonify. 
This has security implications when rendering the JSON in to JavaScript in templates, and should typically remain enabled.

Default: True'
http://flask.pocoo.org/docs/1.0/config/
"""
JSON_AS_ASCII = False