from pypif_sdk.readview import ReadView
from pypif.obj.common import Value
from json import dumps


def pif_to_mdf_record(pif):
   """Convert a PIF into partial MDF record"""
   res = {}
   res["mdf"] = _to_meta_data(pif)
   res["{source_name}"] = _to_user_defined(pif)
   return dumps(res)


def _to_meta_data(pif):
    """Convert the meta-data from the PIF into MDF"""
    return {}


def _to_user_defined(pif):
    """Read the systems in the PIF to populate the user-defined portion"""
    res = {}

    # make a read view to flatten the heirarchy
    rv = ReadView(pif)

    # Iterate over the keys in the read view
    for k in rv.keys():
        name, value = _extract_key_value(rv[k].raw)
        # add any objects that can be extracted
        if name and value is not None:
            res[name] = value
    return res


def _construct_new_key(name, units=None):
    """Construct an MDF safe key from the name and units"""
    cat = name
    if units:
        cat = "_".join([name, units])
    to_remove = ["/", "\\", "*", "^", "#", " ", "\n", "\t"]
    for c in to_remove:
       cat = cat.replace(c, "_")
    return cat


def _extract_key_value(obj):
    """Extract the value from the object and make a descriptive key"""

    # Parse a Value object, which includes Properties
    if isinstance(obj, Value):
        key = _construct_new_key(obj.name, obj.units)
        value = None
        if obj.scalars and len(obj.scalars) == 1:
            value = obj.scalars[0].value
        elif obj.scalars:
            value =  [x.value for x in obj.scalars]
        elif obj.vectors and len(obj.vectors) == 1:
            value = [x.value for x in obj.vectors[0]]
        
    return key, value

