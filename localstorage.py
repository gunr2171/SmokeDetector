import sys
import os
import pickle


class LocalStorage:
    root_path = "./pickle/"
    suffix = ".p"
    suffixes = {".p", ".pickle"}

    @staticmethod
    def get_path(filename, root=LocalStorage.root_path):
        path = root + filename
        if "." + path.split(".")[-1] not in LocalStorage.suffixes:
            path = path.rstrip(".") + LocalStorage.suffix
        return path

    @staticmethod
    def load(filename, encoding="utf-8", root=LocalStorage.root_path):
        path = LocalStorage.get_path(filename, root=root)
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
    def save(filename, data, protocol=pickle.HIGHEST_PROTOCOL, root=LocalStorage.root_path):
        path = LocalStorage.get_path(filename, root=root)
        with open(path, "wb") as f:
            pickle.dump(data, f, protocol=protocol)

    @staticmethod
    def exist(filename, root=LocalStorage.root_path):
        return os.path.isfile(LocalStorage.get_path(filename, root=root))

    @staticmethod
    def load_if_exist(filename, default=None, encoding="utf-8", root=LocalStorage.root_path):
        if not LocalStorage.exist(filename, root=root):
            return default
        try:
            return LocalStorage.load(filename, root=root)
        except (UnicodeDecodeError, EOFError, pickle.UnpicklingError):
            return default
