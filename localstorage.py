import sys
import os
import pickle


class LocalStorage:
    root_path = "./pickle/"
    suffix = ".p"
    suffixes = {".p", ".pickle"}

    @staticmethod
    def get_path(filename):
        path = LocalStorage.root_path + filename
        if "." + path.split(".")[-1] not in LocalStorage.suffixes:
            path = path.rstrip(".") + LocalStorage.suffix
        return path

    @staticmethod
    def load(filename, encoding="utf-8"):
        path = LocalStorage.get_path(filename)
        with open(path, "rb") as f:
            try:
                data = pickle.load(f)
            except UnicodeDecodeError:
                os.remove(path)

                if "apicall" in filename.lower() or "bodyfetcher" in filename.lower():
                    data = {}
            except EOFError:
                os.remove(path)
                raise
            except pickle.UnpicklingError as e:
                if "pickle data was truncated" in str(e).lower():
                    os.remove(path)
                raise
        return data

    @staticmethod
    def save(filename, data, protocol=pickle.HIGHEST_PROTOCOL):
        path = LocalStorage.get_path(filename)
        with open(path, "wb") as f:
            pickle.dump(data, f, protocol=protocol)
