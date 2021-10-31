from anime_dl.providers.all_anime_provider import AllAnimeProvider

__providers__ = [
    AllAnimeProvider()
]


def get_provider_by_api_name(api_name):
    for provider in __providers__:
        if provider.api_name == api_name:
            return provider
    raise Exception("Provider not found.")
