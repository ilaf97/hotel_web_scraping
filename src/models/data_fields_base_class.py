# TODO: find correct decorator to force this as schema for child classes
class DataFieldsBaseClass:

	def get_name(self):
		pass

	@staticmethod
	def generate_slug(hotel_name: str) -> None:
		return None

	@staticmethod
	def get_resort() -> None:
		return None

	def get_description(self):
		pass

	def get_best_for(self):
		pass

	def get_rooms(self):
		pass

	def get_location(self):
		pass

	def get_facilities(self):
		pass

	def get_meals(self):
		pass

	def get_images(self):
		pass
