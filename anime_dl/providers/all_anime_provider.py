from anime_dl.providers.ProviderAPI import Provider, SearchResult, LoadResponse, TvStatus, ExtractorLink
from anime_dl.utils import session as ses
from bs4 import BeautifulSoup
import typing
import dukpy


def get_status(status):
    if status == "Releasing":
        return TvStatus.ONGOING
    return TvStatus.COMPLETED


class AllAnimeProvider(Provider):
    api_name = "AllAnimeProvider"
    main_url = "https://allanime.site"
    session = ses

    def search(self, query: str) -> typing.List[SearchResult]:
        payload = f"variables=%7B%22search%22%3A%7B%22allowAdult%22%3Afalse%2C%22query%22%3A%22{query}%22%7D%2C%22limit%22%3A100%2C%22page%22%3A1%2C%22translationType%22%3A%22sub%22%7D&extensions=%7B%22persistedQuery%22%3A%7B%22version%22%3A1%2C%22sha256Hash%22%3A%229343797cc3d9e3f444e2d3b7db9a84d759b816a4d84512ea72d079f85bb96e98%22%7D%7D"
        response = self.session.get(f"https://allanime.site/graphql?{payload}")

        if "PERSISTED_QUERY_NOT_FOUND" in response.text:
            response = self.session.get(
                f"https://allanime.site/graphql?{payload}")
            if "PERSISTED_QUERY_NOT_FOUND" in response.text:
                return []

        response = response.json()
        results = []
        for result in response["data"]["shows"]["edges"]:
            skip = 0

            episodes = result["availableEpisodes"]

            for typ in ("raw", "sub", "dub"):
                # To filter out anime that have no episodes.
                if typ in episodes:
                    if episodes[typ] == 0:
                        skip += 1

            if skip == 3:
                continue

            results.append(result)

        return [
            SearchResult(
                x["name"],
                f"{self.main_url}/anime/{x['_id']}",
                self.api_name,
                x["thumbnail"],
                x["season"]["year"]
            )
            for x in results
        ]

    def load(self, url: str) -> LoadResponse:
        html = self.session.get(url).text
        soup = BeautifulSoup(html, "html.parser")

        for script in soup.select("script"):
            if "window.__NUXT__" in str(script):
                show_data = dukpy.evaljs([
                    "const window = {}",
                    script.text,
                    "window.__NUXT__.fetch[0].show"
                ])

                return LoadResponse(
                    show_data["name"],
                    url,
                    self.api_name,
                    [
                        f"{self.main_url}/anime/{show_data['_id']}/episodes/sub/{x}"
                        for i in show_data["availableEpisodes"]
                        for x in range(show_data["availableEpisodes"][i])
                    ],
                    show_data["thumbnail"],
                    show_data["description"],
                    None,
                    show_data["airedStart"]["year"] if "year" in show_data["airedStart"] else None,
                    get_status(show_data["status"])
                )

        raise FileNotFoundError("The given anime was not found.")

    def load_links(self, url: str) -> typing.List[ExtractorLink]:
        raise NotImplementedError
