import whyKensuHero from '../assets/fingerprint-texture.png'
import curationHero from '../assets/typewriter-keys-texture.png'

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
   slug: 'scaling-the-question-bank',
   category: 'BUILD LOG',
   date: 'AUG 11, 2026',
   title: "Scaling the question bank, and why Kensu wont live on a server",
   excerpt: "946 questions sounded like a lot until I realised almost all of them were too easy to ever catch a model lying. Here's what I changed, and a decision I made about how Kensu actually gets run.",
   gradient: 'from-teal-600 via-teal-400 to-teal-200',
   content: [
     "Since ive started the project I think I was fine with the Question Banks. There are basically domains/ topics, math, science, history, geography, fake citations, in almost every single one of them there are under a thousand questions total. Then I actually looked at what was in there and realised almost every question was something like \"what is the capital of France\" or \"what is 2 plus 2\". A model like gpt-4o-mini gets those right basically every single time and every single run. Which sounds good until I  remembered what Kensu actually needed. It needed the model to sometimes question itself, sometimes guess, sometimes be wrong. If a question is so easy the model never hesitates, my signals (consistency, entropy, token probs) have nothing to disagree about in my opinion , this is because I spent a while perfecting them . No hesitation means no fingerprint to catch (read the previous of my posts for explanation).",
     "So the real work the past while was not code, it was going back through every domain and asking is this actually hard enough to matter which in my opinion is a genuine torture because i had to do it line by line. I pushed all five banks toward 5,000 questions total, but the number was never really the point for me because there is no point of having 9999 of the same questions and i actually had to make the spread good enough. History went from \"when did WW2 end\" to asking about specific succession years across entire dynasties. Math went from times tables to asking what the Cauchy-Schwarz inequality actually says. The fake-citations bank is honestly my favourite one now, it is not just those claims from conspirologist people that ai will refuse, some of it is boring and plausible on purpose (fake studies about desk plants and office noise levels) because those are the ones a model is actually likely to hallucinate because they just look real and give fake citation for. That is the whole category that matters most for this project if im honest, since a citation either exists or it doesnt, theres no in between.",
     "The other thing that got decided this week is smaller but I think more important long term. My brother asked me something I couldnt actually answer yet, how is someone supposed to run all of this. I had been assuming I would eventually wrap Kensu in a little API server for the website, and the dependencies for that were literally already sitting in the project unused since the start of the build. But once I actually thought it through, hosting it made no sense for what this is. Everyone has to bring their own OpenAI key anyway, so there is no world where I a, the one footing the bill, and running a server just to proxy someone's own key back to their own account is complexity for nothing. So it will be CLI only, clone it, run it on your own machine, that is it. Ripped the unused server dependencies back out too.But i still think after i run the thing will add one more page with examples of how it works",
     "I will be straight about where this leaves all of the projects things. The banks are built (but there is a bit left with the fake citations and I have checked them for accuracy and duplicates as carefully as I can by hand, but they have not been run against the real API yet, so I genuinely dont know yet how the label matching is going to hold up once real, messy model output comes back instead of the clean fake data ive had before I have been testing against. This is my next goal.",
   ],
   image: curationHero,
 },


,
  {
    slug: 'slug',
    category: 'category',
    date: 'AUG 2, 2026',
    title: 'title',
    excerpt: 'mini description here',
    gradient: 'from-purple-300 via-violet-200 to-purple-100',
  },
]