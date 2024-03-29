fmcschema = {
    'hostname': {
        'type': 'string'
    },
    'ipaddr': {
        'type': 'string'
    },
    'status': {
        'type': 'string'
    },
    'failcode': {
        'type': 'string'
    }
}

overallschema = {
    'name': {
        'type': 'string'
    },
    'status': {
        'type': 'string'
    }
}

canaries = {
    'item_title': 'canary',
    'additional_lookup': {
        'url': 'regex("[\w]+")',
        'field': 'hostname'
    },
    'resource_methods': ['GET'],
    'schema': fmcschema
}

coalmine = {
    'resource_methods': ['GET'],
    'additional_lookup': {
        'url': 'regex("[\w]+")',
        'field': 'name'
    },
    'schema': overallschema
}

DOMAIN = {'canaries': canaries,
          'coalmine': coalmine}

ALLOW_UNKNOWN = True
MONGO_USERNAME = 'lookout'
MONGO_PASSWORD = 'HashBangFP'
MONGO_HOST = 'localhost'
MONGO_PORT = 27017
MONGO_DBNAME = 'fmcDB'
