import functools
import json


@functools.cache
def get_animes():
    result = []
    with open("data/anime-movie.json", "r", encoding="utf-8")as f:
        animes = json.load(f)
        for art in animes["@graph"]:
            if "label" not in art:
                continue
            result.append(art)
    with open("data/anime-regular.json", "r", encoding="utf-8")as f:
        animes = json.load(f)
        for art in animes["@graph"]:
            if "label" not in art:
                continue
            result.append(art)
    return result
