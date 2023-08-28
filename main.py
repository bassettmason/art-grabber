import re
import logging
from fanart import get_fan_art

def get_art(request):
    """
    Handler to retrieve fan art for a given type and ID.

    Parameters:
        request: The HTTP request object. Query parameters are used to specify the 'type' and 'id'.

    Returns:
        tuple: A tuple containing a response body, HTTP status code, and headers.
    """
    # Get type and id from request's query parameters
    type = request.args.get("type")
    id = request.args.get("id")

    headers = {"Content-Type": "application/json"}

    if not type or not id:
        logging.warning("Missing 'type' or 'id' parameter")
        return ({"error": "Missing 'type' or 'id' parameter"}, 400, headers)

    if type not in ["movie", "tv"]:
        logging.error(f"Invalid 'type' parameter: {type}. Allowed values are 'movie' or 'tv'.")
        return ({"error": "Invalid 'type' parameter. Allowed values are 'movie' or 'tv'."}, 400, headers)

    if type == "movie" and not (re.match(r"^tt\d+$", id) or id.isdigit()):
        logging.error(f"Invalid 'id' parameter for movies: {id}. The 'id' must be a valid IMDb ID (e.g., tt1517268) or a Fanart ID (numeric value).")
        return ({"error": "Invalid 'id' parameter for movies. The 'id' must be a valid IMDb ID (e.g., tt1517268) or a Fanart ID (numeric value)."}, 400, headers)
    elif type == "tv":
        logging.error(f"Invalid 'id' parameter for TV shows: {id}. The 'id' must be a numeric TVDB ID.")
        return ({"error": "Invalid 'id' parameter for TV shows. The 'id' must be a numeric TVDB ID."}, 400, headers)

    logging.info(f"Starting fan art retrieval for '{type}' with ID '{id}'.")

    try:
        art = get_fan_art(type, id)  # Assuming you have this function defined somewhere
    except Exception as e:
        logging.error(f"Failed to retrieve fan art for '{type}' with ID '{id}': {e}")
        return ({"error": str(e)}, 500, headers)

    logging.info(f"Successfully retrieved fan art for '{type}' with ID '{id}'.")
    logging.debug(f"Fan art details: {art}")

    return (art, 200, headers)
