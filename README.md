# blog_corpus
Script to download the corpus from "Detecting Dementia through Retrospective Analysis of Routine Blog Posts by Bloggers with Dementia"
- Install the dependencies with 'pip2 install -r requirements.txt'
- Run 'python get_data.py'

Posts were manually tagged as either 'good', 'bad', or 'questionable', based on how much of the post contained writing by the blogger. Some posts, for example, contained mainly images, quotes, or letters from readers, and were therefore tagged as 'bad'. Tags are stored in the filters directory and are current up to April 4th, 2017.

Python2.\* is required (Tested on Python 2.7.1) 

If you use this corpus please cite:

Detecting Dementia through Retrospective Analysis of Routine Blog Posts by Bloggers with Dementia,
V. Masrani and G. Murray and T. Field and G. Carenini, ACL 2017 BioNLP Workshop, Vancouver, Canada.
