⏺ I reorganized the main paragraph of index.html into four clear sections and committed it on a new branch, improve-main-layout. Fonts, blue links and the white background are unchanged. I checked the result
  with headless Chrome screenshots.

  What changed:
  - Projects: one block per project (NoProtocol, FastLLM, VideoIndex, CodeWalk), with a bold name, short grey tags (e.g. inference · kernels) and a one-line description. Key numbers are highlighted, like 1.5×
    faster than vLLM / SGLang. Past projects are now a muted line underneath.
  - Interests: a row of small labels (Agentic AI, LLMs, Distributed systems, …) followed by one sentence about scale.
  - Experience highlights: the Wi-Fi location work, the ultrasound API and open1x are now bullets instead of one long paragraph. The 2.5B+ users/day figure is highlighted.
  - Research: 30+ publications and 52 patents are shown as large numbers with their links, plus the line about ACM conferences.

  Other changes:
  - I moved the old separate "Open source projects" list into the VideoIndex and CodeWalk entries, so those links now appear only once.
  - I fixed a few typos ("specificiations", "knoweledge").
  - The two sections that both had id="other" now have their own ids.
  - Text width is limited to about 760px so lines are easier to read. On phones, the tags move onto their own line.

  All new styles are added at the end of res/css/style.css. index-old.html also uses that file, but it doesn't use any of the new classes, so it isn't affected. To preview, open index.html locally. I didn't push
  the branch.
------------------------------------------------------------------------------------------------------------------------
⏺ Fixed and committed on the crumble-animation branch.

  What was wrong. The first fall was scheduled as the initial hold plus the idle delay, not the initial hold alone. With the old 2.5 second idle delay that meant a 4 second first fall, which looked close enough to pass. Raising the idle delay to 20 seconds pushed the first fall
  to 21.5 seconds, which is what you saw.

  What changed. The first fall is now scheduled at 1.5 seconds on its own timer. Mouse movement during those first 1.5 seconds no longer postpones it, so the intro effect plays even if a visitor is moving the mouse as the page loads. After that, the 20 second idle rule applies
  as before.

  Verified in headless Chrome. With the mouse jiggling during the first second, the text was intact at 1.1 seconds and falling by 1.8 seconds. Mouse movement afterwards pulled the letters back, and they stayed intact through 4 more seconds of idle, as expected with the 20
  second delay.
------------------------------------------------------------------------------------------------------------------------
⏺ Done. The redesign is committed on the ui-refresh branch and not pushed.

  What changed

  - Markdown-driven page. content.md holds all the copy and front matter. Running python3 build.py renders it through res/template.html into index.html. The script has no dependencies, and --check fails if the built
    page is stale.
  - New design in res/css/main.css. Warm paper background with automatic dark mode, Newsreader serif for display and body, IBM Plex Mono for labels and link rows, one rust accent, numbered sections, a big-number stats
    strip, and a staggered load reveal that respects reduced motion. Verified in headless Chrome at desktop, tablet, and phone widths, in both light and dark.
  - Open source section at the end lists videoindex.org, codewalk.app, and safesecret.link with a "hobby" pill. A Writing section holds the Recall article and is where the blog will plug in.
  - CLAUDE.md captures the intent you gave, the design system, the Markdown conventions, the roadmap for blog and email signup, and the edit-build-commit workflow. The readme now points to it.

  Markdown conventions you can use in content.md

  - ## Heading starts a numbered section.
  - - [name](url) — description becomes a link row. Inline code in the description, like `hobby`, becomes a pill tag.
  - A one-row table becomes the stats strip.
  - The links: list in the front matter drives the top nav.

  Things to confirm

  - I wrote the safesecret.link description from its name alone. Please check it in content.md.
  - The original page said "papers (and award)", so I wrote "Papers and an award". Adjust if it was a best-paper award.
  - The Google Analytics tag is a Universal Analytics ID, which Google stopped processing in 2023. It is still in the front matter and can be swapped for a GA4 ID or removed.

  Next step is to open a PR from ui-refresh into master when you are happy with the copy. Preview locally with python3 -m http.server from the repo root.


