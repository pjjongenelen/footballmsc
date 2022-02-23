import beautifulsoup4 as bs4
from requests import get

response = get("http://www.vi.nl/nieuws/nec-blunder-houdt-goffert-syndroom-in-stand", verify=False)
