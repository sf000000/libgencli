# libgencli

A command-line interface for searching and downloading books from Library Genesis.

## Screenshots

```zsh
libgen --in title
```

![App Screenshot](https://i.postimg.cc/SsHqPcLT/image.png)
![App Screenshot](https://i.postimg.cc/3wMcz9zD/image.png)

## Installation

Install libgencli with pipx

```bash
pipx install libgencli
```

## Configuration

`~/.config/libgen/config.json`

```json
{
  "savePath": "~/books",
  "truncateTitles": true,
  "maxTitleLength": 50,
  "style": {
    "pointer": "fg:#f38ba8 bold",
    "highlighted": "fg:#490d90 bg:#cba6f7 bold",
    "question": "fg:#cdd6f4 bold",
    "text": "fg:#cdd6f4",
    "answer": "fg:#c6a0f6 bold"
  }
}
```
