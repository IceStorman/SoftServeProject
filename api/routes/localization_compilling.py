import hashlib
import json
import subprocess
from pathlib import Path


class LocalizationCompiler:
    def __init__(self):
        self.__version_file = "translation_version.json"


    def compile_translations(self):
        self.__update_version(self.__pass_to_translation_folder())


    def __pass_to_translation_folder(self):
        BASE_DIR = Path(__file__).resolve().parent
        return BASE_DIR / "translations"


    def __update_version(self, TRANSLATIONS_DIR):
        current_version, saved_hash = self.__get_current_version()
        new_hash = self.__get_translation_files_hash()
        saved_hash = None

        if Path(self.__version_file).exists():
            with open(self.__version_file, "r") as f:
                saved_hash = json.load(f).get("hash")

        if new_hash != saved_hash:
            major, minor = map(int, current_version.split("."))
            new_version = f"{major}.{minor + 1}"
            with open(self.__version_file, "w") as f:
                json.dump({"version": new_version, "hash": new_hash}, f)

            subprocess.run(["pybabel", "compile", "-d", str(TRANSLATIONS_DIR)], check=True)


    def __get_translation_files_hash(self):
        hash_md5 = hashlib.md5()

        for po_file in self.__pass_to_translation_folder().rglob("*.po"):
            with open(po_file, "rb") as f:
                hash_md5.update(f.read())

        return hash_md5.hexdigest()


    def __get_current_version(self):
        if Path(self.__version_file).exists():
            with open(self.__version_file, "r") as f:
                data = json.load(f)

                return data.get("version"), data.get("hash")

        return "1.0", None