At work, the project was going well, we were still meeting with my
former teammates regularly over videoconference, with me working
inside the Research team this time. It seemed to be everything I ever
wanted from a Research position, but with actual product impact. That
arrangement didn’t last long, it did however morph into something
better, although I didn’t quite see it at the time. Let me explain.

It started with one of the engineers in the Research team announcing
his transfer into a product team within Search. It was a team that was
planning to develop a long-form question answering system, that is, a
system that would answer in complete sentences, not just short factual
answers. A few days after that, we got invited to a meeting with the
architect of that new system on neutral ground, in a meeting room
half-way across the campus, between the Research building and the
Search building, on Shoreline boulevard. It was a very consequential
moment, although I had no idea at the time. A couple of days later,
the manager of that team came to see me and ask me if I would like to
join his team. As I had just transferred into my current team, I
declined, saying that I quite enjoyed working with my new team, and
also that I would have to consult with my manager. That’s when he
clarified: “Oh, I already spoke to your manager, your entire team is
joining our project.”

That completely changed the equation: unbeknownst to me, there was a
Google-wide effort underway to “embed” researchers into the product
teams, to have them work side by side with the software engineers to
build products. A totally reasonable idea, in my opinion, as I had
already seen the challenges of keeping Research separate from
Engineering in IBM’s case. The best way it was described to me was
that trying to get research ideas into production was like pushing on
a rope: it only works if the other party (Engineering) is pulling. So,
we all moved into the Search Division and got assigned to this new
project. Of course, short answers would get incorporated into the long
answers, and our short answer candidates would be a critical signal
for scoring the candidate sentences. There was a lot more that needed
to be figured out though. So the team grew more, and many different
subsystems were developed to realize this vision.

I learned a lot during that process: I remember our new manager coming
to our desks to ask why our experimental system was giving a wrong
answer, and we didn’t have an easy way to answer that. “We would need
to add some debugging print statements, compile the code, and run it
again to trace the exact scores produced by the subsystems”. “No”, he
said, “I know you can do that for this particular case, but I want to
be able to debug the scoring myself anytime I see a wrong answer”. It
hadn’t occurred to me that a simple observability change like this
could be so valuable. So we set out to add a detailed “debug mode”
internal URL parameter he could use anytime and get a detailed view of
each and every scoring signal computed by the system for any given
query. In retrospect, we should have thought about that. It reminded
me of my manager from my first job in Toronto who was always telling
us to “never build something that you can’t monitor”.

The system grew more and more complex over time, but with each quality
improvement it became slower and slower, to the point where it was
frequently exceeding the timeout of 100 milliseconds the Google search
process allocated to our question answering system. Unfortunately, a
system that could give great answers but times out is not very useful,
so a new team was formed to address this. A manager with a good track
record of radical performance improvements started looking for
engineers to work on this. He approached me with a small challenge:
cut the running time of one of the scoring systems. I don’t remember
now what I did, but he must have liked it because he asked me to join
his team. We first tried the usual tricks: run the scoring systems in
parallel to reduce the overall wall clock time. That helped somewhat,
at the expense of using more CPU cores, which would sit idle between
requests. Not a very efficient use of resources. The cloud managers
came after us soon enough, our CPU utilization was abysmal. Our
manager then made an aggressive bet: “Give me three engineers for six
months, and we’ll reduce the running time from the current median of
80 milliseconds running in parallel on 8 CPU cores, to 10 milliseconds
running single-threaded on a single core!”. Nobody believed him, but
he was given the time to try. The thinking was that even if we managed
to accomplish half that goal it would still solve the timeout issues.

Not to brag, but under his guidance, we managed to completely
re-implement all the scoring systems in a more efficient way, and the
resulting system did accomplish a 10 millisecond median running time
on a single core. That allowed us to drastically improve the CPU
utilization and run well under the timeout threshold for all queries.
Enormously satisfying project!
