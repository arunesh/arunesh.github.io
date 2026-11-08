 I've added the NoProtocol article to the blog and built it. It's live locally at /blog/noprotocol/ and appears on the blog index and RSS feed. I haven't committed or pushed anything.

  What's in it:
  - The post: blog/_src/posts/2026-11-03-noprotocol.md. All sections, both tables, the inline links and the full Sources list come over word for word. I dropped the doc's title and byline line, because the blog
    template prints the title, date and tags itself.
  - The diagram: the export left out the doc's architecture diagram, so I rebuilt it as blog/assets/noprotocol/architecture.svg. It uses the same colours and fonts as the VideoIndex figures, and its caption is the
    doc's caption.
  - Front matter I wrote: a summary for the index and feed, tags (agentic AI, AI safety, security, multi-agent systems) and a table of contents. Edit any of these as you like.

  One decision for you: the post is dated Nov 3, 2026, the date on the doc, so it sits below the VideoIndex post (Nov 8). If you want it at the top, rename the file to 2026-11-08-noprotocol.md, change date: to
  match, and rebuild.

  To preview, run python3 blog/build.py --serve. I can commit and push when you're ready.

✻ Brewed for 2m 34s · done 1:20 PM

------------------------------------------------------------------------------------------------------------------------
 The blog is built and committed on a new branch, blog, which starts from the layout branch. The homepage now has Blog · Resume · GitHub links under your name, and the first post is about VideoIndex. Nothing is pushed yet. I
  checked each page in headless Chrome screenshots.

  Writing a post
  1. Add a Markdown file to blog/_src/posts/, e.g. 2026-11-08-videoindex.md, starting with a title, date, summary and tags.
  2. Run python3 blog/build.py --serve and open http://localhost:8000/blog/. It rebuilds each time you save.
  3. Commit the .md file together with the generated HTML.

  The build also makes an RSS feed at /blog/feed.xml. blog/README.md explains the extras you can use in a post (figures, stat boxes, callout boxes). GitHub Pages ignores the source folder, so only the finished pages go live.

  Design: light background, Inter for body text and JetBrains Mono for code. Cyan is the only accent: a thin gradient line across the top, a stripe on the signup box, link colour and tag labels.

  Email signup: I'd use Buttondown. It's simple, it's free up to 100 subscribers, and it can email new posts automatically from the RSS feed. The alternatives:
  - Substack: heavy branding and pulls readers onto its site.
  - Kit (ConvertKit) or Mailchimp: more marketing features than you need.
  - Your own Cloudflare Worker storing emails in D1: you own the list, but you'd have to build sending and unsubscribe yourself.

  The box is already at the top of the blog and under each post. To turn it on, put your Buttondown username in blog/_src/site.json and rebuild. Until then it shows "coming soon" with an RSS link and doesn't submit anywhere.

  The VideoIndex post (about 11 minutes to read) is drawn from the Oct 4 improvements report and the engineering doc. It covers:
  - the architecture, with a new diagram
  - the indexing pipeline, hybrid search, and the agent loop with its tools
  - how you measure, including noise and paired comparisons
  - results against Gemini's agentic video mode (84.1% vs 80.8% on LVBench, 78.1% vs 76.5% on MINERVA), with a chart
  - the six changes that worked, the ones that didn't, and lessons

  I left out hostnames, file paths, keys, branch names and anything about security incidents.

  Please check these before you publish:
  - Numbers and model names. They come straight from internal reports, so confirm you're happy making them public.
  - Live video. The "What's next" section mentions the live-video work, which currently lives in private repos. Cut that line if it isn't public yet.
  - "Open source" label. The project notes say the core VideoIndex repo went private in October, but your homepage still marks VideoIndex and CodeWalk as "(open source)".
------------------------------------------------------------------------------------------------------------------------
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


