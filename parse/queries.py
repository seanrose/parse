from .operations import pointer


class Query(object):
    """A light wrapper for Parse queries

    Right now this only holds the constraints and object class for a given
    query. It also has a helper to create relations. This will eventually
    have helpers to support all of the relation types Parse has
    """

    def __init__(self, parse_client, object_class, constraints=None):

        self.constraints = {} if not constraints else constraints
        self.object_class = object_class
        self.parse_client = parse_client

    def add_pointer(self, attribute_name, object_class, object_id):

        self.constraints[attribute_name] = pointer(object_class, object_id)

    def add_relation(self, parent_attribute_name, parent_object_class,
                     parent_object_id):

        self.constraint['$relatedTo'] = {
            'object': pointer(parent_object_class, parent_object_id),
            'key': parent_attribute_name
        }

    def execute(self):
        """Runs the query"""
        return self.parse_client.query_object_class(self.object_class,
                                                    self.constraints)
