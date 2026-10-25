# Direction template

Every direction file has these sections. Numbers, not adjectives: a verifier must be able to
measure the page against each line.

## What feels clumsy today
Measured findings from the walk (sizes in px, what shifts, what disagrees between pages). Omit for
an app with no screens yet.

## The feeling
One line ("a well-kept notebook: quiet paper, one voice of type, one left edge, one colour that
always means *now*").

## Type
- Families, and which role each is for (one family for everything that speaks is a good default).
- **At most seven sizes**, as a table: role, weight, desktop size/line height, phone size/line height.
  Roles: page title, answer or key figure, section heading, body, label (tabs, buttons, row heads),
  small, micro.
- Figures tabular where numbers line up. Whether all caps is allowed (default: no).
- **The selected state never changes weight** — a bold selected tab widens and shifts its neighbours.

## Spacing and grid
- The spacing steps (e.g. 4 / 8 / 12 / 16 / 24 / 32 / 48 / 64); nothing off them.
- Side margin at each width. Columns and gutter.
- Page widths by kind: working pages (grids, boards) take the window; reading pages hold a column
  (~880px); a conversation holds a narrower centred one (~640px).

## Alignment
The one left edge that the wordmark, first tab, page title, table edge and first column share, at
every width. The inset shared by table heads and cells.

## The top of every page, at each width
Phone, tablet, laptop: rows, heights (fixed at each width), what sits where, whether it sticks, how
navigation collapses on a phone. The header is the same height on every page.

## Colour
Each colour and its single meaning. Ink, muted ink, lines, fills, and the accent — say what the
accent means and that it means nothing else. Dark mode values for each.

## Controls
Button kinds (at most two: primary filled, secondary outlined), one height for buttons, chips and
fields, how a chosen chip or segmented option looks. One word per state across the app.

## Tables and grids
Head style, cell alignment, what pins when scrolling, hover and selected rows in both themes, how an
empty cell reads.

## States
Hover, focus, selected, empty, loading, error, and the designed message page for a bad link or
server fault — none of these as bare text.

## Motion
What moves, how long, and that nothing moves the layout under the reader's finger.

## Build order
The shell first, then pages in order, each with the one or two changes that matter most on it.
