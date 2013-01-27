def pointer(object_class, object_id):
    """
    Turns an object class and id into the proper format
    for a Parse relation type
    """
    return {'__type': 'Pointer',
            'className': object_class,
            'objectId': object_id}


def construct_add_relation(object_attribute, relation_class,
                           relation_id, unique=False):
    object_relation = pointer(relation_class, relation_id)
    if unique:
        op = 'AddUnique'
    else:
        op = 'AddRelation'
    return {
        object_attribute: {
            '__op': op,
            'objects': [object_relation]
        }
    }


def construct_increment_relation(amount_to_increment):
    return {'__op': 'Increment', 'amount': amount_to_increment}
