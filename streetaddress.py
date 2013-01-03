from addressconf import Directions, Streets, States, Regexes
import re

#street_type_regexp = re.compile('|'.join(Streets.STREET_TYPES_LIST.keys()), re.IGNORECASE)
#number_regexp = re.compile(r'\d+-?\d*')
#fraction_regexp = re.compile(r'\d+\/\d+')
#state_regexp = re.compile('|'.join([v.replace(' ','\\s') for v in (States.STATE_CODES.values() + States.STATE_CODES.keys())]), re.IGNORECASE)
#direct_regexp = re.compile('|'.join(Directions.DIRECTIONAL.keys()) + '|' + '|'.join([(''.join([n+'\\.' for n in v])+'|'+v) for v in sorted(Directions.DIRECTIONAL.values(), key=len, reverse=True)]), re.IGNORECASE)
#zip_regexp = re.compile(r'(\d{5})(?:-(\d{4}))?')
#corner_regexp = re.compile(r'(?:\band\b|\bat\b|&|\@)', re.IGNORECASE)
#unit_regexp = re.compile(r'(?:(su?i?te|p\W*[om]\W*b(?:ox)?|dept|apt|apartment|ro*m|fl|unit|box)\W+|\#\W*)([\w-]+)', re.IGNORECASE)
#street_regexp = re.compile(r'(?:(?:({0})\W+({1})\b)|(?:({0})\W+)?(?:([^,]+)(?:[^\w,]+({1})\b)(?:[^\w,]+({0})\b)?|([^,]*\d)({0})\b|([^,]+?)(?:[^\w,]+({1})\b)?(?:[^\w,]+({0})\b)?))'.format(direct_regexp.pattern,street_type_regexp.pattern), re.IGNORECASE)
#place_regexp = re.compile(r'(?:([^\d,]+?)\W+(${0})\W*)?(?:{1})?'.format(state_regexp.pattern,zip_regexp.pattern), re.IGNORECASE)
#address_regexp = re.compile(r'\A\W*({0})\W*(?:{1}\W*)?{2}\W+(?:{3}\W+)?{4}\W*\Z'.format(number_regexp.pattern,fraction_regexp.pattern,street_regexp.pattern,unit_regexp.pattern,place_regexp.pattern), re.IGNORECASE)

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
			'street_type':match_data[5] or match_data[2],
			'unit':match_data[13],
			'unit_prefix':match_data[12],
			'suffix':match_data[6] or match_data[11],
			'prefix':match_data[3],
			'city':match_data[14],
			'state':match_data[15],
			'postal_code':match_data[16],
			'postal_code_ext':match_data[17]})

def normalize_address(addr):
	addr['state'] = normalize_state(addr['state']) if 'state' in addr and addr['state'] else None
 	addr['street_type'] = normalize_street_type(addr['street_type']) if 'street_type' in addr and addr['street_type'] else None
        addr['prefix'] = normalize_directional(addr['prefix']) if 'prefix' in addr and addr['prefix'] else None
        addr['suffix'] = normalize_directional(addr['suffix']) if 'suffix' in addr and addr['suffix'] else None
        addr['street'] = addr['street'].upper() if 'street' in addr and addr['street'] else None
        addr['street_type2'] = normalize_street_type(addr['street_type2']) if 'street_type2' in addr and addr['street_type2'] else None
	addr['prefix2'] = normalize_directional(addr['prefix2']) if 'prefix2' in addr and addr['prefix2'] else None
        addr['suffix2'] = normalize_directional(addr['suffix2']) if 'suffix2' in addr and addr['suffix2'] else None
        addr['street2'] = addr['street2'].upper() if 'street2' in addr and addr['street2'] else None
        addr['city'] = addr['city'].upper() if 'city' in addr and addr['city'] else None
        addr['unit_prefix'] = addr['unit_prefix'].upper() if 'unit_prefix' in addr and addr['unit_prefix'] else None
	return addr 

def normalize_state(state):
	if len(state) < 3:
		return state.upper()
	else:
		return States.STATE_CODES[state.lower()]

def normalize_street_type(s_type):
	if s_type.lower() in Streets.STREET_TYPES:
		return Streets.STREET_TYPES[s_type.lower()]
	elif s_type.lower() in Streets.STREET_TYPES_LIST:
		return s_type.upper()
      
def normalize_directional(direction):
	if len(direction) < 3:
		return direction.upper()
	else:
		return Directions.DIRECTIONAL[direction.lower()]
