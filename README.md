# Secret Role Dealer

A single-file, no-build companion web app for the board game [Secret
Hitler](https://www.secrethitler.com) that replaces the physical role
envelopes with a digital pass-and-reveal flow, plus a lightweight way to
run the Fascist powers (Investigate Loyalty, Execute) at the table.

Everything lives in `secret-role-dealer.html` — vanilla JS, no backend, no
build step, no accounts. Refreshing the page wipes the game by design:
nothing about anyone's role is ever stored anywhere.

## Running it

It's a static file. Either:

- Open `secret-role-dealer.html` directly in a browser, or
- Serve the directory with anything that serves static files, e.g.:

  ```
  python3 -m http.server 8000
  ```

  then visit `http://localhost:8000/secret-role-dealer.html`.

## What it does

- Enter 5–10 player names (the first 5 are required, 6–10 are optional) and
  deal roles.
- One phone is passed around the table: each player gets a "Pass to
  [name]" screen, then a press-and-hold reveal pad (so a phone glance can't
  accidentally spoil a role), then a role card showing their team, role,
  and whatever "night phase" intel Secret Hitler's actual rules say they
  should know (fellow Fascists, who Hitler is, or nothing at all).
- A hold-to-redeal control on the pass screen lets the table void every
  role assignment and reshuffle from scratch if someone accidentally sees
  a card that isn't theirs.
- Once everyone's seen their role, the President can trigger Investigate
  Loyalty (reveals a target's party — Liberal or Fascist — never
  specifically whether they're Hitler) or Execute (reveals only
  Hitler-or-not, never party) against any player still in the game.
- Manual "Liberals win" / "Fascists win" controls cover the win conditions
  this app doesn't track on its own (5 Liberal policies enacted; 6 Fascist
  policies enacted; Hitler elected Chancellor after the 3rd Fascist
  policy) — the app doesn't implement the policy tracker or elections, just
  the role-dealing and the two powers that don't depend on them.

## Design notes for anyone extending this

- `ROLE_TABLE`, `HITLER_KNOWS_MAX`, and `dealRoles()` near the top of the
  `<script>` are the only parts that encode Secret Hitler's actual rules —
  kept deliberately separate from the UI/state-machine code below them.
  `dealRoles()` returns a `players[]` array where each player has an
  `intel` object describing exactly (and only) what that player should be
  shown — this shape is meant to port directly to a multi-device backend
  later (push each player's `intel` to their own phone instead of paging
  through everyone on one screen).
- No screen ever colors its background by team (red/blue) — that can
  reflect off a player's face or glasses and tip off anyone glancing over.
  Team is signaled only by the small tinted party sigil, never by full
  screen color, and execution results never reveal party at all (only
  Hitler-or-not), matching the actual rule that an executed non-Hitler's
  party is never revealed to the table.
- `liberalSigil.png` / `fascistSigil.png` are the Party Membership sigils
  extracted from the official print-and-play kit; `process_sigils.py`
  (requires Pillow) recolors them and regenerates the transparent,
  perfectly-square `*-tinted.png` files the app actually references. Re-run
  it if you replace the source images.

## License

Secret Hitler is licensed [CC BY-NC-SA
4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/) by its creators,
Mike Boxleiter, Tommy Maranges, and Mac Schubert. This project is a
non-commercial fan companion under those same terms — see
[LICENSE](./LICENSE). It reproduces none of the original's card art, logos,
or trademarked title treatment beyond the Party Membership sigils described
above.

The official rulebook and print-and-play kit (source for the sigil art and
the rules this app implements) aren't vendored in this repo — get them at
[secrethitler.com](https://www.secrethitler.com).
