from src.models.hotel_model import Hotel


def convert_json_list_to_hotel_obj_list(json_list):
	hotel_obj_list = []
	for hotel in json_list:
		hotel_obj = Hotel(**hotel)
		hotel_obj_list.append(hotel_obj)

	return hotel_obj_list

