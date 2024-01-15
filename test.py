import json
from typing import Any, cast

from anime import get_animes
from settings import get_index, init_index
from split_text import split_text
from to_vec import init_models, to_vec


def art_to_vectors(art: dict):
    if "label" not in art:
        return None
    words = split_text(art["label"])
    # print("split text", words)
    if len(words) == 0:
        return None
    vectors = [to_vec(word)[0] for word in words]
    # print("vectors", vectors)
    # sum_vecs = cast(Any, vectors[0])
    # sum_vecs.flags.writeable = True
    # for vec in vectors[1:]:
    #     sum_vecs += vec
    # # print(sum_vecs)
    # return sum_vecs
    return vectors


def update_index():
    init_models()
    index = init_index()

    # TODO ストップワード削除, 正規化(大文字->小文字, カタカナ->ひらがな, 漢字->ひらがなの読み)
    for art in get_animes():
        art_vecs = art_to_vectors(art)
        if art_vecs is None:
            continue
        ids = [index.add_item(vec) for vec in art_vecs]
        print(art["label"], ids)

    # for vec in vectors:
    #     print("vec", len(vec), vec)
    #     id = index.add_item(vec)
    #     print(id, )
    # index.add_items(vectors)

    index.save("output.voy")


def search():
    q = "はいきゅー"
    print("search", q)
    init_models()
    index = get_index()
    vec = art_to_vectors({"label": q})
    print("vec", vec)
    neighbors, distances = index.query(vec, k=10, query_ef=0.3)
    print("neighbors", neighbors)
    print("distances", distances)


# init_models()
# art_to_vectors({"label": "鬼滅の刃"})


# update_index()
search()
