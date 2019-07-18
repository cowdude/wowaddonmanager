from requests_html import HTMLSession
import re


def get_info(name):
    """
    Given an addon slug name, returns (download url, archive hash).
    Raises if no download link was mined from the addon web page.
    """
    session = HTMLSession()
    root = "https://www.curseforge.com/wow/addons/%s" % name
    r = session.get("%s/files" % root)

    md5 = r.html.find(":contains(MD5) + *", first=True)
    md5 = md5.text

    link = r.html.find("a[href^='/wow/addons/%s/download/']" % name, first=True)
    if not link:
        raise RuntimeError("Download link not found")

    uri = link.attrs["href"]
    url = "https://www.curseforge.com" + ("%s/file" % uri)
    return url, md5

