from tinycrawler import TinyCrawler
from bs4 import BeautifulSoup


def url_validator(url):
    root = "https://www.example.com/recipes/"
    return url.startswith(root) and url.count("/") == 8 and "?" not in url


def file_parser(response, logger):
    soup = BeautifulSoup(response.text, "lxml")
    section = soup.find(attrs={"class": "sp-corpo lato col-md-12"})
    if not section:
        section = soup.find(attrs={"class": "plain-step-container"})

    if section:
        ps = [p.get_text() for p in section.find_all("p")]
        return "\n".join(ps)

    logger.error("Unable to parse %s" % response.url)
    return None


seed = "https://www.example.com/recipes/spaghetti/"

crawler = TinyCrawler(use_cli=True, directory="recipes")
crawler.set_file_parser(file_parser)
crawler.set_url_validator(url_validator)

crawler.load_proxies("https://1.0.0.1/", "proxies.json")

crawler.run(seed)
