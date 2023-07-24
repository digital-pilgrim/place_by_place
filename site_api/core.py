from config_data.config import SiteSettings
from site_api.utils.site_api_handler import SiteAPIInterface


site_settings = SiteSettings()

url = f'{site_settings.api_host}'.join(['https://', '/search-nearby'])

headers = {
    'X-RapidAPI-Key': site_settings.api_key.get_secret_value(),
    'X-RapidAPI-Host': site_settings.api_host
}

params = {
    'query': '',
    'lat': '',
    'lng': '',
    'limit': 1,
    'language': 'ru',
    'region': 'ru',
    'fields': 'phone_number,'
              'name,'
              'latitude,'
              'longitude,'
              'full_address,'
              'rating,'
              'website,'
              'owner_name,'
              'photos_sample,'
              'address,'
              'street_address'
}

timeout = 5

site_api = SiteAPIInterface

if __name__ == '__main__':
    site_api()
