from .addressconf import Directions, Streets, States, Regexes
import re

def parse(location):
	if Regexes.corner.search(location):
		return parse_intersection(location)
	else:
		return parse_address(location)

def parse_intersection(inter):
	match = Regexes.intersection.match(inter)
	if not match:
		return
	match_data = match.groups()
	return normalize_address({'street':match_data[3] or match_data[8],
			'street_type':match_data[4],
			'suffix':match_data[5],
			'prefix':match_data[2],
			'street2':match_data[14] or match_data[19],
			'street_type2':match_data[15],
			'suffix2':match_data[16],
			'prefix2':match_data[13],
			'city':match_data[22],
			'state':match_data[23],
			'postal_code':match_data[24]})

def parse_address(addr):
    match = Regexes.address.match(addr)
    if not match:
        return
    match_data = match.groups()
    return normalize_address({'number':match_data[0],
            'street':match_data[4] or match_data[9] or match_data[1],
            'type':match_data[5] or match_data[2],
            'sec_unit_num':match_data[13],
            'sec_unit_type':match_data[12],
            'suffix':match_data[6] or match_data[11],
            'prefix':match_data[3],
            'city':match_data[14],
            'state':match_data[15],
            'zip':match_data[16],
            'zip_ext':match_data[17]})

def normalize_address(addr):
    addr['state'] = normalize_state(addr.get('state', None))
    addr['city'] = normalize_city(addr.get('city', None))

    addr['type'] = normalize_street_type(addr.get('type', None))

    addr['street_type2'] = normalize_street_type(addr.get('street_type2', None))

    addr['prefix'] = normalize_directional(addr.get('prefix', None))
    addr['prefix2'] = normalize_directional(addr.get('prefix2', None))
    addr['suffix'] = normalize_directional(addr.get('suffix', None))
    addr['suffix2'] = normalize_directional(addr.get('suffix2', None))

    addr['unit_prefix'] = _upper_if_exists(addr.get('unit_prefix', None))

    addr = dict((k,v) for k,v in addr.items() if v)

    return addr

def normalize_city(city) :
    if not city :
        return None
    city_list = []
    for word in city.split() :
        if word in Directions.DIRECTIONAL_CODES :
            city_list.append(Directions.DIRECTIONAL_CODES[word].title())
        else :
            city_list.append(word)
    return ' '.join(city_list)

def normalize_state(state):
    if not state :
        return None
    if len(state) < 3:
        return state.upper()
    else:
        return States.STATE_CODES[state.lower()]

def normalize_street_type(s_type):
    if not s_type :
        return None
    if s_type.lower() in Streets.STREET_TYPES:
        return Streets.STREET_TYPES[s_type.lower()].title()
    elif s_type.lower() in Streets.STREET_TYPES_LIST:
        return s_type.title()

def normalize_directional(direction):
    if not direction :
        return None
    if len(direction) < 3:
        return direction.upper()
    else:
        return Directions.DIRECTIONAL[direction.lower()]

def _upper_if_exists(field) :
    if not field :
        return None
    else :
        return field.upper()
