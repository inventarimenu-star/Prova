# Boulevard Caffe — Instagram/Facebook playbook (for scheduled runs)

Owner: Erald. He wants this run without asking him for each post. Report results in Albanian, short.

## Owner's decision 21 Oct 2026 (overrides the rest)
Metricool free plan = 20 posts/month. From 21 Oct 2026 the owner posts Reels/Stories HIMSELF via Meta Business Suite;
Metricool is used ONLY for the match-day Story (scheduled task). Daily-morning and weekly-planner tasks are disabled.
Claude prepares videos/captions on request and checks prices in the DB; it does not schedule other posts in Metricool.

## Accounts
- Metricool brand blogId `7293736` → Instagram `@boulevard.cafe_el` + Facebook page `boulevardcaffe`.
- Publish every post to BOTH: providers `[{"network":"instagram"},{"network":"facebook"}]`,
  `instagramData.type` REEL/STORY, `facebookData.type` REEL/STORY, `instagramData.isAiGenerated: true` when the photo is AI-made (all photos in media/base are).
- Media must be a public URL: commit the file to this repo (main) and use
  `https://raw.githubusercontent.com/inventarimenu-star/Prova/main/<path>`.

## Source of truth for prices and offers (read-only!)
Lovable connector, `query_database`, project `58dc0c87-3008-4bdc-85e3-82d8c17aeb57`. Never write to the database.
- Offers: `combo_offers` (enabled, start_time, end_time) → `combo_offer_conditions` (item_id) → `combo_offer_rewards`
  (price = discount, negative). Net price = `menu_items.price + reward.price`.
- Known offers: Oferta e Mëngjesit `0fd8218a-…` (07–11), 🍺 & 🍷 `c5245195-…` (12–23),
  Oferta e Drekës 🍕 `75934a0f-ba5c-4691-a263-d1fd183e0742` (12–18, ends 31 Oct 2026).
- Sales: `pos_orders` (status='closed', items jsonb [{name, price, quantity, forKitchen}], created_at UTC; use Europe/Tirane).
- Only promote an offer if `enabled = true` at run time, with prices computed from the DB. Never invent prices, numbers or claims.

## What sells (30 days to 14 Oct 2026)
Peaks 08–11 and 18–20 (19:00 best). Dead 14–17. Thursday weakest, Friday best. Espresso ≈29% of revenue.
Kitchen only 13% → push food at lunch (12–18 offer) and evening. Top beer: Heineken shishe. B52 popular in evenings.
Pomodoro Pizzeria (5.0★) is 50 m away: position Boulevard as coffee + quick lunch deal + beer & snacks, not a pizzeria.

## Weekly rhythm (max one Reel per day + the daily 07:30 Story, which a separate task handles)
- Mon 18:30 evening drinks (beer offer if active) · Tue 11:30 lunch offer · Wed 18:30 beer
- Thu 11:30 lunch offer + Thu 19:00 food (weakest day) · Fri 18:30 drinks · Sat 11:30 lunch · Sun none
Avoid the same photo/angle two days running. Skip a slot rather than post something inaccurate.

## What performs on the accounts (Metricool, Jul–Oct 2026)
- IG ~2,600 followers. Best post ever: 14 Sep breakfast-offer PHOTO (reach 508, 987 views). Offer photos beat Reels
  (Reels ~250 reach). Reach collapses to ~3/day on days with no post → post every day.
- Facebook page has MORE followers (~3,670) but was almost unused (1 post in 90 days, slowly losing followers) → always cross-post.
- So: per week publish 2 of the Reels ALSO as a feed photo POST the next day (frame at 0.5 s of the Reel, saved as .jpg:
  `ffmpeg -ss 0.5 -i reel.mp4 -frames:v 1 -q:v 2 out.jpg`), instagramData type "POST", facebookData type "POST".
- Report reach of last week's posts in the weekly report (IGRE11/IGRE23 reels, IGPO14/IGPO28 posts, IGEV20 stories, FBRE11/FBPO12).

## Hero product: premium Belgian beers (owner's call, 14 Oct 2026)
Duvel and Blanche de Namur are top Belgian beers. In the 🍺&🍷 offer they cost 200 lekë (from 350 / 320), the same as a
Heineken, yet sold 0 in the 30 days to 14 Oct while Heineken sold 227. Nobody knows. While the offer is enabled with those
prices: give them one evening Reel per week (prefer Friday or a big-match night), lead with "birrat belge premium me çmimin
e një Heineken-i", and track their weekly sales in the report (menu names "Duvel Beer", "Blenche de Namy").

## Photos (media/base) — some have text baked in
- `heineken.jpg` — headline "HEINEKEN 200 LEKË · Shishe ose kriko · 12:00–23:00": use ONLY while 🍺&🍷 is enabled and both Heineken net prices are 200.
- `food-lunch.jpg` — headline "OFERTA E DREKËS · 12:00–18:00 · 100 lekë më lirë": use ONLY while the lunch offer is enabled with −100.
- `food-pizza.jpg` — headline "PIZZA NGA 500 LEKË · Chicken finger · Wings · Fokace": use only if the cheapest pizza price is 500.
- Coffee photos (espresso, latte-beans, latte-flatlay, cheers, terrace) — no prices, mornings only.
Never write "pica": the owner wants "pizza".

## Tools
- Reel: `python3 tools/reel_gen.py cfg.json` (cfg: src, tmp, out, anchor_y, subtitle, card_title, card_sub,
  rows [[label, price, sub, old_price]] max 4, foot1, foot2). Check two frames with Read before publishing.
- Music (owner, 14 Oct 2026): EVERY video gets original Italian-style melody (mandolin/accordion), NEVER a voice.
  Styles: `mattina` = coffee/breakfast/morning/app, `pranzo` = lunch/pizza by day, `sera` = evening, beer, football, food after 18:00.
  `pianobar` = solo lounge piano (the café used to host live piano-bar nights): alternate it with `sera` for evening
  posts, especially premium beers (Duvel/Blanche), wine and calm evenings; keep `sera` for football nights.
  Reel: `python3 tools/italian_music.py 12 m.wav <style> <seed>` then `python3 tools/audio.py mix in.mp4 m.wav out.mp4`
  (music length = video length; use a different seed each post so no two posts sound the same).
- Stories are published as 10 s VIDEO with music, not as still jpg:
  `python3 tools/story_video.py in.jpg out.mp4 <style> <seed>` (slow 4% zoom, text stays in frame). Morning Stories `mattina`, match-day `sera`.
- Videos the owner makes himself (CapCut etc.) keep THEIR OWN audio (owner, 17 Oct 2026); Italian music only on videos we generate.
- Feed photo POSTs (frame grab) stay photos (Instagram API cannot add music to photos); they are the only exception.
- Captions: Albanian first, one short English line, one ask, max 4–5 hashtags (#elbasan #elbasancafe + topic).
- Check `getScheduledPosts` first; never duplicate a slot that already has a post.

## Football (the café shows all big matches)
- Match-day Story: `python3 tools/matchday.py D matches.json [--offer "Heineken 200 lekë · shishe ose kriko"]`
  matches.json = [["HH:MM local Tirane", "Home", "Away", "Competition"], ...], max 7, kickoffs 12:00–22:30 only.
- Leagues: Champions League, Premier League, Serie A, La Liga, Bundesliga, Ligue 1, World Cup / Euro / Albania national team.
  Prefer the biggest clubs when there are more than 7. Short common names (Man City, PSG, Real Madrid).
- Design: night stadium + ball (owner's choice, 17 Oct 2026) = default style of matchday.py (background media/base/stadium.jpg).
- Club crests next to team names (owner's decision, 17 Oct 2026; tools/logos via tools/logos.py). No league logos. Teams without a crest (e.g. national teams) show the name only.
- Offer line only if 🍺&🍷 is enabled and Heineken net price matches.

## 10:00 "Ora e fundit" Story (owner's idea, daily while the breakfast offer is enabled)
`python3 tools/lastcall.py D rows.json --until <offer end HH:MM>` → media/daily/oferta-ora-fundit-D.jpg, posted 10:00.
Rows (label, net price, old price or null), prices from the DB every day:
Çokollatë e nxehtë = ÇOKOLLATE · Kapuçino = KAPUCHINO ME KAFE · Çaj bio = CAJ I NXEHTË BIO · Briosh = Briosh ·
Tost mëngjesi = Tost Mengjesi (not in the offer → old price null). Skip the Story if the breakfast offer is disabled.

## Lottery QR reminder (owner: never forget it)
Every receipt has a QR lottery ticket ("Skano QR-në në faturë: mund të jesh fitues").
Check `select enabled, ends_at from lottery_settings` (read-only). While enabled and today ≤ ends_at:
- pass `--qr` to greeting.py, lastcall.py and matchday.py (adds the gold pill),
- end every Reel/post caption with the line: "🎟️ Skano QR-në në faturë, mund të jesh fitues!"
- the weekly report may quote real totals (wins, lekë returned) from lottery_tickets; never invent odds or numbers.

## Loyalty program "E 10-ta FALAS" (live since 16 Oct 2026)
Every 10th unit of each item is free; counted only for orders placed from the phone menu (scan table QR → caffeboulevard.com,
name entered the first time, same phone; 30 days without orders resets). Check `select enabled from loyalty_settings` (read-only).
While enabled: mention it in coffee/breakfast captions ("☕ E 10-ta kafe FALAS kur porosit nga telefoni") and in app posts.
Media: media/besnikeria/ (programi-besnikerise-9x16.png, besnikeria-story*.mp4 — QR verified to open caffeboulevard.com).
Owner's decision (17 Oct 2026): a loyalty Story EVERY day, rotating 09:00 / 13:00 / 19:00 (day of year mod 3), always
  media/besnikeria/besnikeria-story-capcut.mp4 (owner, 17 Oct 2026: only the CapCut video, not the poster). Skip if a Story already sits at one of those three times that day. Never claim numbers of members.
Note: the lottery only gives a chance to bills up to max_prize_value (lottery_settings) — don't promise "every bill can win".
