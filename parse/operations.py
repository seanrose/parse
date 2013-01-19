def construct_dict_for_relation(object_class, object_id):
    """
    Turns an object class and id into the proper format
    for a Parse relation type
    """
    return {'__type': 'Pointer',
            'className': object_class,
            'objectId': object_id}


def construct_attribute_for_where_relation(object_id, object_class,
                                           relation_attribute):
    object_relation = construct_dict_for_relation(object_class,
                                                  object_id)
    return {
        '$relatedTo': {
            'object': object_relation,
            'key': relation_attribute
        }
    }


def construct_add_relation(object_attribute, relation_class,
                           relation_id, unique=False):
    object_relation = construct_dict_for_relation(relation_class, relation_id)
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
