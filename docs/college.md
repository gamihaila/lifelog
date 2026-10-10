Finally, after spending nine months in the Army, it was time to start
college, an Informatics (Computer Science) major in the Mathematics
department of the University of Bucharest.

I, of course, didn’t have the faintest idea what kind of work I would
be doing after graduating—perhaps some coding in a state-run data
center, still better than being sent to teach math in some remote
village. This was 1986 Romania, and I still hadn’t seen an actual
computer, much less run any code on it. All the programs I had written
so far were handwritten on paper and “executed” by hand, by tracing
them.

My first contact with an actual computer was in my freshman year at
university, by typing my Fortran programs on a punch card machine and
submitting a stack of cards to an operator, then waiting for a
printout the next day. That really forced one to think hard before
writing any code. Around junior year, we finally got access to VT100
terminals where we could actually edit and execute our programs. We
were also introduced to the C programming language around the same
time. What kinds of problems were we coding? Mostly math-inspired:
linear algebra, graph algorithms, recursive algorithms—standard stuff.
Nothing related to any real-world problems. Still, for me it was fun,
and a definite improvement over punch cards.

Then came the opportunity to buy a personal computer. ZX Spectrum
computers were being sold on the black market in the dorms for 15,000
lei, which was a lot of money (about four months’ salary for my
parents). It came without a monitor, so we bought a cheap TV and
installed it in my bedroom. External storage was on cassette tapes, so
I could use my radio-cassette recorder to save and load my programs.
It came preloaded with a BASIC interpreter, and it was also possible
to load a Pascal compiler from a tape. It also had games. I spent many
hours playing the games but also trying to replicate some with my own
BASIC programs. For example, I implemented Slippery Sid (aka Snake)
using the queue data structure that we had just learned, and Tetris,
using the matrix that represents rotation by 90 degrees. I also
implemented a Pentomino tiling program using recursion for a radio
challenge to find the most ways to fill a P-pentomino scaled 3× with
unique pentominoes. When we were taught the Simplex algorithm for
linear programming problems in the Operations Research course, I
implemented it on my Spectrum and submitted it. My professor liked it
so much that he exempted me from the midterm!

In the first semester of junior year we had a class on theoretical
computer science taught by a very non-conformist professor. His name
was Virgil Căzănescu. He was quite a character, chain smoking in class
(was that allowed, probably not, but he didn’t seem to care). His
general demeanor was exactly like what you’d imagine an eccentric
mathematician to be, a figure larger than life. Not only was he
brilliant, he had an uncanny ability to explain complicated concepts
in a very accessible manner. His love for mathematics was deeply
contagious, you could tell right away he really cared about his
subject, more than anyone else. A few weeks into the class, we had an
intersession for practical training, which was meant to give us
unstructured time to experiment with programming on the mainframe
computer in the lab. He used this opportunity to recruit potential
students for undergraduate research projects. He was very open about
it: at the beginning of the intersession period, he asked out loud
from his desk:

“Who are the top three students in order of the university admission
score?”

We all knew exactly the order of the top scores in the class, so three
of us raised our hands.

“Come over here, I want to show you what I’m working on.”

And just like that, we took three chairs next to him at his desk and
he proceeded to introduce us into his research on expressing logical
flowcharts using algebraic expressions which could be rewritten and
reasoned about in a formal way. We all listened to his first few
private lectures, but after a couple of weeks the other two students
had lost interest and I was left alone with him. I have to be
perfectly honest that I didn’t completely understand all the technical
details of his formalism, but I got enough of the intuition of what he
was attempting to be able to ask good questions. After a few such
interactions, he started inviting me to his home to work together on a
paper.

He lived in a high-rise apartment building, just like everyone else,
in a pretty cramped three-bedroom apartment with his wife and two
young sons. He had turned one of the bedrooms into his office, with a
large desk in the middle of the room, and bookshelves all around,
chock full of math books, on the shelves and his desk, and many stacks
of books on the floor. I didn’t find that particularly unusual, it was
just like my dad’s desk area. His wife would drop in and bring us
coffee and home-baked cookies, and then retreat in silence. We would
sit hunched over papers for hours, with me trying to follow what we
were doing, mostly serving as a soundboard for him, forcing him to
spell out any parts that were not sufficiently justified in the
proofs. It was quite thrilling for me to be taken seriously as an
apprentice researcher, even if I didn’t have the full background
needed to advance the theory. It was in his crammed office I first
heard of Category Theory and how it could be used as a common
framework for many areas of Mathematics, including the formal study of
computer programs. It really felt like he was holding my hand into a
wonderful hidden world lying behind the everyday reality.

You can imagine my reaction when, a few months later, prof. Căzănescu
walked into the classroom and emphatically dropped a bound preprint
paper onto my desk, in front of the entire class, with our names on
the cover, entitled “Infinite Flowchart Schemes”. It was my very first
publication. Actually, not quite a peer-reviewed publication, a
preprint published by the Mathematics Institute of the Romanian
Academy of Sciences, but still. We immediately submitted it to a
journal and a few months later it was published[^1].

At the time it was incredibly motivating for me, and building into my
fantasy of one day working as a computer scientist, and possibly
pursuing an academic career. I was conflicted though, simultaneously
pulled into more practical software engineering and theoretical
computer science. It was a time of figuring out what I wanted to do,
and it was confusing.

On the one hand I truly enjoyed the thrill of seeing my programs come
to life: I would type words and my words would literally give birth to
whatever world I imagined.

"In the beginning was the Word, and the Word was with God, and the
Word was God"[^2]

It is hard to describe this feeling to anyone who hasn't ever written
a computer program from scratch. Alone in front of the blank TV screen
with just a blinking cursor, I could build whatever I wanted and it
would materialize in front of my eyes, I could interact with it,
refine it, improve it, perfect it! Having instant feedback for my
attempts was intoxicating, after struggling with a deck of punched
cards and waiting to get the printout the next day from the computer
lab operator. 

On the other hand, imagining the abstract mathematical objects of
category theory and trying to build an intuition starting from
incomplete information was a different kind of fun: less immediate,
more vague, more challenging. I had a clear realization that in order
to get good at this I would have to immerse myself completely in an
endless pit of mathematical knowledge, and I didn't have the
confidence I could do it. I wasn't even sure I wanted to give up
everything else to get good at this.

There is, of course, a bit of similarity between a Math article and a
computer program. Let me explain what I mean: both are structured in a
modular way, each piece becoming a building block for the next. In a
Math article, one starts from axioms, then gives some definitions,
proves some lemmas and propositions, and finally uses all the
preliminary results in the proof of the main theorem. In a computer
program one starts from the basic constructs of the programming
language, numbers, variables, and the specific syntax and semantics of
the language; then introduces some definitions of data structures,
implements some helper functions for simple operations, then
references these functions in the implementation of more complex
procedures, and finally assembles all that into a main program which
calls the complex procedures to achieve the desired computation. In a
math paper one can refer to existing theorems proven by others in
outer papers; in a computer program once can refer to existing
procedures and data structures implemented by others and made
available in programming libraries. We all stand on the shoulders of
giants, rarely building anything truly from scratch. The difference is
that when implementing a computer program one can see immediatelly if
the program works or not, or where it fails, and can iterate on fixes
until one is reasonably sure the program is correct. When writing a
math article, the mathematician doesn't have this luxury. Nobody
spells out every single step down to the axioms, and it is easy to
skip steps that appear obviously true but are actually
incorrect. Happes to the best of them, even to Andrew Wiles when he
proved Fermat's Last Theorem. I find that deeply unsettling and in
retrospect seems to have played a big role in my career choices.

I would only fully resolve this conflict some twenty years later, but
let’s not jump ahead.


[^1]: Virgil E. Cazanescu, George A. Mihaila. Partial flowchart
schemes, In Studii si Cercetari Matematice, 43, 1-2, pp.11-23, 1991

[^2]: John 1:1.