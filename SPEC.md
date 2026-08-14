# Personal Website Spec

## Philosophy

The web defaults right now are either corporate glass (gradients, glow, blur, dark mode, thin sans-serif, bento grids — everything looks like a SaaS dashboard) or punk maximalism (bold, loud, contrasty, deliberately ugly). Both are reactions to each other and both erase the person behind them.

This site takes a third path: things that feel like *objects*. Paper has texture. Books have weight. A card on a table casts a small shadow not because of a `box-shadow: 0 25px 50px` but because it physically sits above the surface. Warmth isn't a filter — it's what happens when materials absorb light instead of reflecting it.

Concretely this means:
- **Texture as information, not decoration.** Every texture needs a reason. A dot grid on an infinite canvas gives you a reference point for pan and zoom — that's functional. A generic paper texture slapped on a background is just a filter. The question is always: what does this texture *tell* the user? Shadows that show depth hierarchy. Not-quite-black instead of black. Not-quite-white instead of white. These are texture decisions too — they say "this is a surface, not a void." But none of it for its own sake.
- **Warmth over cool.** Tans, greens, cream — colors that exist in rooms with windows open. The palette should feel like afternoon light, not a monitor in a dark room.
- **Serif over sans.** Serif on the web used to mean "trying too hard" because screens couldn't render the details. On modern high-DPI displays, serif means *books*, *essays*, *someone sat down and wrote this*. IBM Plex Serif specifically because it stays readable even at small sizes.
- **Weight over weightlessness.** Elements should feel like they have mass. Cards sit on a surface. Transitions ease in and out like physical objects with momentum, not like layers fading in a compositor. Hover states should feel like picking something up, not like a CSS property changed.
- **Motion as physics, not decoration.** Animations communicate that something *moved*, not that something *appeared*. Ease curves that suggest mass. No gratuitous parallax, no scroll-triggered fly-ins. If something animates, it's because it went from here to there.

The Brian Eno quote on Lyra's pinned tweet gets at it: "whatever you now find weird, ugly, uncomfortable and nasty about a new medium will surely become its signature." The grain, the texture, the imperfection — these aren't bugs to be polished away. They're what make a thing feel *real* instead of *rendered*.

This is a personal site for someone who builds LLM research pipelines, trains tiny models on weird datasets, designs beat map generators from audio latents, produces neurofunk in Ableton, and builds custom tools because "it's fun and I wanna use it." Someone whose design philosophy across projects is "everything visible at once" with minimal nesting — who'd rather offload complexity to the user than hide it behind hand-holding. Someone who understands underlying systems rather than using abstractions.

The site should reflect that. Not unfinished, but honest about being a made thing. The same instinct that makes Lyra seed base models with "." just to see what the raw distribution looks like — that's the instinct for this site. Show the material. Trust the viewer.

## Design

- Card grid layout for projects (neal.fun style — each card is visually distinct, illustrated/themed to its project)
- Cards are rounded rectangles, varied sizes in a responsive grid
- Short intro/hero section at the top
- Clean, playful, not corporate

### Visual language
- Textured, classy, simple, warm, natural
- NOT glossy, NOT hypermodern/corporate, NOT purple-gradient-bento-box
- "Middle ground between punkness and corporate slop"
- "Minimalist but not sanitized"
- Feels like a blue light filter is always on — warm tones throughout

### Color
- Tans, sage greens, natural warm earth tones
- No purple gradients, no Facebook blue, no glow-and-dark
- Warm > cool. Think "blue light filter on" not "blue gray"

### Typography
- Serif, not sans — "serif web feels classy" on modern high-res screens
- IBM Plex Serif (chosen for readability at small sizes)
- No thin hero fonts

### Texture & detail
- Every texture must be *deliberate* — it exists because it communicates something, not because bare surfaces feel unfinished
- Not-quite-black (`#1a1a1a` not `#000`), not-quite-white (`#f5f0eb` not `#fff`) — removes the digital harshness, says "surface" not "void"
- Shadows should communicate depth hierarchy (what's on top of what), not just look nice
- No generic paper/noise textures as wallpaper — if grain exists, it has a job
- Example of texture done right: dot grid on an infinite canvas gives spatial reference for pan/zoom. It works *because* the context demands it. Same pattern on a static page would be meaningless

### Motion & interaction
- Transitions should feel physical — ease curves that imply mass and momentum
- Hover states should feel like lifting/picking up, not like opacity changed
- No gratuitous parallax, no scroll-triggered fly-ins
- If something animates, it's because it *moved*, not because it *appeared*
- Cards are objects on a surface, not layers in a compositor

## Content

- Brief intro — Lyra, 25, ML engineer / music producer in Eugene, OR. Optimistic irreverence, not corporate bio.
- Project cards (outlinks) — likely includes: base model research tools (looms, eval frameworks), audio/music tools (Beatformer, sample browsers), synthetic data pipelines, small model experiments
- Blog section or link
- Social links — X (@_lyraaaa_), Discord (lyraaaa_), GitHub, web-loom.org

## Technical

- Static site, hosted on GitHub Pages
- Plain HTML/CSS/JS (no framework, no build step)

## References

- neal.fun — card grid style, each project gets a unique visual card
  ![neal.fun screenshot](../claudebot/attachments/1467369806754873414_Screenshot_20260131_200315_Claude.jpg)
- Anthropic website — warm tones, natural illustration, serif text, good middle ground for the vibe
- Mistral AI website — pixel art, warm palette, playful but classy
- Design discussion (Discord, 01/25/2026) — Lyra's own words on the aesthetic direction
- Lyra's socials — @_lyraaaa_ on X, lyraaaa_ on Discord. Music AI tools, base models, data farming, Ableton. Brian Eno pinned tweet re: medium signatures
