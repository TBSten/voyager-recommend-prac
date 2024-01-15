from voyager import Index, Space, StorageDataType

DIMENSIONS = 200
INDEX_OUTPUT_PATH = "./output.voy"


def init_index():
    index = Index(
        space=Space.Euclidean,
        num_dimensions=DIMENSIONS,
    )
    index.save(INDEX_OUTPUT_PATH)
    return index


def get_index():
    index = Index.load(
        INDEX_OUTPUT_PATH,
    )
    return index
