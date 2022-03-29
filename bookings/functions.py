from itertools import chain


def to_dict(instance):
    """
    Alternative to python's 'model_to_dict' function, which
    was excluding the non-editable 'date_of_message' field.

    https://stackoverflow.com/questions/21925671/
    convert-django-model-object-to-dict-with-all-of-the-fields-intact
    """

    opts = instance._meta
    data = {}
    for f in chain(opts.concrete_fields, opts.private_fields):
        data[f.name] = f.value_from_object(instance)
    for f in opts.many_to_many:
        data[f.name] = [i.id for i in f.value_from_object(instance)]
    return data
