from anime_dl.providers import get_provider_by_api_name

a = get_provider_by_api_name("AllAnimeProvider")
search_overlord_iii = a.search("overlord iii")[0]
load_overlord_iii = a.load(search_overlord_iii.url)

print(search_overlord_iii)
print(load_overlord_iii)

# Video scraping not done yet.
