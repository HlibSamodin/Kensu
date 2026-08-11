# kensu-web

The website for [Kensu](https://github.com/HlibSamodin/Kensu) — an AI hallucination
detector. This is a static React site that explains the project, walks through
installing and running Kensu locally, and hosts a blog documenting how it's being built.

There's no backend here and no hosted demo — Kensu runs entirely on your own
machine with your own OpenAI API key, so this site is just the front door: an
install guide and a blog, nothing more.

## Stack

- React 19 + Vite
- Tailwind CSS v4
- React Router

## Development

```bash
npm install
npm run dev       # local dev server with HMR
npm run build     # production build
npm run preview   # preview the production build locally
npm run lint       # eslint
```

## Structure

- `src/pages/Install.jsx` — step-by-step guide to cloning, installing, and running Kensu locally
- `src/pages/Blog.jsx` / `BlogPost.jsx` — build log, added to as the project progresses
- `src/data/posts.js` — blog post content lives here
- `src/components/` — Nav, StepCard, VideoCard, CopyButton, Loader

## License

MIT — see the [main repo](https://github.com/HlibSamodin/Kensu) for details.