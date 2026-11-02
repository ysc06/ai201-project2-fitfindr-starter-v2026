"""
The runs your test needs. ← UNIT 4, MILESTONE 3

Each of your five criteria needs something run against it. A criterion about
the empty-search branch needs an impossible query. One about the fit card needs
the same item run more than once. Working that out is Milestone 3's first step,
and this file is where you write it down.

`run_eval.py` runs everything here five times and writes the run log — five
because your criteria are written out of five.

Three scenarios are filled in to show the shape. Add or change whatever your
own criteria need — these are a starting point, not a fixed set.
"""

SCENARIOS = [
    {
        # A query the data can match. Criterion 1.
        "name": "matching query completes",
        "query": "vintage graphic tee under $30",
        "wardrobe": "example",
        "criterion": 1,
    },
    {
        # A query nothing can match. Criterion 2 — the branch.
        "name": "impossible query stops early",
        "query": "designer ballgown size XXS under $5",
        "wardrobe": "example",
        "criterion": 2,
    },
    {
        # A user with nothing saved. One of unit 4's three failure modes.
        "name": "empty wardrobe",
        "query": "denim jacket under $50",
        "wardrobe": "empty",
        "criterion": None,
    },
    {
        # Criterion 3 — the id search put first must be the id suggest_outfit
        # got. Needs 2+ results, or picking the wrong index can't show up:
        # this one returns 3, lst_004 first. Compare the id in trace step [2]'s
        # note with the id on step [3]'s input line.
        "name": "search result reaches suggest_outfit",
        "query": "90s track jacket in size M",
        "wardrobe": "example",
        "criterion": 3,
    },
    # Criterion 4 — "for 5 different items", so one scenario per item, each
    # run five times. Picked to spread what the card has to get right: all
    # three platforms, prices from $12 to $75, five categories. Each query's
    # first search result is the item named in the comment.
    {
        # lst_022 — $75, depop, outerwear (the most expensive listing)
        "name": "fit card: leather bomber",
        "query": "90s leather bomber",
        "wardrobe": "example",
        "criterion": 4,
    },
    {
        # lst_018 — $38, thredUp, blazer
        "name": "fit card: linen blazer",
        "query": "linen blazer under $40",
        "wardrobe": "example",
        "criterion": 4,
    },
    {
        # lst_028 — $44, poshmark, shoes
        "name": "fit card: chelsea boots",
        "query": "suede chelsea boots",
        "wardrobe": "example",
        "criterion": 4,
    },
    {
        # lst_011 — $27, poshmark, pants
        "name": "fit card: cargo pants",
        "query": "low-rise cargo pants",
        "wardrobe": "example",
        "criterion": 4,
    },
    {
        # lst_014 — $12, thredUp, accessory (the cheapest of the five)
        "name": "fit card: leather belt",
        "query": "braided leather belt under $15",
        "wardrobe": "example",
        "criterion": 4,
    },
    # Criterion 5 — no invented wardrobe pieces, on 5 matching queries. Picked
    # to tempt the model: each item's usual pairings are missing from the
    # example wardrobe (no skirts, dresses, shorts, shirts, jewelry, sandals,
    # socks). A piece the outfit presents as owned that isn't in
    # wardrobe["items"] is a FAIL; the thrifted item itself is fine.
    {
        # lst_013 — a dress; tempts sandals, jewelry, a cardigan
        "name": "wardrobe only: slip dress",
        "query": "silk slip dress",
        "wardrobe": "example",
        "criterion": 5,
    },
    {
        # lst_009 — shoes; tempts a pleated skirt, white socks
        "name": "wardrobe only: mary janes",
        "query": "platform mary janes",
        "wardrobe": "example",
        "criterion": 5,
    },
    {
        # lst_023 — summer top; tempts denim shorts, a skirt, sandals
        "name": "wardrobe only: halter top",
        "query": "crochet halter top",
        "wardrobe": "example",
        "criterion": 5,
    },
    {
        # lst_036 — formal; tempts a button-down, loafers, jewelry
        "name": "wardrobe only: velvet blazer",
        "query": "velvet blazer",
        "wardrobe": "example",
        "criterion": 5,
    },
    {
        # lst_017 — sheer layer; tempts a bralette or slip, a mini skirt
        "name": "wardrobe only: mesh top",
        "query": "mesh long-sleeve top",
        "wardrobe": "example",
        "criterion": 5,
    },
    #
    # Set "criterion" to the number in criteria.md that the scenario tests.
    # "criterion": None means a diagnostic run — useful to have, but it isn't
    # one of your five, and run_eval.py marks it as such in the table.
    #
    # For a state criterion, any normal query works — what you're checking is
    # what ends up in the session, not what the user typed.
    #
    # For a fit-card criterion, you probably want the SAME query listed more
    # than once, or several different items, depending on what your criterion
    # actually says.
]

WARDROBES = ("example", "empty")


def validate() -> list[str]:
    """Complain about anything malformed, before a long run rather than during."""
    problems = []
    for i, scenario in enumerate(SCENARIOS, 1):
        if not scenario.get("query", "").strip():
            problems.append(f"scenario {i} has no query")
        if scenario.get("wardrobe") not in WARDROBES:
            problems.append(
                f"scenario {i} has wardrobe {scenario.get('wardrobe')!r} — "
                f"it should be one of {WARDROBES}"
            )
    return problems
