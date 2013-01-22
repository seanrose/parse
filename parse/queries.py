

class Query(object):
    """A light wrapper for Parse queries

    Right now this only holds the constraints and object class for a given
    query. It also has a helper to create relations. This will eventually
    have helpers to support all of the relation types Parse has
    """

    def __init__(self, constraints=None, object_class=None):

        self.constraints = {} if not constraints else constraints

        # Query requires a specific object class
        if not object_class:
            raise AttributeError(
                """Queries must be instantiated with a an object_class e.g.
                >>> q = Query(object_class='Users')"""
            )

    def add_relation(attribute_name, object_class, object_id):
        # TODO: implement
        return
