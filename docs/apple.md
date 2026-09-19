
Back at IBM Research I had this teammate, Roxana, who joined at the
same time. We used to go for long walks after lunch talking about
anything and everything, including her vision of wearable computing
(this was before the iPhone). She moved to IBM Almaden at some point
but we kept in touch. When we moved to California, we re-started our
lunch conversations: every couple of months or so, we would meet and
have lunch together, first at the Google cafeterias, then, after I
left, in downtown Mountain View. I remember when she called me to tell
me she got an offer from Apple, sometime around 2015. "That's
exciting, you should take it!", I said. She did.

We continued to have regular lunches after that, and in the fall of
2018, when I told her I'm thinking of leaving Megagon, she immediately
suggested I should consider following her at Apple Maps.

"Maps?", I remember asking, "what's so interesting about Maps, it's
just an app..."

"No, it's an entire platform. It's deeply integrated with the entire
iPhone operating system, providing location-aware services to all
applications", she corrected me. "There are plenty of exciting
challenges for someone like you!"

From the outside, I had no idea, but the way she explained it, it made
sense. So I decided to apply. I remember she came to visit us at our home in
Mountain View over Christmas break and sat with me for hours, helping
me bring my resume up to date, focusing on my leadership
contributions. She really believed I should apply for a management
position.

At the same time I responded to multiple recruiters from other
companies, and started interviewing in earnest. Within the span of a
few weeks I had offers from LinkedIn, Open Storage, and Apple. For
Apple I had interviewed in two different divisions: Maps and Siri. The
Apple Siri recruiter told me they wanted to prepare an offer, but that
I need to pick between them and Maps first. I picked Maps, in
large part because of Roxana.

I joined Apple Maps in the spring of 2019. I started getting used to the team and the codebase, and gradually
getting involved in the planning process. My manager also asked me to
have informal discussions with some engineers from another team and
qpick two I would like to be transferred to our team.  After six
months, it was time to officially announce my new management role. My
manager had brief one-on-ones with all the engineers in my new team
asking them if they had any concerns, and then it was official!
Exciting and scary at the same time: we were just about to deploy a
new system to production. I shared my feelings with my manager, and he
understood me completely: "George, just give this management thing a
try this for a couple of years, see how you like it! I know it's not
an easy transition."

Less than a month after my promotion to management, two of the
engineers in my new team left Apple, they had been interviewing with
other companies for a while and got offers. One of them had just
joined our team a couple of months before, through an internal
transfer. Unfortunately, during this short time he had built a
component of the system that we were preparing to launch, and his code
had not been completely reviewed yet. Actually, it turned out that he
was developing this component on his own and nobody in the team fully
understood it yet. First hard-learned lesson: "Never let anybody build
something nobody else understands!"

Well, the lesson was good, but we still had to launch on time! I first
tried to do a code walk-through together with another senior engineer
but although we understood the main idea, neither of us was convinced
that the code would run in a reasonable amount of time in all
cases. And indeed, once we deployed it in a staging environment running
at scale, it would frequently take more than double the allotted time
to complete. Worst of all, there wasn't an easy way to fix it as long
as we kept that approach. We needed to go back to the drawing board. I
approached a couple of engineers and asked them for ideas, got
some leads, but no concrete solution emerged, especially on short
notice. This was late on a Friday afternoon. We called it a day and
went home.

Over the weekend, I kept obsessing about the problem, and finally came
up with a much simpler idea on Sunday afternoon that I thought might
work (sorry for being vague, I can't disclose the problem or the
solution here). On a hunch, I implemented a proof-of-concept solution
on my MacBook and ran it on some real data. It worked, and completed
in much less time than the existing algorithm on the same data, well
under the allotted time! The following week I cleaned up the code,
submitted it for review, and merged it. I was happy we were able to
keep the original launch timeline, but my manager tempered my
enthusiasm: "That's good we delivered the system on time, but I don't
want you to go and implement things by yourself, you have engineers
for that; if you keep doing things like this, over time, they will
come to rely on you, instead of working hard to come up with solutions
themselves." Lesson number two.

When the pandemic hit, everybody went home and we slowly adjusted to
working remotely and meeting only virtually. Initially it was exciting
to see we can be resilient and continue to get things done without the
commute, but after a few months it started to wear us down. Several
engineers got sick and had to take extended time off. I was finding it
increasingly difficult to keep everyone's spirits up, without the
in-person interactions we had taken for granted before.

Initially all of us had to work from home, but after a few months we
were allowed the option to come back to the office, if we wanted. I
asked each engineer in my team if they want to come back, but none of
them was willing. At the time, my kids were also at home, doing their
school work over Zoom meetings, and I was having trouble concentrating
at home. So I went back to the office. I was the only one. The entire
campus was completely empty. I really felt like that lone guy in the
Passengers movie, before waking up Aurora from her hybernation pod. A
few more months passed, and one day another engineer showed up in the
office. Her name was Franziska, she was a new hire in another team,
and she had just moved from Germany. Naturally, we started spending
time together, playing table tennis during the breaks, talking, and
cycling to the other, larger Apple buildings that had their cafeterias
open (ours was still closed for lack of customers). Slowly, very
slowly, more engineers started showing up, and we would all go to
lunch together. At some point, she told me in passing that she is
planning to get her California driver license (she had a German one),
but she didn't have a car for the road test. As I had a Nissan Leaf
in addition to our family car, I offered to lend it to her to practice
and also to go with her to the DMV for the test. I have fond memories
of our long conversations from that time, she was helping me through
some difficult interactions with my daughters, providing some
perspective from her own college years. Even after she eventually
moved to Southern California, we still kept in touch as friends. 

At work, I was spending more and more time in (virtual) meetings, and
less and less time doing what I love, designing and building
software. My manager noticed that (I kept complaining about it), and
at one point asked me to take a few days off and just think about what
gives me joy. I did, and wrote down a long list of all the aspects of
my job that I enjoyed and another one with all the ones I dreaded. I
sent him the lists, unedited. When I got back to work, on our next
one-on-one meeting I said:

"Thank you for being supportive and allowing me to really spend some
time figuring out what I want. When I read back the lists I sent you
it became quite clar that I would rather be a software engineer than a
manager."

"Well, you can, if that's what you want. You can step down and I can
look for someone else to manage the team. Do you have any
suggestions?"

"Actually, I do, and I think he would do a great job." I said, and
nominated the best senior engineer in my team, who was the de-facto
architect of the new system.

So it was, that after about three years of management, I went back to
doing what I love! It wasn't easy, but it was the best decision. It
took a while to figure things out, but after trying to be a
researcher, then college professor, then software engineer, then
manager, then software engineer again, I now know that there isn't
anything else I'd rather do. And that's okay.





