# Modules
import requests
from selectolax.parser import HTMLParser
# ===================================================================== #

class Scrape:
    def __init__(self, website: str):
        self.website = website
    # ---------------------------------------------- #

    def extract_html(self) -> str:
        response = requests.get(self.website)

        if (response.status_code == 200):
            return response.content.decode()
        else:
            raise Exception(f"Error fetching html {response.status_code}")
    # ---------------------------------------------- #
    
    def extract_content(self, page_source: str) -> str:
        html = HTMLParser(page_source)
        
        for tag in html.css("script, style, iframe, noscript"):
            tag.decompose()

        content = html.body.text(separator="\n")
        content = "\n".join([l.strip() for l in content.splitlines() if (l.strip())])
        
        return content
# --------------------------------------------------------------------- #