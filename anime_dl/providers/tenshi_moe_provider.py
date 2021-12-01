from anime_dl.providers.ProviderAPI import DubStatus, Episode, Provider, SearchResult, LoadResponse, TvStatus, ExtractorLink
from anime_dl.utils import session as ses
from bs4 import BeautifulSoup
import typing
import json
import re


class TenshiMoeProvider(Provider):
    api_name = "TenshiMoe"
    main_url = "https://tenshi.moe"
    session = ses
    __cookies = {'loop-view': 'thumb'}

    def __parse_search_page(self, soup: BeautifulSoup) -> typing.List[SearchResult]:
        return [
            SearchResult(
                x['title'],
                x['href'],
                self.api_name,
                x.find('img').get("src", None)
            )
            for x in soup.select("ul.thumb > li > a")
        ]

    def search(self, query: str) -> typing.List[SearchResult]:
        soup = BeautifulSoup(self.session.get(
            "{}/anime".format(self.main_url),
            params={'q': query},
            cookies=self.__cookies
        ).text, "html.parser")

        results = self.__parse_search_page(soup)

        while soup.select_one(".pagination"):
            link = soup.select_one('a.page-link[rel="next"]')
            if link:
                soup = BeautifulSoup(self.session.get(
                    link["href"],
                    params={'q': query},
                    cookies={'loop-view': 'thumb'}
                ).text, "html.parser")

                results.extend(self.__parse_search_page(soup))
            else:
                break

        return results

    def load(self, url: str) -> LoadResponse:
        soup = BeautifulSoup(self.session.get(url, cookies=self.__cookies).text, "html.parser")  # noqa
        title = soup.select_one("header.entry-header > h1.mb-3").text.strip()
        poster = soup.select_one("img.cover-image")
        if poster:
            poster = poster["src"]

        description = soup.select_one(".entry-description > .card-body")
        if description:
            description = description.text.strip()

        episode_nodes = soup.select("li[class*=\"episode\"] > a")

        total_episode_pages = soup.select(
            ".pagination .page-item a.page-link:not([rel])"  # noqa
        )[-1].text if soup.select(".pagination") else "1"  # noqa

        if total_episode_pages.strip().isdigit():
            total_episode_pages = int(total_episode_pages)
        else:
            total_episode_pages = 1

        for page_num in range(2, total_episode_pages):
            response = self.session.get(url, params={"page": page_num}, cookies=self.__cookies).text  # noqa
            page_soup = BeautifulSoup(response, "html.parser")
            episode_nodes.extend(page_soup.select(
                "li[class*=\"episode\"] > a"))

        episodes = [
            Episode(
                x.select_one(
                    ".episode-title").text.strip() if x.select_one(".episode-title") else None,
                x["href"],
                index + 1,
                DubStatus.SUBBED,
                x["data-content"].strip()
            )
            for index, x in enumerate(episode_nodes)
        ]

        return LoadResponse(
            title,
            url,
            self.api_name,
            episodes,
            poster,
            description
        )

    def load_links(self, url: str) -> typing.List[ExtractorLink]:
        soup = BeautifulSoup(self.session.get(url).text, "html.parser")
        sources: typing.List[ExtractorLink] = []

        for source in soup.select("[aria-labelledby=\"mirror-dropdown\"] > li > a.dropdown-item"):
            release = source.text.replace("/", "").strip()

            source_html = self.session.get(
                f"https://tenshi.moe/embed?v={source['href'].split('v=')[1].split('&')[0]}",
                headers={"Referer": url}
            ).text

            source_regex = r"sources: (\[(?:.|\s)+?type: ['\"]video/.*?['\"](?:.|\s)+?])"
            qualities = re.findall(source_regex, source_html)
            if qualities:
                qualities = qualities[0].replace("'", "\"")
                qualities = re.sub(r"(\w+): ", "\"\g<1>\": ", qualities)
                qualities = re.sub(r"\s+", "", qualities)
                qualities = qualities.replace(",}", "}").replace(",]", "]")
                qualities = json.loads(qualities)

                for quality in qualities:
                    sources.append(ExtractorLink(
                        f"{self.api_name} {release} - " + str(quality["size"]) + "p",  # noqa
                        self.fix_url(quality["src"])
                    ))
        return sources
