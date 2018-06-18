from bs4 import BeautifulSoup
from tinycrawler import TinyCrawler


def url_validator(url):
    has_root = "https://recipe.example.com/" in url
    is_not_index = "/recipe-with" not in url
    is_not_browser = url.count('/') == 3
    return has_root and is_not_index and is_not_browser


def file_parser(response, logger):
    text = response.text
    soup = BeautifulSoup(text, "lxml")
    section = soup.find(attrs={"class": "right-push"})
    if section:
        ps = section.find_all("p", recursive=False)
        pss = [p.get_text() for p in ps if not(p.get_attribute_list("id")
                                               [0] or p.get_attribute_list("class")[0])]
        return "\n".join(pss)
    logger.error("Unable to parse %s" % response.url)
    return None


seed = "https://recipe.example.com/Tiramisu.html"

crawler = TinyCrawler(use_cli=True, directory="recipes")
crawler.set_file_parser(file_parser)
crawler.set_url_validator(url_validator)

crawler.load_proxies(seed, "proxies.json")

crawler.run(seed)
