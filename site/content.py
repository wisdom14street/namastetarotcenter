"""Namaste Tarot Center: a study center for people learning tarot. Card meanings, deck structure, spreads, how a professional reading runs,
study decks, and Namaste Bookshop's free online course."""
import json, os
import engine as G
from cards import MAJORS, SUITS
E = G.E
BUSINESS_TYPE = 'BookStore'
THEME_COLOR = '#0f4c48'
FONTS = 'https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,600;9..144,800&family=Inter:wght@400;600&display=swap'
ORG_DESC = 'Namaste Tarot Center is a free tarot study site from Namaste Bookshop in New York: card-by-card notes, how the deck is built, practice spreads and how a real reading runs.'
LLMS_NOTE = ('Namaste Tarot Center is a Wealth Edge Ventures Inc. brand connected to Namaste Bookshop, 2 West 14th Street, New York. '
             'All card notes are original study notes. It does not run in-person classes; it points students to Namaste Bookshop\'s free online starter course and to readings at the shop.')
NAV = [('/how-tarot-works/', 'The deck'), ('/card-meanings/', 'Card meanings'), ('/spreads/', 'Spreads'), ('/watch-a-reading/', 'Sit for a reading'), ('/study-decks/', 'Study decks'), ('/free-course/', 'Free course')]
ROMAN = ['0', 'I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII', 'IX', 'X', 'XI', 'XII', 'XIII', 'XIV', 'XV', 'XVI', 'XVII', 'XVIII', 'XIX', 'XX', 'XXI']

def shell(pg):
    nav = ''.join(f'<li><a href="{h}"' + (' aria-current="page"' if pg['path'].startswith(h) else '') + f'>{t}</a></li>' for h, t in NAV)
    return (f'<body><a class="skip" href="#main">Skip to content</a><div class="top"><a class="mark" href="/"><span class="dot">NT</span><span>Namaste <b>Tarot Center</b><i>a study site from Namaste Bookshop</i></span></a>'
            f'<details class="mnav"><summary>Study map</summary><ul>{nav}</ul></details></div>'
            f'<div class="wrap"><aside class="side"><p class="sl">Study map</p><ol>{nav}</ol><p class="sl">Practice in person</p><p class="tiny">Namaste Bookshop<br>{G.ADDR}<br><a href="tel:{G.TEL}">{G.PHONE}</a></p></aside>'
            f'<main id="main">{pg["body"]}</main></div>'
            f'<footer class="ft"><p><b>Namaste Tarot Center</b> is a free study site run by Wealth Edge Ventures Inc. and connected to Namaste Bookshop, {G.ADDR}. '
            f'Readings and decks are booked and sold through <a href="{G.SHOP}/">namastebookshop.com</a>.</p>'
            f'<p><a href="mailto:{G.EMAIL}">{G.EMAIL}</a> &middot; <a href="/about/">About</a> &middot; <a href="/privacy/">Privacy</a></p></footer></body></html>')

def major_page(i, m):
    slug, n, name, words, up, rev, q = m
    prev_, next_ = MAJORS[i - 1] if i else None, MAJORS[i + 1] if i < 21 else None
    nav = ('<nav class="pn">' + (f'<a href="/card-meanings/{prev_[0]}/">&larr; {prev_[2]}</a>' if prev_ else '<span></span>')
           + (f'<a href="/card-meanings/{next_[0]}/">{next_[2]} &rarr;</a>' if next_ else '') + '</nav>')
    body = (f'<article class="lesson"><p class="kicker">Major Arcana &middot; card {ROMAN[n]}</p><h1>{name}</h1><p class="words">{words}</p>'
            f'<h2>Reading it upright</h2><p>{up}</p><h2>Reading it reversed</h2><p>{rev}</p>'
            f'<h2>Journal prompt</h2><blockquote>{q}</blockquote>'
            f'<div class="tip"><b>Study tip.</b> Draw {name} on purpose, set it in front of you, and write three things you can literally see in the picture before you look at any notes. '
            f'Your own observations will stay with you longer than a keyword list.</div>{nav}'
            f'<p class="tiny">Notes on this site are a starting point. Different decks and readers interpret cards differently, and a reading is never a substitute for professional advice.</p></article>')
    G.add(f'/card-meanings/{slug}/', f'{name} Tarot Card: Upright, Reversed & a Journal Prompt | Namaste Tarot Center',
          f'Study notes for {name} (Major Arcana {ROMAN[n]}): what the image shows, how to read it upright and reversed, and a question to journal.', body,
          crumbs=[('Home', '/'), ('Card meanings', '/card-meanings/'), (name, f'/card-meanings/{slug}/')])

def suit_page(s):
    slug, name, elem, theme, cards = s
    rows = ''.join(f'<tr><th scope="row">{r} of {name}</th><td>{t}</td></tr>' for r, t in cards)
    body = (f'<article class="lesson"><p class="kicker">Minor Arcana &middot; {elem}</p><h1>The suit of {name}</h1>'
            f'<p>{name} carry the element of {elem} and deal with {theme}. Numbers one to ten trace a story from first spark to full weight; the four court cards read as people, roles or ways of acting.</p>'
            f'<table class="suit"><thead><tr><th>Card</th><th>Short study note</th></tr></thead><tbody>{rows}</tbody></table>'
            f'<h2>How to practice this suit</h2><ol><li>Lay out the Ace to Ten of {name} in order and say the story aloud in one sentence per card.</li>'
            f'<li>Pull the four court cards and match each to someone you know.</li><li>Shuffle only the {name} and draw one each morning for a week; note what happened that day.</li></ol>'
            f'<p><a href="/card-meanings/">Back to all 78 cards</a></p></article>')
    G.add(f'/card-meanings/suit-of-{slug}/', f'Suit of {name} Tarot Meanings, Ace to King | Namaste Tarot Center',
          f'All fourteen {name} cards in one table, with the element of {elem}, a short note for each card and practice drills for the suit.', body,
          crumbs=[('Home', '/'), ('Card meanings', '/card-meanings/'), (f'Suit of {name}', f'/card-meanings/suit-of-{slug}/')])

def pages():
    decks = G.cached('study_decks', lambda: G.by_handles(['rider-waite-classic', 'apprentice-tarot', 'starter-tarot', 'universal-waite', 'radiant-rider-waite', 'pocket-rider-waite', 'happy-tarot-serena-ficca']))
    why = {'rider-waite-classic': 'The image set most beginner books describe, so your notes and your cards line up.',
           'apprentice-tarot': 'Keywords printed on each card, handy while meanings are still new.',
           'starter-tarot': 'Prints prompts for both directions, which helps when you start reading reversals.',
           'universal-waite': 'Same structure as the classic, recolored in softer tones.',
           'radiant-rider-waite': 'Classic scenes with brighter, higher-contrast color.',
           'pocket-rider-waite': 'Smaller cards that are easier to shuffle and carry to practice.',
           'happy-tarot-serena-ficca': 'A cheerful art style for people who find traditional decks gloomy.'}
    home = (f'<section class="intro"><p class="kicker">Free &middot; self-paced &middot; from Namaste Bookshop</p><h1>Learn tarot one layer at a time</h1>'
            f'<p class="lede">Namaste Tarot Center is a study site for people who want to read tarot themselves. Start with how the deck is built, work through card notes and practice spreads, '
            f'then sit for a reading at Namaste Bookshop and watch how a working reader puts it all together.</p></section>'
            f'<ol class="path">'
            f'<li><span>1</span><div><h2><a href="/how-tarot-works/">Understand the deck</a></h2><p>78 cards, two arcana, four suits, sixteen court cards. Learn the skeleton first.</p></div></li>'
            f'<li><span>2</span><div><h2><a href="/card-meanings/">Study the cards</a></h2><p>Notes for all 22 Major Arcana and a table for each suit, each with something to practice.</p></div></li>'
            f'<li><span>3</span><div><h2><a href="/spreads/">Practice spreads</a></h2><p>Four layouts, from a single morning card to a five-card cross for a decision.</p></div></li>'
            f'<li><span>4</span><div><h2><a href="/watch-a-reading/">Sit for a real reading</a></h2><p>What happens at the table, and what a student can notice from the other chair.</p></div></li>'
            f'<li><span>5</span><div><h2><a href="/free-course/">Take the free course</a></h2><p>Namaste Bookshop\'s seven-lesson Online Tarot School walks you to your first full reading.</p></div></li></ol>'
            f'<section class="box"><h2>Is psychic ability required?</h2><p>Not at all. Reading tarot is mostly looking closely, knowing the structure and practicing a lot. Intuition grows with use.</p>'
            f'<h2>Which deck should I learn on?</h2><p>Any deck you will actually pick up. If you want a guide, the <a href="/study-decks/">study decks page</a> compares seven common starter decks.</p></section>')
    G.add('/', 'Namaste Tarot Center | Learn Tarot: Card Meanings, Spreads & Practice',
          'A free tarot study site from Namaste Bookshop in NYC. Learn how the 78-card deck is built, study each card, practice spreads, and see how a real reading works.', home,
          ld=[G.shop_ld('BookStore')])
    deck = (f'<article class="lesson"><h1>How a tarot deck is built</h1><p class="lede">Before memorizing anything, learn the layout. Once you know where a card sits in the system, you can make a decent guess at it even with no notes.</p>'
            f'<h2>Two halves</h2><p>A standard deck has 78 cards. The <b>Major Arcana</b> are 22 numbered cards, from The Fool (0) to The World (21), and stand for big themes and turning points. '
            f'The <b>Minor Arcana</b> are 56 cards in four suits and cover daily life.</p>'
            f'<h2>Four suits, four elements</h2><table class="suit"><thead><tr><th>Suit</th><th>Element</th><th>Area of life</th></tr></thead><tbody>'
            + ''.join(f'<tr><td><a href="/card-meanings/suit-of-{s[0]}/">{s[1]}</a></td><td>{s[2]}</td><td>{s[3]}</td></tr>' for s in SUITS) + '</tbody></table>'
            f'<p class="tiny">This is the most common pairing. A few decks, especially some Thoth-style ones, swap elements or rename suits; follow your deck\'s guidebook.</p>'
            f'<h2>The numbers tell a story</h2><ul><li><b>Aces</b>: a seed or first chance</li><li><b>Twos and threes</b>: choices and early growth</li><li><b>Fours</b>: a pause or stable base</li>'
            f'<li><b>Fives</b>: friction</li><li><b>Sixes and sevens</b>: adjusting and testing</li><li><b>Eights and nines</b>: momentum and near-completion</li><li><b>Tens</b>: the cycle at its fullest</li></ul>'
            f'<h2>Court cards</h2><p>Each suit has a Page, Knight, Queen and King (some decks use Princess, Prince or other titles). Read them as a person in your life, a role you are playing, or a style of acting.</p>'
            f'<h2>Reversed cards</h2><p>Some readers read cards that land upside down differently, often as blocked, delayed or turned-inward versions of the upright idea. Others ignore reversals. Pick one approach and stay consistent while you learn.</p>'
            f'<p><a class="btn" href="/card-meanings/">Go to the card notes</a></p></article>')
    G.add('/how-tarot-works/', 'How the Tarot Deck Is Built: Arcana, Suits, Numbers & Courts | Namaste Tarot Center',
          'The structure of a 78-card tarot deck explained: Major and Minor Arcana, the four suits and elements, number patterns, court cards and reversals.', deck,
          crumbs=[('Home', '/'), ('How tarot works', '/how-tarot-works/')])
    idx = ('<article class="lesson"><h1>Tarot card meanings for students</h1><p class="lede">Each Major Arcana card has its own page with an upright note, a reversed note and a journal prompt. The Minor Arcana are grouped by suit.</p>'
           '<h2>Major Arcana</h2><ol class="tiles">' + ''.join(f'<li><a href="/card-meanings/{m[0]}/"><b>{ROMAN[m[1]]}</b>{m[2]}<small>{m[3]}</small></a></li>' for m in MAJORS) + '</ol>'
           '<h2>Minor Arcana</h2><ul class="tiles suits">' + ''.join(f'<li><a href="/card-meanings/suit-of-{s[0]}/"><b>{s[2]}</b>{s[1]}<small>Ace to King</small></a></li>' for s in SUITS) + '</ul></article>')
    G.add('/card-meanings/', 'All 78 Tarot Card Meanings: Study Index | Namaste Tarot Center',
          'An index of tarot card study notes: the 22 Major Arcana, each on its own page, and the Wands, Cups, Swords and Pentacles suits.', idx,
          crumbs=[('Home', '/'), ('Card meanings', '/card-meanings/')])
    for i, m in enumerate(MAJORS): major_page(i, m)
    for s in SUITS: suit_page(s)
    spreads = [
        ('Morning card', 1, ['What deserves my attention today?'], 'Draw one card before work. In the evening, write one line about where it showed up. Do this for thirty days and the deck starts to feel familiar.'),
        ('Then, now, next', 3, ['What led here', 'Where things stand', 'The likely next step if nothing changes'], 'A timeline layout. Read the middle card first, then ask how the left card explains it and the right card follows from it.'),
        ('Two roads', 5, ['The heart of the choice', 'Path A: what it offers', 'Path A: what it costs', 'Path B: what it offers', 'Path B: what it costs'], 'Lay the first card in the center and the two pairs on either side. Compare the pairs side by side rather than reading the cards one at a time.'),
        ('Week ahead', 7, ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'], 'One card per day in a row. Look for repeated suits or numbers across the week before reading any single card.'),
    ]
    sp = ('<article class="lesson"><h1>Practice spreads</h1><p class="lede">A spread is a set of positions, each with its own question. These four go from very simple to moderately complex. Practice each one several times before moving on.</p>'
          + ''.join(f'<section class="spread"><h2>{n} <small>{c} card{"s" if c > 1 else ""}</small></h2><ol>' + ''.join(f'<li>{p}</li>' for p in pos) + f'</ol><p>{how}</p></section>' for n, c, pos, how in spreads)
          + '<h2>Writing better questions</h2><p>Open questions give the cards room to say something. "How can I make this job work better?" usually reads more clearly than "Will I get fired?". '
          'Questions about other people\'s private thoughts are hard to read and easy to misread; try framing them around your own choices.</p></article>')
    G.add('/spreads/', 'Four Tarot Spreads to Practice, 1 to 7 Cards | Namaste Tarot Center',
          'Practice tarot spreads for students: a morning card, a then-now-next timeline, a two-roads decision layout and a seven-card week ahead, plus tips on questions.', sp,
          crumbs=[('Home', '/'), ('Spreads', '/spreads/')])
    faq = [('Can I tell the reader I am learning?', 'Yes. Saying so at the start lets the reader explain a little more about why a card means what it does, if they are comfortable doing that.'),
           ('Which reader is best for a student?', 'Choose a style you want to learn. For Thoth study, sit with Casey Deamoira; for Lenormand next to tarot, Mallika; for the Voyager deck, Anthony Fusco.'),
           ('How long should I book?', 'Thirty minutes gives enough time for a full spread plus a couple of follow-up questions. Fifteen minutes is fine for watching one short spread.')]
    watch = (f'<article class="lesson"><h1>Sit for a reading as a student</h1><p class="lede">One of the fastest ways to learn is to watch someone experienced read for you. Namaste Bookshop on 14th Street has readers working most days.</p>'
             f'<h2>What usually happens</h2><ol><li>The reader asks what you would like to look at, or invites you to keep it to yourself.</li><li>You or the reader shuffle, and cards are laid in a spread.</li>'
             f'<li>The reader talks through the cards, connects them and leaves room for your questions.</li></ol>'
             f'<h2>What to notice from your chair</h2><ul><li>Which card the reader looks at first.</li><li>How they link neighboring cards into one sentence.</li><li>When they use the picture versus a traditional meaning.</li><li>How they word hard cards kindly.</li></ul>'
             f'<p>Write your notes after the session rather than during it, so you stay present.</p><h2>Questions from students</h2><dl class="faq">' + ''.join(f'<dt>{q}</dt><dd>{a}</dd>' for q, a in faq) + '</dl>'
             f'<p><a class="btn" href="{G.BOOK}">Book a reading at Namaste Bookshop</a></p><p class="tiny">Readings take place at {G.ADDR}. Sessions run 15 to 60 minutes, and each reader lists their price on the booking page.</p></article>')
    G.add('/watch-a-reading/', 'Learn Tarot by Sitting for a Reading | Namaste Tarot Center',
          'How a professional tarot reading runs, what a student can learn from watching one, and how to book a session at Namaste Bookshop in Manhattan.', watch,
          ld=[G.faq_ld(faq)], crumbs=[('Home', '/'), ('Sit for a reading', '/watch-a-reading/')])
    dk = ('<article class="lesson"><h1>Study decks</h1><p class="lede">You can learn on any deck. These seven are the starter decks Namaste Bookshop recommends in its own beginner guide; prices and stock update daily.</p><ul class="dk">'
          + ''.join(f'<li><img src="{E(G.img(x["img"], 300))}" alt="{E(x["t"])}" width="120" height="120" loading="lazy"><div><h2>{E(x["t"])}</h2><p>{why.get(x["h"], "")}</p>'
                    f'<p class="pr">{G.money(x["p"])}</p><a class="btn" {G.buy_attrs(x, "study-decks")}>Buy this deck</a></div></li>' for x in decks)
          + '</ul><p class="tiny">Buy opens checkout on namastebookshop.com, which ships the deck. If a deck is missing above, it is out of stock today.</p></article>')
    G.add('/study-decks/', 'Best Tarot Decks to Learn On: 7 Starter Picks | Namaste Tarot Center',
          'Seven beginner-friendly tarot decks compared for students, from the classic Rider-Waite to a pocket edition, with live prices from Namaste Bookshop.', dk,
          ld=[G.product_ld(decks, 'Study decks for tarot students')], crumbs=[('Home', '/'), ('Study decks', '/study-decks/')])
    fc = (f'<article class="lesson"><h1>The free Online Tarot School</h1><p class="lede">Namaste Bookshop runs a free beginner course on its own site. It is the natural next step after the notes here.</p>'
          f'<ul><li>Seven lessons, about 90 to 120 minutes in total</li><li>A matching workbook page for each lesson</li><li>A final check where you give a full three-card reading in your own words</li><li>Email reminders are optional; nothing is locked behind sign-up</li></ul>'
          f'<p><a class="btn" href="{G.SHOP}/pages/online-tarot-school">Open the Online Tarot School</a> <a class="ghost" href="{G.SHOP}/pages/free-tarot-starter-course">Go to lesson 1</a></p>'
          f'<h2>Is there an in-person class?</h2><p>This site does not list in-person classes. For hands-on help, the closest thing is a reading with one of the shop\'s readers. For news about anything new, call {G.PHONE} or email {G.EMAIL}.</p></article>')
    G.add('/free-course/', 'Free Online Tarot Course for Beginners | Namaste Tarot Center',
          'Namaste Bookshop offers a free seven-lesson online tarot course with a workbook and final check. Here is what it covers and where to start.', fc,
          crumbs=[('Home', '/'), ('Free course', '/free-course/')])
    G.add('/about/', 'About Namaste Tarot Center', 'Who runs Namaste Tarot Center and how it relates to Namaste Bookshop in New York.',
          f'<article class="lesson"><h1>About Namaste Tarot Center</h1><p>Namaste Tarot Center is a free study site connected to Namaste Bookshop, a metaphysical bookshop at {G.ADDR}. '
          f'Wealth Edge Ventures Inc., owner of the bookshop, publishes it.</p><p>The card notes, spreads and drills were written for this site. The deck suggestions come from the bookshop\'s beginner guide, '
          f'and the "sit for a reading" page points to the readers who work at the shop. The site is a learning aid; it does not certify readers.</p>'
          f'<p><a href="tel:{G.TEL}">{G.PHONE}</a> &middot; <a href="mailto:{G.EMAIL}">{G.EMAIL}</a></p></article>', crumbs=[('Home', '/'), ('About', '/about/')])
    G.add('/privacy/', 'Privacy | Namaste Tarot Center', 'How namastetarotcenter.com uses analytics and where bookings and orders are handled.',
          '<article class="lesson">' + G.privacy('namastetarotcenter.com is a reading and study site. You can use all of it without an account.', products=True) + '</article>',
          crumbs=[('Home', '/'), ('Privacy', '/privacy/')])

NOTFOUND_DESC = 'Page not found on namastetarotcenter.com.'
NOTFOUND = '<article class="lesson"><h1>Lesson not found</h1><p>This page does not exist. Head back to the <a href="/card-meanings/">card index</a> or the <a href="/">study map</a>.</p></article>'

CSS = """:root{--teal:#0f4c48;--coral:#e0704a;--bg:#f4f1ea;--ink:#1d2725}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--ink);font:16.5px/1.7 Inter,system-ui,sans-serif}a{color:#0d6b63}
h1,h2{font-family:Fraunces,Georgia,serif;line-height:1.15;color:var(--teal)}h1{font-size:clamp(1.9rem,6vw,2.7rem);font-weight:800;margin:.2em 0 .4em}
.skip{position:absolute;left:-999px}.skip:focus{left:8px;top:8px;background:#fff;padding:6px}
.top{display:flex;justify-content:space-between;align-items:center;gap:10px;padding:12px 16px;background:#fff;border-bottom:3px solid var(--coral);position:sticky;top:0;z-index:5}
.mark{display:flex;gap:10px;align-items:center;text-decoration:none;color:var(--ink);line-height:1.15}.mark b{color:var(--teal)}.mark i{display:block;font-size:.72rem;color:#68736f;font-style:normal}
.dot{display:grid;place-items:center;width:38px;height:38px;border-radius:9px;background:var(--teal);color:#fff;font:800 .9rem Fraunces,serif}
.mnav{position:relative}.mnav summary{cursor:pointer;background:var(--teal);color:#fff;padding:7px 12px;border-radius:8px;list-style:none;font-weight:600;font-size:.9rem}
.mnav ul{position:absolute;right:0;top:110%;background:#fff;list-style:none;padding:8px;margin:0;border-radius:10px;box-shadow:0 6px 20px #0002;min-width:200px}.mnav li a{display:block;padding:8px;text-decoration:none}
.wrap{max-width:1100px;margin:0 auto;padding:0 16px;display:grid;gap:24px}.side{display:none}
@media(min-width:900px){.wrap{grid-template-columns:230px 1fr}.side{display:block;position:sticky;top:80px;align-self:start;padding-top:24px}.mnav{display:none}
.side ol{padding-left:1.2em}.side li{margin:.35em 0}.side a[aria-current]{font-weight:700;color:var(--coral)}}
.sl{font-weight:700;text-transform:uppercase;font-size:.72rem;letter-spacing:.12em;color:#68736f;margin:1.4em 0 .3em}.tiny{font-size:.85rem;color:#5b6663}
main{padding:20px 0 40px;min-width:0}.kicker{color:var(--coral);font-weight:700;text-transform:uppercase;font-size:.75rem;letter-spacing:.12em;margin:0}.lede{font-size:1.1rem}
.path{list-style:none;padding:0;counter-reset:x}.path li{display:flex;gap:14px;background:#fff;border-radius:12px;padding:14px 16px;margin:10px 0;border:1px solid #e2ddd2}
.path span{flex:none;width:36px;height:36px;border-radius:50%;background:var(--coral);color:#fff;display:grid;place-items:center;font-weight:700}.path h2{margin:0 0 .2em;font-size:1.2rem}.path p{margin:0}
.box{background:var(--teal);color:#e6f1ef;padding:18px 20px;border-radius:12px}.box h2{color:#fff;font-size:1.15rem}.box a{color:#ffd2c1}
.lesson{max-width:720px}.words{font-style:italic;color:#5b6663;font-size:1.05rem}blockquote{margin:0;padding:12px 16px;border-left:4px solid var(--coral);background:#fff;font-family:Fraunces,serif;font-size:1.15rem}
.tip{background:#fff7f2;border:1px dashed var(--coral);padding:12px 14px;border-radius:10px;margin:20px 0}.pn{display:flex;justify-content:space-between;gap:10px;margin:18px 0}
.suit{width:100%;border-collapse:collapse;background:#fff}.suit th,.suit td{padding:8px 10px;border-bottom:1px solid #e6e1d8;text-align:left;vertical-align:top}.suit th{white-space:nowrap}
.tiles{list-style:none;padding:0;display:grid;grid-template-columns:repeat(2,1fr);gap:8px}@media(min-width:640px){.tiles{grid-template-columns:repeat(4,1fr)}}
.tiles a{display:flex;flex-direction:column;background:#fff;border:1px solid #e2ddd2;border-radius:10px;padding:10px;text-decoration:none;color:var(--ink);height:100%}.tiles b{color:var(--coral);font-family:Fraunces,serif}.tiles small{color:#68736f}
.spread{background:#fff;border-radius:12px;padding:6px 16px 12px;margin:14px 0;border-top:4px solid var(--teal)}.spread small{font:600 .8rem Inter,sans-serif;color:var(--coral)}
.btn{display:inline-block;background:var(--coral);color:#fff;text-decoration:none;font-weight:700;padding:10px 16px;border-radius:8px}.ghost{display:inline-block;padding:10px;font-weight:600}
.dk{list-style:none;padding:0}.dk li{display:flex;gap:14px;background:#fff;padding:12px;border-radius:12px;margin:10px 0}.dk img{object-fit:contain;flex:none}.dk h2{font:600 1rem Inter,sans-serif;color:var(--ink);margin:0}.pr{font-weight:700;margin:.3em 0}
.faq dt{font-weight:700;margin-top:.8em}.faq dd{margin:.2em 0 0}
.ft{background:#0b3532;color:#cfe3e0;padding:22px 16px;font-size:.9rem}.ft a{color:#ffd2c1}
"""
