def validate_user_input(user_input) -> bool:
	if user_input.lower() not in {'yes', 'y', 'no', 'n'}:
		raise ValueError("Invalid user input!"
						 "\nUser input must be 'yes', 'y', 'no' or 'n'")
	if user_input.lower() in {'yes', 'y'}:
		return True
	return False
