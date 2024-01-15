
import base64
import time

from settings import get_index
from split_text import split_text
from to_vec import load_models, to_vec


def art_to_vectors(art: dict):
    if "label" not in art:
        return None
    words = split_text(art["label"])
    # print("split text", words)
    if len(words) == 0:
        return None
    vectors = [to_vec(word)[0] for word in words]
    return vectors


def search(q: str):
    print("search", q)
    start = time.time()
    vec = art_to_vectors({"label": q})
    neighbors, distances = index.query(vec, k=10, )
    end = time.time()
    print("time", end-start)
    print("vec", vec)
    print("neighbors", neighbors)
    print("distances", distances)
    threshold = 0.00008
    for i, dis in enumerate(distances[0]):
        nei = neighbors[0][i]
        print("item", nei, dis, -threshold <= dis and dis <= +threshold)


# init_models()
load_models()
index = get_index()

search("イナズマイレブ")
