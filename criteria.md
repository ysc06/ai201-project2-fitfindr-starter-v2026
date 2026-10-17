# Acceptance criteria — FitFindr

Five criteria that say what "working" means for this agent, written in unit 3
**before** any results existed.

An acceptance criterion names a target: a number, a count, a rate, or something
a person could plainly observe. *"The agent handles errors"* is an opinion.
*"When search returns nothing, the agent stops before calling the second tool,
in 5 of 5 tries"* is a criterion.

Under each one, write a sentence or two on **why that target** and not a
stricter one. A reason that says something about your tools, your loop, or the
data earns credit; *"80% seemed reasonable"* does not.

> Missing your own targets next unit costs you nothing. Setting a target so
> easy you can't miss it does.

**Two are written for you. You write three.**

---

## 1. A matching query completes all three tools

Given a query that matches at least one listing, the agent completes all three
tool calls and returns a fit card — in at least 4 of 5 tries.

**Why this target:**
<!-- Why 4 of 5 and not 5 of 5? Something about your search, probably —
     "my search is a plain keyword match and some phrasings will miss" is a
     real answer. -->
My search is a plain keyword match: it splits the query and the listing text on
spaces and counts exact word overlaps. Some phrasings will miss even when a
matching item exists — "t-shirt" never matches "tee", and a word with
punctuation stuck to it in the listing ("graphic.") doesn't count as "graphic".
This path also makes two model calls, so one bad response can break a run. One
miss in five allows for that; more than one means the search or parsing needs work.

---

## 2. An impossible query stops before the second tool

Given a query that matches no listings, the agent stops before calling
`suggest_outfit` and returns a message naming what to change — 5 of 5 tries.

**Why this target:**
<!-- Why is 5 of 5 reasonable here when criterion 1 isn't? What's different
     about this path? -->
Nothing on this path involves the model. `parse_query` and `search_listings` are
plain Python, so the same query gives the same empty list every time, and
`if not session["search_results"]` returns before `suggest_outfit` is ever
reached. The message is built from the fields the user actually set, so it
always names something to change. With no randomness, any miss is a bug in my
branch, not variance, so 5 of 5 is the only fair target.

---

## 3. The item search found is the item suggest_outfit received

<!-- YOU WRITE THIS ONE.

     How would you know that the item your search found is the same item the
     next tool received? Name something countable or observable.

     This is the criterion people find hardest, because state failure doesn't
     look like state failure — it looks like a tool problem. Something that
     compares session["selected_item"] against what actually reached
     suggest_outfit is the shape you're after. -->

Given a query that matches at least one listing, the listing `id` in `session["selected_item"]` is the same as `session["search_results"][0]["id"]` and the same as the `new_item` id shown in the trace's `suggest_outfit` input line — 5 of 5 tries. 


**Why this target:**
FitFindr's whole goal is pairing the item found with the user's wardrobe, so the outfit is worthless if it's built around a different item. The handoff from `search_listings` to `suggest_outfit` doesn't involve the model — so there is no randomness to allow for. A single mismatch means my loop passed the wrong variable, which is a bug, so the target is 5 out of 5 rather than 4 of 5. 



---

## 4. The fit card names the item, price and platform, at caption length

<!-- YOU WRITE THIS ONE.

     The fit card calls a model, so the same input can produce different words
     each time. That's not a bug — it's the nature of the tool. So what would
     make it acceptable?

     Think about what you'd actually be unhappy to see. A caption that never
     mentions the price? Two different items producing the same opening
     sentence? A card longer than a caption anyone would post? Any of those can
     be turned into a number. -->

For 5 different items, each card mentions the item, its price, and its platform, and is 2-4 sentences long — at least 4 of 5 tries. 

**Why this target:**
These rules live in a prompt, and the model doesn't always follow the prompt exactly — at temperature 0.9, captions vary on purpose. But the price and platform are handed to the model directly in the listing dict, so more than one miss would mean my prompt isn't clear enough.  



---

## 5. suggest_outfit only uses items the user actually has 

<!-- YOU WRITE THIS ONE TOO.

     Pick something you actually care about getting right. Speed, the empty
     wardrobe path, what happens when the model can't be reached, whether the
     search respects a price ceiling — anything, as long as it names a number
     or an observable outcome. -->

Using the example wardrobe on 5 matching queries, every piece the outfit suggestion presents is from the user's `wardrobe["items"]` — no invented pieces — in at least 4 of 5 tries. 


**Why this target:**
The prompt lists the wardrobe items and asks the model to only use those, but nothing in the code enforces it. At temperature 0.9, there is some randomness. It can complete an outfit that sounds right but isn't there in the wardrobe. So I allow one miss — more than one miss means my prompt isn't constraining it enough. 


---

<!-- ─────────────────────────────────────────────────────────────────────────
     UNIT 4 — read this before you change anything above.

     If a criterion turns out to be BROKEN rather than merely unmet, you can
     revise it, and that earns credit. But never delete or edit the original
     line. Add the revision underneath it, like this:

         ## 4. Something about the fit card

         The fit card is different every time.

         **Why this target:** ...

         > **Revised in unit 4:** For 5 different items, the 5 fit cards share
         > no opening sentence.
         >
         > **Why revised:** "different" wasn't checkable — two cards that
         > differed by one word still counted. The new version is something I
         > can actually score.

     That's a revision because the criterion couldn't be MEASURED.

     Lowering a target because you missed it is not a revision, and it costs
     you the point:

         ✗ "I said the empty search stops it 5 of 5 times, but I got 3 of 5,
            so 3 of 5 is more realistic."

     A number you missed stays where it is, gets diagnosed, and gets a fix
     attempted. That's where the points are.
     ───────────────────────────────────────────────────────────────────────── -->
