import eve_mongoengine


def generateDomain(models):
    domain = dict()
    specs = models._modelspecs
    for modelname, modelspec in specs.items():
        domain[modelname.lower()] = generateModel(modelspec)
    return domain


def generateModel(modelspec):
    model = {'item_url': 'regex("[a-f0-9]+")',
             'item_lookup_field': '_id',
             'item_methods': ['GET', 'PATCH', 'PUT', 'DELETE'],
             'resource_methods': ['GET', 'POST', 'DELETE'],
             'allowed_roles': ['admin'],
             'allowed_item_roles': ['admin'],
             'url': modelspec._class_name.lower(),
             'schema': eve_mongoengine.schema.SchemaMapper.create_schema(modelspec)}
    return model
