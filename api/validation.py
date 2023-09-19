def validate_event(event):
	if not all(key in event for key in ['code', 'system', 'display']):
		raise Exception("Each object must contain a 'code', 'system' and 'display' value.")

	code = event['code']
	system = event['system']
	display = event['display']
	
	if system == 'age':
		if not code.isdigit() or not 1 <= int(code) <= 121:
			raise Exception("Invalid age value: {code}.")
		if code != display:
			raise Exception("Age display value should match code. Found code: {code}, display: {display}")

	elif system == 'gender':
		if code not in ['male', 'female']:
			raise Exception("Invalid gender value: {code}.")
		if code != display:
			raise Exception("Gender display value should match code. Found code: {code}, display: {display}")

	elif system == 'timegap':
		allowed_timegaps = ["00-01-month", "03-06-month", "06-12-month", "12-99-month"]
		if code not in allowed_timegaps:
			raise Exception("Invalid timegap value: {code}.")
		if code != display:
			raise Exception(f"Timegap display value should match code. Found code: {code}, display: {display}")

	elif system in ['ICD10CM', 'CPT4', 'NDC', 'HCPCS', 'RxNorm-freetext']:
		# Skipping validation for these for now.
		pass

	else:
		raise Exception("Unknown system value: {system}.")

	return True

def validate_history(history):
	if not isinstance(history, list):
		raise Exception("Input should be a list.")

	for event in history:
		validate_event(event)
