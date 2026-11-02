# FitFindr

> ### 👋 Start here
>
> **New to this repo? Read [RUNNING.md](RUNNING.md) first** — setup, every
> command, and what to do when something breaks.
>
> Once `python test.py` passes:
>
> ```bash
> python app.py listings --full -n 6      # read the data (Milestone 1)
> python app.py fields                    # what you can filter on
> python app.py ask 'vintage graphic tee under $30'
> ```
>
> All three tools are stubs, so that last command will do nothing useful yet.
> That's the starting position.
>
> **The rest of this file is your submission.** Fill it in as you go.

---

<!-- ─────────────────────────────────────────────────────────────────────────
     HOW TO USE THIS FILE

     This is your submission. Fill each section in as you finish the milestone
     it belongs to — don't leave it all to the end.

     Unit 3 asks for the first five sections. Unit 4 adds the five below them.
     Leave the unit 4 sections alone until then; they're here so you know
     what's coming.

     Everything is pasted as TEXT. No screenshots, no images, no video links.
     A typed block of output gets full credit; a picture of the same output
     gets none.
     ───────────────────────────────────────────────────────────────────────── -->

<!-- ═══════════════════════ UNIT 3 — THE BUILD ═══════════════════════ -->

## What This Does

<!-- Three or four sentences: what a user asks for, and what they get back. -->

FitFindr takes a plain-English request for a thrifted item, like "vintage graphic tee under $30" or "black jeans size M". It searches 40 secondhand listings from Depop, ThredUp and Poshmark for the best keyword match within the user's price and size, then suggests one or two outfits that pair that item with pieces already in the user's wardrobe. It finishes with a short, post-style caption for the find. If nothing matches, it stops early and tells the user which filter to loosen.


---

## Tool Inventory

<!-- Four lines per tool. This is worth 2 points and it's the single most
     common place students lose them.

     "Returns a list" earns NOTHING. The description has to say what is IN
     the list.

     The empty case isn't optional either — it's the thing your loop branches
     on, and if you don't decide it here you'll discover it as a crash in
     Milestone 5. -->
# Function contract 
### `search_listings`

- **What it does:** Filters listings.json by price ceiling and size (when the user gives them), scores the remaining items by keyword overlap with the description, and returns them highest score first.
- **Inputs:** `description` (str) — keywords like "vintage graphic tee"; `size` (str | None) — case-insensitive, matches when it equals one of the listing's size tokens split on "/" and spaces (so "M" matches "S/M" but not "XL", and "S" doesn't match "US 9"); None skips size filtering; `max_price` (float | None) — inclusive ceiling, None skips price filtering.
- **Returns:** A list of up to `config.SEARCH_RESULT_LIMIT` (currently 10) listing dicts, best match first, each with id, title, description, category, style_tags (list), size, condition, price (float), colors (list), brand (str or None), platform.
- **When it has nothing:** Returns an empty list `[]` — not None, not a string, not an exception.

### `suggest_outfit`

- **What it does:** Calls the model via `generate()` to suggest one or two outfits that pair the thrifted item with pieces from the user's wardrobe.
- **Inputs:** `new_item` (dict) — a listing dict from search_listings, the item the user is considering; `wardrobe` (dict) — has an `items` key holding a list of wardrobe item dicts, each with id, name, category, colors (list), style_tags (list), notes (str or None). The list may be empty.
- **Returns:** A non-empty string describing one or two outfits, each naming specific wardrobe pieces by their `name` alongside the new item.
- **When it has nothing:** If `wardrobe["items"]` is empty, returns a non-empty string of general styling advice for the item — never `""`, never an exception.

### `create_fit_card`

- **What it does:** Calls the model via `generate()` to write a short, post-style caption about the find (not a product description).
- **Inputs:** `outfit` (str) — the outfit suggestion string from `suggest_outfit()`; `new_item` (dict) — the listing dict for the selected item from `search_listings()`.
- **Returns:** A two-to-four sentence caption string that mentions the item's title, price, and platform once each and names the specific vibe; wording varies between runs.
- **When it has nothing:** If `outfit` is empty or whitespace-only, skips the model call and returns the string "Can't write a fit card without an outfit suggestion." — never an exception.

---

## Planning Loop

<!-- Your branch rule, stated as a rule — the condition AND both paths — plus
     the file and function that holds it.

     Like this:
       "If search_listings returns an empty list, put a message in the session
        and stop. Otherwise take the first result and go to suggest_outfit."
        — agent.py::run_agent

     The grader checks your code against what you claim here, so the file and
     function have to be real. -->

**Branch rule:** If `search_listings` returns an empty list, put a message in `session["error"]` telling the user what to change (e.g. raise the max price, drop the size, or use broader keywords) and return the session without calling `suggest_outfit`. Otherwise, put the first result in `session["selected_item"]` and go to `suggest_outfit`.

**Where it lives:** `agent.py::run_agent`

**How the query is parsed:** String splitting, in `agent.py::parse_query`. The query is lowercased, commas become spaces, and it's split into words. A word starting with `$` becomes `max_price` (float); the word after `size` becomes `size`; every other word is kept for `description` unless it's in `STOPWORDS` (filler like "looking", "for", "a", and price words like "under"). Anything not given stays `None`.

**What moves through the session:** `query` → `parsed` (description, size, max_price) → `search_results` (list of listing dicts) → branch: empty sets `error` and returns; otherwise → `selected_item` (`search_results[0]`) → `outfit_suggestion` (from `suggest_outfit(selected_item, wardrobe)`) → `fit_card` (from `create_fit_card(outfit_suggestion, selected_item)`). Each tool reads its inputs back out of the session, not from the previous call's return value.

---

## Sample Run

<!-- Two things go here.

     1. One FULL query and its output, pasted as text.
     2. Your three per-tool terminal tests — the command and what it printed. -->

**One full query**

```
$ python app.py ask 'looking for a vintage graphic tee under $30'

  Found:    Y2K Baby Tee — Butterfly Print — $18.0 on depop

  Outfit:   **Outfit 1: Y2K Casual Streetwear**
Pair the Y2K Baby Tee — Butterfly Print with the Baggy straight-leg jeans, dark wash, layered underneath the Black cropped zip hoodie. Finish the look with the Chunky white sneakers and the Black crossbody bag.

**Outfit 2: Edgy Contrast**
Pair the Y2K Baby Tee — Butterfly Print with the Wide-leg khaki trousers, styled with the Brown leather belt. Throw on the Vintage black denim jacket and ground the outfit with the Black combat boots.

  Fit card: Just scored this Y2K Baby Tee — Butterfly Print on depop for $18.00 and I am so obsessed with the white, pink, and purple colorway! I'm totally styling it for a Y2K casual streetwear vibe layered under a black cropped zip hoodie with baggy dark wash jeans and chunky white sneakers. Such a nostalgic little find.
```

**The same command on a query that matches nothing** — it stops after the search, with no outfit and no fit card:

```
$ python app.py ask 'designer ballgown size XXS under $5'

  No listings matched. Try to raise your max price above $5.00, or drop the size filter (xxs), or use broader keywords than "designer ballgown".

0 model calls this session
```

**The three tools, tested one at a time**

`search_listings` — a match, then nothing:

```
$ python -c "from tools import search_listings; print(search_listings('graphic tee', max_price=30))"
[{'id': 'lst_002', 'title': 'Y2K Baby Tee — Butterfly Print', 'description': 'Super cute early 2000s baby tee with butterfly graphic. Fitted crop length. Tag says medium but fits like a small.', 'category': 'tops', 'style_tags': ['y2k', 'vintage', 'graphic tee', 'cottagecore'], 'size': 'S/M', 'condition': 'excellent', 'price': 18.0, 'colors': ['white', 'pink', 'purple'], 'brand': None, 'platform': 'depop'}, {'id': 'lst_006', 'title': 'Graphic Tee — 2003 Tour Bootleg Style', 'description': 'Vintage-style bootleg tee with faded graphic. Slightly boxy fit. 100% cotton, soft and worn-in.', 'category': 'tops', 'style_tags': ['graphic tee', 'vintage', 'grunge', 'streetwear', 'band tee'], 'size': 'L', 'condition': 'good', 'price': 24.0, 'colors': ['black'], 'brand': None, 'platform': 'depop'}, {'id': 'lst_017', 'title': 'Mesh Long-Sleeve Top — Black', 'description': 'Sheer black mesh long-sleeve. Great for layering under a graphic tee or over a bralette. Stretchy material, fits true to size.', 'category': 'tops', 'style_tags': ['y2k', 'grunge', 'goth', 'layering'], 'size': 'S/M', 'condition': 'excellent', 'price': 15.0, 'colors': ['black'], 'brand': None, 'platform': 'depop'}, {'id': 'lst_033', 'title': 'Vintage Band Tee — Faded Grey', 'description': 'Faded grey band-style tee with distressed graphic. Crew neck. Fits boxy. Well-loved but no holes or major damage.', 'category': 'tops', 'style_tags': ['vintage', 'grunge', 'band tee', 'graphic tee', 'streetwear'], 'size': 'L', 'condition': 'fair', 'price': 19.0, 'colors': ['grey', 'charcoal'], 'brand': None, 'platform': 'depop'}, {'id': 'lst_015', 'title': 'Vintage Graphic Hoodie — Faded Black', 'description': 'Faded black pullover hoodie with barely-visible vintage graphic on the chest. Cozy interior. Some pilling but adds to the worn-in look.','category': 'tops', 'style_tags': ['vintage', 'grunge', 'graphic', 'streetwear'], 'size': 'L', 'condition': 'fair', 'price': 26.0, 'colors': ['black', 'charcoal'], 'brand': None, 'platform': 'depop'}]

$ python -c "from tools import search_listings; print(search_listings('zzzz'))"
[]
```

`suggest_outfit` — example wardrobe, then empty wardrobe:

```
$ python -c "from tools import suggest_outfit; from utils.data_loader import get_example_wardrobe, load_listings; print(suggest_outfit(load_listings()[0], get_example_wardrobe()))"
Here are two ways to style your Vintage Levi's 501 Jeans:

**Outfit 1: Casual Streetwear**
*   **Top:** Oversized grey crewneck sweatshirt
*   **Shoes:** Chunky white sneakers
*   **Accessory:** Black crossbody bag

**Outfit 2: Edgy & Cropped**
*   **Top:** White ribbed tank top
*   **Outerwear:** Vintage black denim jacket
*   **Shoes:** Black combat boots
*   **Accessory:** Brown leather belt

$ python -c "from tools import suggest_outfit; from utils.data_loader import get_empty_wardrobe, load_listings; print(suggest_outfit(load_listings()[0], get_empty_wardrobe()))"
Vintage Levi's 501 jeans in a medium wash are the ultimate thrift store staple—they work with almost anything and just get better with age. Here are two ways to style them:

**Outfit Idea 1: Classic Off-Duty Casual**
Pair the vintage Levi's with a crisp white cotton t-shirt tucked in casually at the front. Layer an oversized black leather biker jacket over the top for some texture contrast. Finish the look with a pair of retro leather sneakers and a minimalist canvas tote bag.

**Outfit Idea 2: Elevated Streetwear**
Style the medium wash denim with an oversized, boxy button-down shirt in blue-and-white stripes, worn open over a ribbed white tank top. Add a chunky black leather belt with a statement silver buckle to cinch the waist, and step into some classic chunky loafers. Accessorize with a silver chain necklace to tie the metallic details together.
```

`create_fit_card` — an outfit, then a blank one:

```
$ python -c "from tools import create_fit_card; from utils.data_loader import load_listings; print(create_fit_card('Pair with chunky white sneakers and an oversized grey sweatshirt.', load_listings()[0]))"
Found the absolute holy grail on depop today—these Vintage Levi's 501 Jeans in the dreamiest medium wash for just $38.00! Can't wait to live in them with my chunky white sneakers and an oversized grey sweatshirt for the ultimate cozy streetwear fit. Honestly, nothing beats that broken-in indigo denim feeling.

$ python -c "from tools import create_fit_card; from utils.data_loader import load_listings; print(repr(create_fit_card('   ', load_listings()[0])))"
"Can't write a fit card without an outfit suggestion."
```

---

## How I Used AI

<!-- Two specific moments. What you asked, what came back, what you changed.

     "I used Claude to help me code" is not enough.

     "I gave Claude my search_listings spec. It returned None on no match
     instead of an empty list, so I changed it" is the level we want. -->

**Moment 1**

- *What I asked for:* I asked Claude to check my first draft of the `search_listings` Tool Inventory entry against the code.
- *What came back:* My draft said the tool returns the string "sorry, there is no match." when nothing matches. Claude pointed out that the docstring in `tools.py` requires an empty list, and that a non-empty string is truthy, so `if not results` in my loop would never catch it and `results[0]` would hand the character `"s"` to `suggest_outfit`.
- *What I changed:* I changed the empty case to `[]` in both the README and the code, and moved the user-facing "no match" message into `run_agent`, which writes it to `session["error"]`. The tool returns the signal and the loop writes the message.

**Moment 2**

- *What I asked for:* I asked Claude to write `parse_query` for `agent.py`.
- *What came back:* A regex version that worked on all my test queries, but I couldn't read the patterns well enough to debug them.
- *What I changed:* I asked for a string-splitting version instead and typed it in myself. I left out the `i += 1` that skips the word after `size`, so "designer ballgown size XXS" parsed to a description of "designer ballgown xxs". I tested it, found the size leaking into the description, and added the line back.

<!-- ═══════════════════════ UNIT 4 — THE TEST ═══════════════════════

     Don't fill these in during unit 3.
     ═══════════════════════════════════════════════════════════════════ -->

---

## Run Log — Before

<!-- Five criteria, five tries each, in this exact format.

     Five, because your criteria are written out of five. Mark each try PASS
     or FAIL, count the passes, and read that count against your target — a
     row targeting 4 of 5 with three PASS cells is MISSED (3/5).

     `python run_eval.py --label before` runs everything and writes the table
     into results/. Paste it here and fill in the verdicts. -->

| Criterion | Target | Try 1 | Try 2 | Try 3 | Try 4 | Try 5 | Verdict |
|---|---|---|---|---|---|---|---|
| 1. A matching query completes all three tools | 4 of 5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |
| 2. An impossible query stops before the second tool | 5 of 5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |
| 3. The item search found is the item suggest_outfit received | 5 of 5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |
| 4. The fit card names the item, price and platform, at caption length | 4 of 5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |
| 5. suggest_outfit only uses items the user actually has | 4 of 5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |

Source: `results/run_2026-11-01_2346_before.md`, from `run_eval.py --label before`
(caching off, temperature 0.9).

**How the rows were scored.**

- **1** — PASS if the run returned a fit card without stopping early.
- **2** — PASS if the run stopped with a message naming what to change, and
  the trace has no `suggest_outfit` step. All five tries stopped at step [2].
- **3** — PASS if the id in trace step [2]'s note (`search_results[0]`) matches
  the id on step [3]'s input line (what `suggest_outfit` got), and
  `selected_item` is the same listing. All five: `lst_004` → `lst_004`, query
  `90s track jacket in size M` (3 results, so a wrong index would show).
- **4 and 5** — each criterion says "5 different items", so each has five
  scenarios, one item apiece, every one run five times. Try *k* is round *k*:
  each of the five items run once. A try is PASS only if all five items pass.

Per-item detail for 4 and 5 (passes out of 5 runs):

| Criterion | Item | Price | Platform | Passes |
|---|---|---|---|---|
| 4 | lst_022 90s Leather Bomber | $75 | depop | 5/5 |
| 4 | lst_018 Vintage Linen Blazer | $38 | thredUp | 5/5 |
| 4 | lst_028 Suede Chelsea Boots | $44 | poshmark | 5/5 |
| 4 | lst_011 Low-Rise Cargo Pants | $27 | poshmark | 5/5 |
| 4 | lst_014 Leather Belt | $12 | thredUp | 5/5 |
| 5 | lst_013 90s Silk Slip Dress | $30 | depop | 5/5 |
| 5 | lst_009 Platform Mary Janes | $55 | depop | 5/5 |
| 5 | lst_023 Crochet Halter Top | $22 | depop | 5/5 |
| 5 | lst_036 Velvet Blazer | $52 | depop | 5/5 |
| 5 | lst_017 Mesh Long-Sleeve Top | $15 | depop | 5/5 |

- **4** — a card passes if it names the item, gives the right price ($75 or
  $75.00 both count), names the platform, and is 2–4 sentences. Every card
  was 2 or 3 sentences. One judgment call: linen blazer try 5 said "cream
  linen blazer" instead of the full title "Vintage Linen Blazer — Cream". I
  counted it as naming the item, since the criterion says "mentions the
  item", not "quotes the title".
- **5** — a suggestion fails if it presents any piece that isn't in
  `wardrobe["items"]` and isn't the thrifted item itself, including optional
  extras like "add some jewelry". The five items were picked because their
  usual pairings are missing from the example wardrobe (no skirts, shorts,
  shirts, jewelry, sandals or socks). None of the 25 invented a piece. Closest
  call: slip dress try 1 says the sweatshirt over the dress gives "a
  skirt-and-sweater effect" — that describes the look, it doesn't add a skirt.

**Real output from one try**, pasted as text, naming the file and function
that produced it.

Every block below is copied from `results/run_2026-11-01_2346_before.md`,
written by `run_eval.py::write_report` from what `run_eval.py::run_once`
captured when it called `agent.py::run_agent`. Within a run, the trace lines
come from the `trace.step()` calls in `agent.py::run_agent`, the outfit from
`tools.py::suggest_outfit`, and the fit card from `tools.py::create_fit_card`.

**Criterion 1 — try 1.** Query `vintage graphic tee under $30`, example
wardrobe. All three tools ran and a fit card came back
(`agent.py::run_agent` → `tools.py::suggest_outfit` → `tools.py::create_fit_card`):

```
- stopped early: no
- selected_item: Y2K Baby Tee — Butterfly Print ($18.0, depop)
- search_results: 10

Outfit suggestion:
**Outfit 1: Casual Y2K Streetwear**
*   Y2K Baby Tee — Butterfly Print
*   Baggy straight-leg jeans, dark wash
*   Vintage black denim jacket
*   Chunky white sneakers
*   Black crossbody bag

**Outfit 2: Elevated Contrast**
*   Y2K Baby Tee — Butterfly Print
*   Wide-leg khaki trousers
*   Brown leather belt
*   Black combat boots

Fit card:
Found the absolute cutest Y2K Baby Tee — Butterfly Print on depop for just $18.00 and I am obsessed! The pink and purple butterfly graphics give major early 2000s mall-goth vibes, especially paired with my baggy dark wash jeans and a vintage black denim jacket. Can't wait to style it with wide-leg khakis and combat boots next time!

Trace:
[1] parse_query
      in:  vintage graphic tee under $30
      out: {'description': 'vintage graphic tee', 'size': None, 'max_price': 30.0}
[2] search_listings (via MCP)
      in:  {'description': 'vintage graphic tee', 'size': None, 'max_price': 30.0}
      out: 10 items: Y2K Baby Tee — Butterfly Print, Graphic Tee — 2003 Tour Bootleg Style, Vintage Band Tee — Faded Grey … +7 more
      →    branch: 10 results, continuing with lst_002
[3] suggest_outfit
      in:  lst_002 Y2K Baby Tee — Butterfly Print + wardrobe of 10 items
      out: **Outfit 1: Casual Y2K Streetwear** *   Y2K Baby Tee — Butterfly Print *   Baggy straight-leg jeans, dark wash…
[4] create_fit_card
      in:  outfit suggestion + Y2K Baby Tee — Butterfly Print
      out: Found the absolute cutest Y2K Baby Tee — Butterfly Print on depop for just $18.00 and I am obsessed! The pink …
```

**Criterion 2 — try 1.** Query `designer ballgown size XXS under $5`, example
wardrobe. The message is `session["error"]`, set by the empty-search branch in
`agent.py::run_agent`; the trace ends at step [2], so `suggest_outfit` never ran:

```
- stopped early: yes — No listings matched. Try to raise your max price above $5.00, or drop the size filter (xxs), or use broader keywords than "designer ballgown".
- selected_item: (none)
- search_results: 0

Trace:
[1] parse_query
      in:  designer ballgown size XXS under $5
      out: {'description': 'designer ballgown', 'size': 'xxs', 'max_price': 5.0}
[2] search_listings (via MCP)
      in:  {'description': 'designer ballgown', 'size': 'xxs', 'max_price': 5.0}
      out: [] (empty)
      →    branch: empty, stopping
```

**Criterion 3 — try 1.** Query `90s track jacket in size M`, example wardrobe.
Trace from the `trace.step()` calls in `agent.py::run_agent`: step [2]'s note
gives `search_results[0]` as `lst_004`, and step [3]'s input line shows
`suggest_outfit` received `lst_004`, the same listing as `selected_item`:

```
- stopped early: no
- selected_item: 90s Track Jacket — Navy/White Stripe ($45.0, poshmark)
- search_results: 3

Trace:
[1] parse_query
      in:  90s track jacket in size M
      out: {'description': '90s track jacket', 'size': 'm', 'max_price': None}
[2] search_listings (via MCP)
      in:  {'description': '90s track jacket', 'size': 'm', 'max_price': None}
      out: 3 items: 90s Track Jacket — Navy/White Stripe, 90s Silk Slip Dress — Floral, Midi Length, 90s Leather Bomber — Black
      →    branch: 3 results, continuing with lst_004
[3] suggest_outfit
      in:  lst_004 90s Track Jacket — Navy/White Stripe + wardrobe of 10 items
      out: **Outfit 1: Casual Streetwear** *   **Top:** White ribbed tank top *   **Bottoms:** Baggy straight-leg jeans, …
[4] create_fit_card
      in:  outfit suggestion + 90s Track Jacket — Navy/White Stripe
      out: Just scored this 90s Track Jacket on poshmark for $45.00 and I am already obsessed! Threw it on over baggy dar…
```

**Criterion 4 — leather bomber, try 1.** Query `90s leather bomber`, example
wardrobe. Fit card from `tools.py::create_fit_card`. It names the item
("90s Leather Bomber — Black"), the price ("$75.00"), the platform ("depop"),
and is 3 sentences:

```
- selected_item: 90s Leather Bomber — Black ($75.0, depop)

Fit card:
Absolute core-shattered because I finally found the 90s Leather Bomber — Black I’ve been hunting for months on depop. For $75.00, the worn-in leather is giving major grunge energy, and it looks so good thrown over an oversized grey crewneck and khaki trousers. Such a classic vintage win!
```

**Criterion 5 — slip dress, try 1.** Query `silk slip dress`, example
wardrobe. Outfit suggestion from `tools.py::suggest_outfit`. Every piece
besides the thrifted dress is one of the ten in `wardrobe["items"]`: Oversized
grey crewneck sweatshirt, Black combat boots, Black crossbody bag, Vintage
black denim jacket, Chunky white sneakers:

```
- selected_item: 90s Silk Slip Dress — Floral, Midi Length ($30.0, depop)

Outfit suggestion:
Here are two ways to style your 90s silk slip dress using pieces from your wardrobe:

**Outfit 1: Effortless 90s Grunge**
*   **Thrifted Item:** 90s Silk Slip Dress — Floral, Midi Length
*   **Layer:** Oversized grey crewneck sweatshirt (worn layered right over the dress for a skirt-and-sweater 90s effect)
*   **Shoes:** Black combat boots
*   **Accessories:** Black crossbody bag

**Outfit 2: Edgy Casual**
*   **Thrifted Item:** 90s Silk Slip Dress — Floral, Midi Length
*   **Layer:** Vintage black denim jacket
*   **Shoes:** Chunky white sneakers
*   **Accessories:** Black crossbody bag
```

---

## Verdicts and Diagnoses

<!-- MET or MISSED per criterion against LAST UNIT's target, plus a sentence on
     how you decided.

     Then, for every miss: which of the four places it happened — a tool, the
     loop's branch, the session, or the model's output — AND the mechanism.

     Not a diagnosis:  "The fit card was bad."
     A diagnosis:      "The fit card criterion missed on 2 of 5 items. Both had
                        an empty brand field. My prompt puts the brand in the
                        first sentence, so the card opened with a blank and read
                        like a fragment. The tool worked; the prompt assumed a
                        field that isn't always there."

     Look for a pattern. Three misses on the same tool is one problem, not
     three. -->

| # | Criterion | Target | Verdict | How I decided |
|---|---|---|---|---|
| 1 |  |  |  |  |
| 2 |  |  |  |  |
| 3 |  |  |  |  |
| 4 |  |  |  |  |
| 5 |  |  |  |  |

**Diagnoses**



---

## Loop Trace

<!-- One full run, printed step by step, with the MCP call visible in it.

     `python app.py ask '...' --trace` once you've added the trace.step()
     calls in Milestone 2.

     Worth pasting BOTH the happy path and the empty-search path. The empty
     one should be visibly shorter, because it stops. If your two traces are
     the same length, your branch isn't working — and this is the fastest way
     anyone will ever find that out. -->

**Happy path**

```

```

**Empty search**

```

```

**On the MCP move:** <!-- what changed in your code, and whether anything
behaved differently afterwards. If the rewire didn't work, say exactly where it
broke — the error text and the last thing that worked. That earns the point in
full. -->



---

## The Improvement

<!-- What you changed, why your diagnosis pointed at it, and the after-run in
     the same table format. One change, measured properly.

     `python run_eval.py --label after` -->

**What I changed:**

**Which failure it was meant to fix:**

### Run Log — After

| Criterion | Target | Try 1 | Try 2 | Try 3 | Try 4 | Try 5 | Verdict |
|---|---|---|---|---|---|---|---|
| 1.  |  |  |  |  |  |  |  |
| 2.  |  |  |  |  |  |  |  |
| 3.  |  |  |  |  |  |  |  |
| 4.  |  |  |  |  |  |  |  |
| 5.  |  |  |  |  |  |  |  |

**Did it help, and how do I know:**

<!-- If it made things worse, say that. Honestly reported, that earns full
     credit and is more interesting than one that worked. -->



---

## What's Still Broken

<!-- For each criterion still missed: what you'd do, and why you stopped where
     you did. "I ran out of time" is fine if it's true. Pretending nothing is
     left is not. -->



<!-- ═════════════════════════════════════════════════════════════════════

     SUBMISSION CHECKLIST — unit 3

       [ ] criteria.md has five numbered criteria, each with a target
       [ ] Each criterion has a reason underneath it
       [ ] All five unit 3 sections above have real content
       [ ] Tool Inventory: all three tools, inputs WITH TYPES, a specific
           return value, and the empty case
       [ ] Planning Loop names the branch rule and agent.py::run_agent
       [ ] Sample Run: one full query plus the three per-tool tests, as text
       [ ] At least four new commits
       [ ] Repository URL submitted — WRITE IT DOWN, you submit the same one
           next unit

     SUBMISSION CHECKLIST — unit 4

       [ ] mcp_server.py exists with one tool registered
           (or a written record of exactly where the rewire broke)
       [ ] Run Log — Before, five criteria, five tries each
       [ ] Real output pasted underneath, naming file and function
       [ ] A verdict on every criterion
       [ ] A diagnosis for every miss, naming a place AND a mechanism
       [ ] Loop Trace, with the MCP call visible in it
       [ ] All three failure modes triggered and handled
       [ ] One improvement, with Run Log — After in the same format
       [ ] What's Still Broken
       [ ] At least four new commits
       [ ] The SAME repository URL as last unit

     Do not delete and recreate this repository. Your commit history is what
     shows your criteria existed before your results did.
     ═════════════════════════════════════════════════════════════════════ -->

---

📖 **How to run this project: [RUNNING.md](RUNNING.md)**
