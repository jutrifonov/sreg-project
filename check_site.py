"""Check generated local links, assets, anchors, and page structure."""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urljoin, urlparse, unquote

ROOT = Path(__file__).parent / 'docs'
ORIGIN = 'https://example.invalid'

class Page(HTMLParser):
    def __init__(self, text):
        super().__init__()
        self.ids, self.refs, self.tags, self.langs = set(), [], [], []
        self.feed(text)

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        self.tags.append((tag, attrs))
        if 'id' in attrs:
            assert attrs['id'] not in self.ids, f'Duplicate id: {attrs["id"]}'
            self.ids.add(attrs['id'])
        for name in ('href', 'src'):
            if name in attrs:
                self.refs.append(attrs[name])
        if 'data-lang' in attrs:
            self.langs.append(attrs['data-lang'])

pages = {p: Page(p.read_text()) for p in ROOT.rglob('*.html')}
checked = 0
for path, page in pages.items():
    rel = path.relative_to(ROOT).as_posix()
    route = '/' + rel.removesuffix('index.html') if rel.endswith('index.html') else '/' + rel
    for ref in page.refs:
        url = urlparse(urljoin(ORIGIN + route, ref))
        if url.netloc != 'example.invalid' or url.scheme not in ('http', 'https'):
            continue
        target = ROOT / unquote(url.path).lstrip('/')
        if target.is_dir():
            target /= 'index.html'
        assert target.is_file(), f'{path}: missing {ref} → {target}'
        if url.fragment:
            assert target in pages and unquote(url.fragment) in pages[target].ids, f'{path}: missing anchor {ref}'
        checked += 1
    assert sum(tag == 'main' for tag, attrs in page.tags) == 1, f'{path}: expected one main landmark'
home = pages[ROOT / 'index.html']
assert any(tag == 'body' and attrs.get('class') == 'home' for tag, attrs in home.tags)
assert set(home.langs) == {'r', 'stata', 'python'}
guide = pages[ROOT / 'get-started/index.html']
assert set(guide.langs) == {'r', 'stata', 'python'}
assert {'install', 'data', 'estimate', 'interpret', 'next'} <= guide.ids
empirical = pages[ROOT / 'empirical-example/index.html']
assert set(empirical.langs) == {'r', 'stata', 'python'}
assert {'setting', 'load', 'unadjusted', 'adjusted', 'report', 'sources'} <= empirical.ids
assert home.langs.count('r') == home.langs.count('stata') == home.langs.count('python')
print(f'Passed: {len(pages)} pages; {checked} local links/assets/anchors; three language variants.')
