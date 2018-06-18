from bs4 import BeautifulSoup
from tinycrawler import TinyCrawler


def soft_validator(url: str):
    root = "https://www.example.com/"
    return url.startswith(root) and url.endswith("/")


def strong_validator(url: str):
    root = "https://www.example.com/recipes/"
    return url.startswith(root) and url.count("/") == 6


def file_parser(response, logger):
    if not strong_validator(response.url):
        logger.log("I don't wanna parse %s" % response.url)
        return None
    soup = BeautifulSoup(response.text, "lxml")
    section = soup.find("div", attrs={"class": "entry"})
    if section:
        [s.extract() for s in section('script')]
        ps = section.find_all("p", recursive=False)
        return "\n".join([p.get_text() for p in ps])
    logger.log("Unable to parse %s" % response.url)
    return None


seed = "https://www.example.com/recipes/my/salad/"

crawler = TinyCrawler(use_cli=True, directory="recipes")
crawler.set_file_parser(file_parser)
crawler.set_url_validator(soft_validator)

crawler.load_proxies("https://1.0.0.1/", "proxies.json")

crawler.run(seed)
