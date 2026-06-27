try:
    from .quality_dataset import build_dataset
except ImportError:
    from quality_dataset import build_dataset


if __name__ == "__main__":

    build_dataset()
