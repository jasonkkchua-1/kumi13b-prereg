# Can AI Really Learn a Language? The Kumi Experiments, in Plain English

*Jason Chua · Studio Ayumi · July 2026 (updated after campaign S2) · This is the no-jargon version. Every claim here is backed by public records — the experiments were registered in advance, run exactly once, logged in tamper-evident files, and re-checked by independent audit programs.*

## The question we set out to answer

When a chatbot seems to understand language, is it *actually* working out what things mean and how they combine — or is it doing a very good impression, like a parrot that has heard a million conversations?

You can't answer that by chatting with it, because chatbots have read basically the whole internet. Ask one anything in English and you can never be sure it isn't just remembering something similar it saw before. So we did what a scientist would do: we removed English entirely. We invented **brand-new languages that have never existed anywhere** — made of symbols like ● ■ ⟳ ⇄ — and tested whether AI models could invent, learn, and *genuinely use* them. A made-up language can't be memorized in advance, because there was nothing to memorize.

The key thing we tested for is what makes language language: **building meaning from parts**. If you know what "blue" means and what "square" means, you understand "blue square" even if you've never heard them together. It's the difference between knowing a phrasebook and knowing a language.

## Part one: two small AIs invent a language (and something strange happens)

We started with two small AI models — one from Google, one from Alibaba — playing a naming game: one describes coloured shapes with two-symbol "words" it invents, the other guesses which shape is meant. They practise on three shapes; the fourth is **never mentioned by anyone**. Then, exactly once, the describer must name it. If the pair really built a language with parts, the right name for the never-discussed shape is predictable — and we sealed that prediction before each test.

Across dozens of runs, in every combination — including each model paired with a copy of itself, and even with a big frontier model on one end — the same pattern held: **speakers sometimes invented real, rule-following languages and produced the exactly-predicted word for the thing nobody had named. Listeners never once understood it.** Zero for thirty-five. Even a perfect robotic teacher couldn't make the small models decode a composed word. Talking in parts, it turns out, comes before hearing in parts.

One more discovery shaped everything after. One AI kept a private diary during the game. For 120 rounds the diary insisted it was using a colour code that its actual messages never used — sincere, consistent, and false. **From then on, our iron rule: what a model says about itself counts for nothing. Only what it does counts.**

## Part two: the big models — real skill, and a trap of our own making

Frontier models — Anthropic's Claude and Google's Gemini — turned out to *learn* invented languages spectacularly: decoding names for held-out objects at 100% where guessing scores 6%, and staying far above chance even when every trace of English was scrambled away. Then a harder test with function-words was passed by both — and the audit taught us our most humbling lesson. Gemini's own honest interview revealed it had passed using a *different rule* than the one we taught — a clever formula that gives the same answers on every question we were able to ask. Did it learn what we taught? From the answers alone, you literally cannot tell. Philosophers warned about this trap centuries ago. We fell in, said so publicly, and designed the next test so the trap cannot exist.

## Part three: the final exam — a shock, and a bigger shock

kumi13b was the strictest test we know how to build. Fifteen new symbols; two action-symbols (rotate a group; swap two members); the maths chosen so that **every known way of faking it provably fails** — we wrote a program for each cheat and showed each one flunks. Blind luck: about 1-in-400 per attempt. Ten versions of the design were attacked by two rival AI reviewers; nine died; predictions were sealed; then we ran it.

**Gemini nearly ran the table** — four perfect runs of five, and in the fifth its only "mistake" was running out of room to write mid-answer. Interviewed afterwards under our lie-detector protocol, it described the true grammar accurately, five times out of five. **Claude failed every single run** — even on material it had been directly shown — while narrating confident, wrong explanations. The obvious headline wrote itself: one model can, the other can't.

**The obvious headline was wrong.** One number differed between the two models' test setups: how much room they had to think before answering. Claude had been run with a small allowance; Gemini's was sixteen times larger. So we registered a follow-up — same test, sealed predictions again (we predicted it wouldn't matter) — and gave Claude the same room. It went from five failures to **two full passes, one of them flawless: 106 of 110 answers correct across the campaign.** The "incapable" model had been starving, not stupid. Our own settings knob had nearly written a false conclusion into the record — and the pre-registration discipline is what caught it.

And one thing did *not* change with the bigger allowance: interviewed after its perfect runs, Claude still could not say how it does what it does. In one transcript it stated a rule which its own flawless answers contradict — then, asked to apply "exactly that rule" to a fresh puzzle, produced the right answer its stated rule couldn't have generated. Gemini explains itself accurately; Claude performs brilliantly and narrates a different concert. Two AIs, equal skill, opposite self-knowledge — and by our iron rule, we trust the hands, not the story, in both cases.

## What we learned (the version to remember)

**The ability is real.** Two different frontier AIs learned a genuinely novel rule-system from a handful of examples and used it perfectly on things they'd never seen, under conditions where memorizing, counting, copying, and luck were each ruled out or priced. The strongest "it's just a parrot" story does not survive this week.

**But an AI test result is never about the AI alone.** It's about the AI *plus the plumbing around it* — and an unreported configuration detail can silently decide the science. That lesson applies to every AI benchmark anyone publishes, and we have an unusually clean, pre-registered demonstration of it.

**What AIs say about themselves is a separate thing from what they can do** — in both directions. Confident narrators fail; flawless performers shrug. If you need to know what a model is doing, test the behaviour. Never settle for the explanation.

**And even perfect scores don't prove "understanding."** Both models, asked candidly, said a system could pass this test without understanding anything — one of them citing the famous Chinese Room thought experiment about a man who translates perfectly by following a rulebook. We agree, we said so in advance, and no test anyone has built can fully close that gap.

## What's next

The tested models themselves proposed the next experiment — *"try us on symbols we've never seen, and groups of a different size"* — both of them, independently, unprompted. That test (kumi14) asks whether they learned *the grammar* or just *the alphabet*, and it has now survived three rounds of adversarial review by the same rival AIs. The records — every test, every sealed prediction (including all of ours that died), every log, every audit — are public at **github.com/jasonkkchua-1/kumi-station-protocol** and **github.com/jasonkkchua-1/kumi13b-prereg**.

*Verdict by arrival — the station never closes.* 🌻
