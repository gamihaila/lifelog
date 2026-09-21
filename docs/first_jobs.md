I remember our first day at the Research Institute for Informatics: we
were asked to pick a research group to join. I was at a loss: so far
all my research was purely theoretical, using algebraic objects to
describe the structure of flowcharts. Nobody was working on anything
remotely related to that in the institute, they were mostly focused on
more traditional areas like Operating Systems, Compilers, Networks,
and Information Systems. That's when Dana said:

"George, how about Databases? Every application needs to persist state
somehow, you'll always be in demand. It's not Abstract Algebra, but
it's useful. And I heard that it has a theoretical side to it
too. That's what I'm picking."

At that point, I knew next to nothing about databases, only that I
tried and failed to convert the CS library catalog into a searchable
database, as a school project. I had never seen a commercial database
system ever. I heard of a thing called Oracle, but I don't think it
was installed on our school mainframe, and even if it was, us students
didn't have access to it. However, Dana's arguments resonated with me,
after spending the past couple of years wondering whether my work
could have any possible applications, I was attracted by the idea of
working in a more applied area. So we went together to talk to the
manager of the Database Research group. I don't know what kind of vibe
we were giving, because, after he listened to us he said:

"It's great that you're interested in this area, there are a lot of
interesting problems to solve. I do have one thing I want to warn the
two of you about, though: are you sure you want to work in the same
team and see each other all the time at work too?"

It took us a second to process his question, and then we answered in
unison:

"Oh, we're not married!"

"Oh, sorry", said the manager, slightly confused, "in that case,
welcome to our team!"

So we joined the Database Research group and got assigned seats in
their lab right away.  There was however no on-boarding, no
mentorship, and no oversight to our work. I think I did less work
there than ever before and nobody was really interested. It was quite
a letdown after all the hard classes and the undergraduate research I
did. I kept busy implementing side projects for fun on the work PC,
and getting used to the newest peripheral, the mouse, of course in
text mode, but still a great improvement over arrow keys. I left that
job after about six months. Dana left around the same time too: she
had applied for graduate school in France, and had obtained a
scholarship at the famous École Normale Supérieure in Paris.

At the time I was still enrolled in the fifth year at the university,
a sort of masters program. I remember we were in the final week before
graduation when a young woman came into our classroom during a break
and said something like this, with no introductions:

"Hello, is this the Informatics Fifth Year class?"

"Yes, it is. Who are you?", I remember asking.

"My name is so and so, and I came here to recruit software engineers
for my brother's start-up. Who are the top three graduating students
in your cohort?"

"Petrișor, Cristi and myself", I said, pointing to my classmates.

"Well, my brother has founded a start-up last year and at the moment
we have more computers than people. If you're interested, we would
love to have you visit our lab. Here is our address and phone
number. When would it be a good time?"

"We have our final exams next week but we can come the week after", we
all aggreed.

So, on the appointed day, the three of us went together to the address
on the card and met with her brother, the founder, and the handful of
engineers working there. The company was called Omnis Group and they
were working with some companies and universities in Belgium,
developing some applications for them. The office was in a converted
four bedroom apartment in a residential high-rise building, and indeed
they had about ten Windows PCs, a print server, a couple of printers,
a modem, and a local area Ethernet network connecting
everything. Aside from the founder, there were about five engineers
working there. They also had an impressive collection of American
software engineering books and magazines, which was unheard of in
1991. After an informall chat with the founder we were all hired on a
trial basis, with a basic official salary in lei which was already
more than my pay as a TA at the university, supplemented by a monthly
pay in dollars, completely off the books. Moreover, the dollar amount
was going to be increasing every month for the first year, provided
that we had a satisfactory performance. This was not that unusual in
those early years of free market capitalism after ther revolution,
where the many start-up firms that had sprung up were competing for
the relatively few engineers on the market. Of course, it was all very
hush-hush, we were just paid in cash with no paper trail, and we were
not supposed to talk about it. At first, I thought that was quite
sketchy and I was afraid that the shadow payments will dry out
eventually, but they kept coming, month after month, each month more
than the previous one. They weren't large amounts, in absolute terms,
on the order of a hundred dollars a month, but they were more dollars
that I had ever seen in my life, and the exchange rate was insanely
favorable, what with the national currency in free fall and
everything. We were living it up, very soon I was making more money
than my parents combined.

At Omnis Group is where I first
saw a graphical operating system, the new Microsoft Windows 3.1, in
1991. I learned how to write programs for Windows from the Charles
Petzold book, Programming Windows. At the time, the programs were
single threaded, and the book taught us to write event handlers that
returned control quickly because otherwise the operating system would
be frozen. These were interactive programs: a user would push a button
on the UI, or select a menu item, something needed to happen in
response, and then the program would wait for the next user
interaction. So I used this paradigm to implement some sort of
accounting application for a Belgian oil refinery that was backed by a
network database called dbVista.

There were tools for designing the GUI visually and converting it to
runnable assets accessible from C code. I also started learning C++
there, from Bjarne Stroustrup’s book. I needed that for the next
project, a research GUI for analyzing proteins. There were some
edge-detection algorithms there, but I don’t remember much about that
project other than the fact we were using graphical workstations
running X11 and the mice were optical with a special mouse pad with a
grid on it. I also had my first contact there with running remote
sessions over the LAN on my colleagues' workstations. We were playing
pranks on each other by opening windows on someone else’s screen. It
was there I first heard of telnet and ftp. No email just yet, since
our LAN was not permanently connected to any external network. There
was an occasional connection through a modem and a leased telephone
line, I heard, but that wasn’t part of my day-to-day work.

I was working two jobs at this point: full time software engineer at
Omins Group and part-time teaching assistant at the University. I was
also supposedly continuing my collaboration with prof. Căzănescu, with
the understanding that I would eventually work towards a doctoral
dissertation under his supervision. This wasn't sustainable, and after
a year of running around and having very little to no time left for
research I left my job at Omnis Group thinking I could focus on my
academic career.

I was wrong. My in-laws started to ask me to run errands for them the
moment I was out from my full-time job: I apparently had too much time
on my hands. Also, the savings from my high paying gig eventually
drained up and we could no longer afford the nice life we had just
started getting used to, on Ioana's teacher salary and my TA stipend.

I clearly needed another full-time job, and fast. Hearing
me say that, our old friend Claudia offered to talk to her boss about
me. She was a salesperson at the Romanian branch of Ciel!, a French
accounting software company. And wouldn't you know it, he called me
for an interview the very next week! On the appointed day I went to
their office in the Bucharest Hotel, remembering how I had carried
bricks when the hotel was being built during my high school mandatory
"volunteering" weeks (we were all taken out of regular classes for two
weeks to work on various construction sites each year).

Anyway, I got to the manager's office and he showed me the company
software suite on his PC. It was a comprehensive set of accounting
applications they were adapting for the Romanian small businesses, all
running in text mode, with drop down menus and text-based input
forms. I looked at him and said: "This is good, but nowadays the
competition has modern GUIs running inside Microsoft Windows. Give me
six months and I will rewrite one of these applications completely
from scratch in Windows, as a proof of concept." He hired me on the
spot.

There I worked on porting to Windows an old text-mode Clipper
accounting application called “Ciel! Dossiers Analytiques”. One
thing I remember about that was the trouble caused by rounding for
accounting applications, where the monetary amounts had to match
precisely, down to cents.

I remember there was this constant friendly teasing between the
software people and the sales people about who's contribution was more
important: of course we were arguing that without us, there would be
nothing to sell, but Claudia was pointing out that our software would
be worthless if she and her peers didn't get the customers to pay for
the license. She had a point!


