import whyKensuHero from '../assets/fingerprint-texture.png'

export const posts = [
  {
    slug: 'why-kensu',
    category: 'INTRO',
    date: 'AUG 7, 2026',
    title: "Why am I building Kensu?",
    excerpt: "Every single LLM lies really confidently but they never actually tell you when the are lying. Kensu is me attempting at catching it before you actually do",
    gradient: 'from-orange-300 via-amber-200 to-orange-100',
    content: [
      "Go on ChatGpt website and ask an LLM something it doesn't know, and trust it usually wont tell you the answer which you expected. It will just answer anyway, but with the same confident tone / speaking manner it uses for things it actually gets right like math or coding. This gap between something \"sounding right\" and \"being right\" is the whole problem, and it is the reason why i created Kensu.",
      "The idea which I had in my head is pretty simple. Basically if the  model is guessing instead of confidently answering, it tends to leave some type fingerprint.  With one of the ways of finding if it lies or not I came up using the real life story with my dad so basically when I was speaking to my dad I asked him the same question multiple times because I couldnt hear him properly and every time I got a similar answer. After this moment something in my head clicked and I understood that I had to ask the same question five times and a confident model gives you roughly the same answer every single time. A model which will guess instead of answering will basically wander around like different phrasing, different facts, sometimes a completely different answers. That is the consistency signal (seems simple took me a while). Pair that with how \"sure\" the models own token probabilities look (entropy, logprobs in scientific way), and you start getting a picture of when it is actually confident versus when it is just performing confidence like it is on a stage.",
      "None of these signals are new and all of this stuff is grounded / used in real research (SelfCheckGPT, Kadavath and more), it is not something I invented from scratch. What Kensu does is just pulls three of those signals together, feeds them into a classifier, and tries to predict whether an answer which it got is a hallucination, using nothing but the models own behavior. No fact checking database or something like that, no external ground truth at inference time it is  just watching how the model acts.",
      "I will be honest about where this stands right now: the pipeline is built, tested, and I trust my own engineering. What I don't have yet is the real result. Everything so far has run on fake, not real placeholder data while I made sure the plumbing works, because the real OpenAI run costs actual money and I'd rather get the pipeline right once than debug it live with a meter running. The real data collection happens soon, and whatever the numbers say,  good or embarrassing , I will post them here.",
      "One thing I already know the model will surely struggle with are cases where the LLM is confidently, consistently wrong. If it says the same wrong answer every single time, all my signals go quiet. There will be literally no disagreement, no hesitation, nothing to catch. I built a specific evaluation just to measure how badly Kensu fails in exactly that case because when I was on holiday for a couple weeks I couldn't figure out the way to fix it, now instead of hiding it , I tell it to you straight. That felt more useful than only reporting the number that makes the project look good.",
      "More posts coming as I get the real results. For now, if you want to poke and try to improve at the code yourself, the install guides will be up soon although you have bring your own API key, I unfortunately don't have enough money to be paying for the whole internets curiosity.",
    ],
    image: whyKensuHero,
  },
  {
    slug: 'slug',
    category: 'category',
    date: 'AUG 2, 2026',
    title: 'title',
    excerpt: 'mini description here',
    gradient: 'from-teal-600 via-teal-400 to-teal-200',
  },
  {
    slug: 'slug',
    category: 'category',
    date: 'AUG 2, 2026',
    title: 'title',
    excerpt: 'mini description here',
    gradient: 'from-purple-300 via-violet-200 to-purple-100',
  },
]