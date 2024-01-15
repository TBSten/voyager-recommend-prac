import json
from typing import Any, cast

from anime import get_animes
from settings import init_index
from split_text import split_text
from to_vec import init_models, to_vec


def art_to_vectors(art: dict):
    if "label" not in art:
        return None
    words = split_text(art["label"])
    if len(words) == 0:
        return None
    vectors = [to_vec(word)[0] for word in words]
    return vectors


def update_index():
    init_models()
    index = init_index()

    # TODO ストップワード削除, 正規化(大文字->小文字, カタカナ->ひらがな, 漢字->ひらがなの読み)
    for data in get_animes():
        art_vecs = art_to_vectors(data)
        if art_vecs is None:
            continue
        ids = [index.add_item(vec) for vec in art_vecs]
        print(split_text(data["label"]), ids)

    index.save("output.voy")


update_index()
