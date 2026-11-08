# Blog

Posts are Markdown files in `_src/posts/`; `build.py` turns them into static HTML in this folder, which
GitHub Pages serves as-is. Commit both the `.md` sources and the generated HTML.

## Write a post

1. Create `_src/posts/YYYY-MM-DD-slug.md`:

   ```markdown
   ---
   title: My post title
   date: 2026-11-08
   summary: One or two sentences, shown on the index, in the feed and as the page description.
   tags: agentic AI, evaluation
   toc: true          # optional: "Contents" box from the ## and ### headings
   draft: true        # optional: skip this post when building
   ---

   Body in Markdown. Tables, footnotes, fenced code and raw HTML all work.
   ```

2. Preview with live rebuild: `python3 blog/build.py --serve`, then open http://localhost:8000/blog/
3. Build once: `python3 blog/build.py`, then commit and push.

The URL is `/blog/<slug>/`, where the slug is the file name without the date (or `slug:` in the front matter).

## Extras you can use in a post

- Images and figures: put files in `assets/<post>/` and reference them as `/blog/assets/<post>/file.svg`,
  inside `<figure><img ...><figcaption>...</figcaption></figure>`.
- Stat tiles: `<div class="stats"><div class="stat"><b>84%</b><span>label</span></div>...</div>`
- Callout box: `<div class="callout" markdown="1"> ...markdown... </div>`, or a plain `> blockquote`.

## Layout and settings

- `_src/templates/base.html`: the page shell (nav, footer, analytics).
- `assets/blog.css`: all styles. The accent colour is defined once at the top.
- `_src/site.json`: blog title, description, site URL and the newsletter settings.

## Email signup

The box at the top of the blog and under each post uses [Buttondown](https://buttondown.com). To turn it on,
create a Buttondown account, put the username in `_src/site.json` under
`newsletter.buttondown_username`, and rebuild. Until then the box shows "coming soon" with the RSS link and
does not post anywhere. Buttondown can also email subscribers automatically from `feed.xml` (RSS-to-email).
