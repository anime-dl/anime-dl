import typing
import enum


class TvStatus(enum.Enum):
    ONGOING = enum.auto()
    COMPLETED = enum.auto()
    CANCELLED = enum.auto()


class DubStatus(enum.Enum):
    SUBBED = enum.auto()
    DUBBED = enum.auto()


class ExtractorLink(typing.NamedTuple):
    title: str
    url: str
    is_m3u8: bool = False
    headers: typing.Dict[str, str] = {}


class Episode(typing.NamedTuple):
    title: str
    url: str
    number: int
    type: DubStatus = DubStatus.SUBBED
    description: typing.Optional[str] = None
    date: typing.Optional[str] = None


class SearchResult(typing.NamedTuple):
    title: str
    url: str
    api_name: str
    poster_url: typing.Optional[str] = None
    year: typing.Optional[int] = None

    def __repr__(self) -> str:
        return f"<SearchResult title='{self.title}'{f', year={self.year}' if self.year else ''}, api={self.api_name}>"


class LoadResponse(typing.NamedTuple):
    title: str
    url: str
    api_name: str
    episodes: typing.List[Episode]
    poster_url: typing.Optional[str] = None
    description: typing.Optional[str] = None
    tags: typing.Optional[typing.List[str]] = None
    year: typing.Optional[int] = None
    tv_type: TvStatus = TvStatus.ONGOING

    def __repr__(self) -> str:
        return f"<LoadResponse title='{self.title}'{f', year={self.year}' if self.year else ''}, eps={len(self.episodes)}, api={self.api_name}>"


class Provider:
    api_name: str = "None"
    main_url: str = "None"

    def search(self, query: str) -> typing.List[SearchResult]:
        raise NotImplementedError

    def load(self, url: str) -> LoadResponse:
        raise NotImplementedError

    def load_links(self, url: str) -> typing.List[ExtractorLink]:
        raise NotImplementedError
