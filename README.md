# minni-image-converter

Multiprocessing tool for fast resize and compress photos.

## Develop

[Install Poetry](https://python-poetry.org/docs/#installation)

```sh
python3 -m venv .venv
. .venv/bin/activate
poetry install --with dev
```

## Usage

```sh
python3 -m minni_image_converter.cli --src source/dir --dst destination/dir
```

```sh
python3 -m minni_image_converter.cli --diff --src source/dir --dst destination/dir
```
