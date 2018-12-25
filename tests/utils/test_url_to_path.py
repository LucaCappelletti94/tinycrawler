from tinycrawler.utils import url_to_path


def test_url_to_path():
    tests = {
        "https://github.com/gagneurlab/Manuscript_Avsec_Bioinformatics_2017/blob/master/automatic_setup.py": "github.com/gagneurlab/Manuscript_Avsec_Bioinformatics_2017/blob/master/automatic_setup.py",
        "https://github.com/gagneurlab/": "github.com/gagneurlab/index.html",
        "https://github.com/gagneurlab": "github.com/gagneurlab/index.html",
        "https://github.com": "github.com/index.html",
    }

    for url, path in tests.items():
        assert url_to_path(url) == path
