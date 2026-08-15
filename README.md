# Shiloh Saints — Team Hub

Mobile-first team hub for Shiloh 4th Grade Football (Class of 2035): roster,
coaching staff, schedule, team stats and per-game box scores.

`index.html` is the whole app — no build step, no dependencies. Open it in a
browser and it runs.

## Layout

```
index.html            the entire site (markup, styles, data, logic)
resize-photos.py      batch-resizes photos for the web
assets/
  sc-logo.png         team mark
  players/            player photos, named by JERSEY NUMBER (24.jpg, 1.png …)
  coaches/            coach photos, named by their id in COACHES (1.jpg …)
  _originals/         full-res originals (git-ignored)
```

## Adding photos

Name each file after the player's jersey number and drop it in
`assets/players/`. Both `.jpg` and `.png` work — the page tries `.jpg`, then
`.png`, then falls back to an initials monogram. Then shrink them for the web:

```bash
python3 resize-photos.py          # add --dry-run to preview
```

Originals are moved to `assets/_originals/` untouched. The script also applies
the EXIF rotation flag and strips EXIF metadata (phone photos can carry GPS).

## Entering a game

Everything derives from the `GAMES` array in `index.html` — player season
totals, the Team Stats page and each box score all roll up from it. Add a
`stats` block to a game and the rest updates itself. Player lines are keyed by
**jersey number**.

On load the page audits each played game and warns in the browser console if
the team touchdown count disagrees with the player lines. The points
cross-foot is off until `SCORING.CONVERSION` is set to this league's
conversion value.

## Access code

The landing screen asks for a 4-digit code. It is a deterrent, not security —
the code sits in `index.html` and asset files can be fetched directly. Keep
this repository private and don't put anything sensitive behind it.
