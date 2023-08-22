import requests
import os
import logging
from google.cloud import secretmanager

# Use Python's built-in logging module.
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

type_mapping = {
    "movie": "movies",
    "tv": "tv"
}

type_data = {
    "movie": {
        "keys": ['hdmovielogo', 'moviebackground', 'movieposter', 'moviethumb', 'moviebanner'],
        "id_keys": ['tmdb_id', 'imdb_id']
    },
    "tv": {
        "keys": ['hdclearart', 'hdtvlogo', 'seasonbanner', 'seasonposter', 'seasonthumb', 'showbackground', 'tvbanner', 'tvposter', 'tvthumb'],
        "id_keys": ['thetvdb_id']
    }
}

def access_secret_version(project_id, secret_id, version_id="latest"):
    client = secretmanager.SecretManagerServiceClient()
    name = f"projects/{project_id}/secrets/{secret_id}/versions/{version_id}"
    response = client.access_secret_version(request={"name": name})
    return response.payload.data.decode("UTF-8")

fanart_api_key = None
# Check if running inside GitHub Actions
if os.environ.get("RUNNING_IN_GITHUB") == "true":
    fanart_api_key = os.environ.get("FANART_API_KEY")
else:
    fanart_api_key = access_secret_version("media-djinn", "FANART_API_KEY")

if not fanart_api_key:
    # Log a CRITICAL message for missing FANART_API_KEY
    logger.critical("FANART_API_KEY environment variable is not set.")
    raise ValueError("FANART_API_KEY environment variable is not set.")


def get_fan_art(type, id):
    """
    Retrieve fan art for a given type and ID.

    Parameters:
        type (str): The type of fan art to retrieve (e.g., 'movie' or 'tv').
        id (str): The ID associated with the type (e.g., IMDb ID for movies or TVDB ID for TV shows).

    Returns:
        dict: A dictionary containing fan art details for the given type and ID.
    """

    fanart_type = type_mapping.get(type, type)
    
    # Log INFO message for starting the fan art retrieval process
    logger.info(f"Starting fan art retrieval for '{type}' with ID '{id}'.")

    try:
        url = f"http://webservice.fanart.tv/v3/{fanart_type}/{id}?api_key={fanart_api_key}"
        response = requests.get(url)
        response.raise_for_status()  # Raises stored HTTPError, if one occurred.
        json_response = response.json()
    except Exception as e:
        # Log ERROR message for any exceptions during fan art retrieval
        logger.error(f"Failed to get fan art: {e}")
        type_keys = type_data[type]["keys"]
        return {
            "name": None,
            "id": id,
            **{key: None for key in type_keys}
        }

    type_keys = type_data[type]["keys"]
    id_keys = type_data[type]["id_keys"]
    logger.debug(f"Received fan art data: {json_response}")

    # Log INFO message for successful completion of fan art retrieval
    logger.info(f"Successfully retrieved fan art for '{type}' with ID '{id}'.")
    
    return construct_result(json_response, type_keys, id_keys)

def construct_result(json_response, keys, id_keys):
    """
    Construct the result dictionary with fan art details.

    Parameters:
        json_response (dict): The JSON response received from the fan art API.
        keys (list): A list of keys corresponding to different fan art details.
        id_keys (list): A list of keys corresponding to the IDs of the fan art.

    Returns:
        dict: A dictionary containing fan art details.
    """
    result = {
        'name': json_response.get('name', ''),
        'ids': {key: json_response.get(key, '') for key in id_keys}
    }
    for key in keys:
        result[key] = json_response.get(key, [{}])[0].get('url') if key in json_response else None
    return result
