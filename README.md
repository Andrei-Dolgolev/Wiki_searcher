# WikiRacer

Foobar is a Python library for dealing with word pluralization.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install foobar.

```bash
pip install -r requirements.txt
```

## Usage

```python
import Racer

start = 'https://en.wikipedia.org/wiki/Battle_of_Cr%C3%A9cy'
end = 'https://en.wikipedia.org/wiki/Wehrmacht'

searcher = Racer(start,end,False)
searcher.search_from_start_to_end()

```

## Roadmap

- Add search to meet each other
- Add search via diferent languages level
- Add regontiton of article signature 



## License
[MIT](https://choosealicense.com/licenses/mit/)
