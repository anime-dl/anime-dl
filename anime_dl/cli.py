from anime_dl.providers import get_provider_by_api_name

a = get_provider_by_api_name("TenshiMoe")
search = a.search("shingeki")[0]
load = a.load(search.url)
load_links = a.load_links(load.episodes[0].url)
print(load_links)
