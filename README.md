boardermash
========
Boardermash is a tool for presenting comparisons to users and allowing them to express preferences with a single click or keystroke. Processing of match results is done asynchronously via placing match results into anAWS SQS queue and having workers pull data from the queue. Significant components include:
* HMAC protection for matches that prevents user generation of matches (prevents result skewing via repeated generation of the same matches or matches involving competitors the user wishes to skew)
* Dynamic ELO score updating on match processing. Competitors have scores tracked in a database that represents the canonical state of the competition at any given time. The set of competitors and their scores is then updated in a redis cache that is read as part of the synchronous user interaction
* ELO based matchmaking. In cooperation with Dr. Jennifer J. Carroll, an epidemiologist (http://jenniferjcarroll.net/), an algorithm was developed to match competitors using windowing with a specified mutation rate that randomly generated matches outside of the window. This resulted in faster score convergence.

Over the course of 3 days, over 200,000 matches were processed by the system, producing significant data for post-analysis.
