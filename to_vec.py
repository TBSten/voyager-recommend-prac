
import time
from os import path

import gensim

from anime import get_animes
from settings import DIMENSIONS
from split_text import split_text


class TestIterable:
    def __iter__(self):
        for art in get_animes():
            if "label" not in art:
                continue
            if not isinstance(art["label"], str):
                continue
            words = split_text(art["label"])
            for word in words:
                yield word


sentences = TestIterable()

FAST_TEXT_MODEL_PATH = "models/fast_text.model"
WORD2VEC_MODEL_PATH = "models/word2vec.model"


def init_fast_text_model():
    fast_text_model = gensim.models.FastText(
        sentences=sentences,
        vector_size=DIMENSIONS,
        window=5,
        min_count=1,
        workers=4,
    )
    fast_text_model.save(FAST_TEXT_MODEL_PATH)
    fast_text_model.train(
        sentences,
        total_examples=2,
        epochs=1,
    )
    return fast_text_model


def init_word2vec_model():
    word2vec_model = gensim.models.Word2Vec(
        sentences=sentences,
        vector_size=DIMENSIONS,
        window=5,
        min_count=1,
        workers=4,
    )
    word2vec_model.save(WORD2VEC_MODEL_PATH)
    word2vec_model.train(
        sentences,
        total_examples=2,
        epochs=1,
    )
    return word2vec_model


def load_fast_text_model():
    if not path.exists(FAST_TEXT_MODEL_PATH):
        return init_fast_text_model()
    return gensim.models.FastText.load(FAST_TEXT_MODEL_PATH)


def load_word2vec_model():
    if not path.exists(WORD2VEC_MODEL_PATH):
        return init_word2vec_model()
    return gensim.models.Word2Vec.load(WORD2VEC_MODEL_PATH)


def to_vec_by_model(text: str, model):
    if model is None:
        raise NotImplementedError("please init_model")
    if text not in model.wv:
        return None
    vector = model.wv[text]
    return vector


word2vec_model = None
fast_text_model = None


def init_models():
    global word2vec_model
    global fast_text_model
    word2vec_model = init_word2vec_model()
    fast_text_model = init_fast_text_model()
    return word2vec_model, fast_text_model


def load_models():
    global word2vec_model
    global fast_text_model
    word2vec_model = load_word2vec_model()
    fast_text_model = load_fast_text_model()
    return word2vec_model, fast_text_model


def to_vec(text: str):
    vec_word2vec = to_vec_by_model(text, word2vec_model)
    if vec_word2vec is None:
        vec_fast_text = to_vec_by_model(text, fast_text_model)
        return vec_fast_text, "fast_text"
    return vec_word2vec, "word2vec"


if __name__ == "__main__":
    def test_word(word: str):
        print("test:", word)
        t1 = time.time()
        vec = to_vec(word)
        t2 = time.time()
        print("  vec", vec)
        print("  time", int((t2-t1)*1_000_000) / 1_000, "ms")

    t1 = time.time()
    init_models()
    t2 = time.time()
    print("init models", t2-t1)

    test_word("な")
    test_word("ファンキー")
    test_word("仕草")
    test_word("NewWord")
