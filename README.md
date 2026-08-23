# lyra's website

static site — plain html/css/js, no build step. hosted on github pages.

## adding a blog post

1. drop `your-post.md` into `posts/`
2. add an entry to `posts/index.json`:

```json
{ "slug": "your-post", "title": "your post title", "date": "august 14, 2026" }
```

3. give it its clean url (`lyraaaa.dev/blog/your-post`):

```
mkdir blog/your-post
cp blog/_post.html blog/your-post/index.html
```

(the file is identical for every post — it reads the slug from its own url.)

4. regenerate the feed (email subscribers get notified off this): `python gen_feed.py`

posts render client-side with marked.js — front matter (`---` block) is stripped, first `# h1` becomes the page title, code blocks get syntax highlighting. images: put them in `posts/img/` and reference as `posts/img/foo.png` (root-relative).

## local preview

```
python -m http.server
```

then open http://localhost:8000 (fetch() needs a server, file:// won't work).

## notes

- `SPEC.md` — design direction for v2 (the fancy one with project cards)
- `_dev/` — mockups, critiques, drafts, card art. local only, not deployed.
