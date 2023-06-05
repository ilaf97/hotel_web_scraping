from abc import abstractmethod


class DataFieldsBaseClass:

	def get_name(self):
		pass

	@staticmethod
	@abstractmethod
	def generate_slug(hotel_name: str) -> None:
		return None

	@staticmethod
	def get_resort() -> None:
		return None

	@abstractmethod
	def get_description(self):
		pass

	@abstractmethod
	def get_best_for(self):
		pass

	@abstractmethod
	def get_rooms(self):
		pass

	@abstractmethod
	def get_location(self):
		pass

	@abstractmethod
	def get_facilities(self):
		pass

	@abstractmethod
	def get_meals(self):
		pass

	@abstractmethod
	def get_images(self):
		pass
