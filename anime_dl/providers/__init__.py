from anime_dl.providers.all_anime_provider import AllAnimeProvider

from providers.tenshi_moe_provider import TenshiMoeProvider

__providers__ = [
    AllAnimeProvider(),
    TenshiMoeProvider()
]


def get_provider_by_api_name(api_name):
    for provider in __providers__:
        if provider.api_name == api_name:
            return provider
    raise Exception("Provider not found.")
