# Can AI Really Learn a Language? The Kumi Experiments, in Plain English

*Jason Chua · Studio Ayumi · July 2026 · This is the no-jargon version. Every claim here is backed by public records — the experiments were registered in advance, run exactly once, logged in tamper-evident files, and re-checked by independent audit programs.*

## The question we set out to answer

When a chatbot seems to understand language, is it *actually* working out what things mean and how they combine — or is it doing a very good impression, like a parrot that has heard a million conversations?

You can't answer that by chatting with it, because chatbots have read basically the whole internet. Ask one anything in English and you can never be sure it isn't just remembering something similar it saw before. So we did what a scientist would do: we removed English entirely. We invented **brand-new languages that have never existed anywhere** — made of symbols like ▲ ● ■ and ⟳ ⇄ — and tested whether AI models could invent, learn, and *genuinely use* them. A made-up language can't be memorized in advance, because there was nothing to memorize.

The key thing we tested for is what makes language language: **building meaning from parts**. If you know what "blue" means and what "square" means, you can understand "blue square" even if you've never heard those words together. Linguists call this *compositionality*. It's the difference between knowing a phrasebook and knowing a language.

## Part one: two small AIs invent a language (and something strange happens)

We started with two small AI models — one made by Google, one by Alibaba — small enough to run on an ordinary laptop. We had them play a naming game: one describes coloured shapes with two-symbol "words" it makes up, the other guesses which shape is meant. They practise on three shapes. The fourth shape — the blue square — is **never mentioned by anyone**. Then, exactly once, the describer has to name it.

Here's the beautiful part. If the pair *really* built a language with parts — a symbol meaning blue, a symbol meaning square — then the right name for the never-discussed blue square is predictable. We wrote that prediction down, sealed, before the test. Then we watched.

Across dozens of runs, in every combination — Google's model talking to Alibaba's, the roles reversed, each model talking to a copy of itself — the same strange pattern appeared: **speakers sometimes invented real, rule-following languages and even produced the exactly-predicted word for the thing nobody had ever named. Listeners never once understood it.** Zero out of thirty-five. We even replaced the AI speaker with a perfect robotic teacher that never made a mistake — the listeners still failed. Talking in parts, it turns out, is easier than hearing in parts. Nobody predicted that; it fell out of the data.

One more discovery from this phase shaped everything after. One AI kept a private diary during the game (we let it take notes). For 120 rounds its diary insisted it was using a colour code — while the words it actually sent used no such code at all. It kept blaming its partner. The diary was sincere, consistent, and false. **From then on, our iron rule: what a model says about itself counts for nothing. Only what it does counts.**

## Part two: the big models — real skill, and a trap of our own making

Then we moved to the frontier: Anthropic's Claude (Sonnet) and Google's Gemini — the big models people actually use. Could they *learn* an invented language from examples alone?

At first, spectacularly yes. Shown a made-up naming system for eighteen objects, both models decoded names for held-out objects with 100% accuracy, where guessing would score about 6%. When we scrambled every hint of English out of the language, performance dropped but stayed far above chance — so familiarity with English was doing a lot of work, but not all of it.

Then we built a harder test with function words — symbols that *do* things rather than name things — and both models passed. And then the audit taught us a humbling lesson. When we examined *how* Gemini passed, we found it had learned a completely different rule than the one we intended — a clever mathematical formula that just happens to give the same answers on every question we were able to ask. Like a student who aces the exam using a method the teacher has never seen: did they learn what was taught? You literally cannot tell from the answers. Philosophers warned about this trap two hundred years ago. We fell into it, published that we fell into it, and designed the next experiment so the trap cannot exist.

## Part three: the final exam — and a twist ending

The last experiment, kumi13b, is the strictest language test we know how to build. A new alphabet of fifteen symbols. Two "action" symbols: one rotates a group of symbols, one swaps two of them. The maths behind it was chosen so that **every known way of faking it provably fails** — counting tricks, memorizing, copying similar examples, doing the steps in the wrong order: we wrote a program for each cheat and proved each one flunks. Blind luck? About 1 chance in 400 per run. Before running anything, we published our predictions and sealed the test. Two rival AI systems spent six rounds trying to find flaws in the design first; ten versions died in review before one survived.

The results were a shock in both directions.

**Gemini nearly ran the table.** Four perfect runs out of five — flawlessly executing symbol-programs it had never seen, at depths it had never seen — and in the fifth run its only "mistake" was running out of room to write mid-answer. We had predicted it would get roughly nothing. Afterwards, interviewed under our lie-detector protocol (it must state its rule, then be trapped into applying its own stated rule to a fresh case), it described the true grammar perfectly, five times out of five. And when asked, off the record, whether passing proves understanding, Gemini itself said no — comparing itself to a famous thought experiment about a man who translates Chinese perfectly using a rulebook without understanding a word.

**Claude failed every single run** — including questions using only material it had been directly shown. Reading its scratch-work, we watched it make very human mistakes: it decided early that the order of operations doesn't matter (it's everything), copied answers from examples that looked similar, and misquoted the examples to itself, then reasoned carefully from its own misquotes. Interviewed afterwards, it was gracious, thoughtful, philosophically eloquent — and described the rules of the language incorrectly while doing so. The model that failed told the best story. The model that aced it answered our "how did it feel?" question with a row of symbols.

## What it all means — and doesn't

Three findings we'd defend anywhere. **First:** at least one frontier AI can learn a genuinely novel rule system from a handful of examples and wield it perfectly on things it has never seen — under conditions where memorization and pattern-tricks are provably impossible. The strongest version of "it's just a parrot" does not survive this. **Second:** that ability is not general-purpose magic. Two comparable AIs, same test: one aced it, one collapsed — the difference wasn't knowledge but *discipline*: one checked its guesses against the evidence, the other fell in love with its first idea. **Third:** what AIs say about themselves is unreliable in both directions — confident narrators fail, and the one accurate self-reporter we found spoke mostly in symbols. Trust the behaviour, verify everything, and treat every explanation — theirs and ours — as a claim to be tested.

And honestly: even the perfect scores don't prove the AI "understands" the way you do. It might be — as Gemini itself suggested — a flawless rulebook-follower. Our test can't tell those apart. No test anyone has built can, yet. What we can say is narrower and solid: the behaviour is real, the shortcuts were ruled out, the predictions were sealed in advance, the coin-flip odds were 1-in-400, and every number can be re-derived from public, tamper-evident logs by code we didn't write.

*The experiments continue. The records are public at github.com/jasonkkchua-1/kumi-station-protocol. Verdict by arrival — the station never closes.* 🌻
