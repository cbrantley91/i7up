Inform 7 Usability Precompiler (I7UP)

====

This is a simple Python webserver to dynamically generate usability enhancements to existing Inform 7 code.  If you are unfamiliar with Inform 7, it is a design-system for text-adventures that uses (somewhat natural) English syntax to generate a world.

Our program parses that input code and generates an html page with possible synonyms (to select from) for nouns/verbs so that the user doesn't have to go "verb-hunting".  For example, if the user were to create the object using "The bathtub is in the Bathroom.", I7UP will allow the user to selectively append:

* Understand "bath" as bathtub.
* Understand "tub" as bathtub.
* Understand "bathing tub" as bathtub.
  
using standard HTML tools (buttons/checkboxes)

Also, if the user has defined any actions, it will conjugate those actions; the phrase:

<pre>The verb to draw is an action applying to a picture.</pre>
  
gets expanded to cover all bases:

<pre>The verb to draw (you draw, he draws, she draws, they draw) is an action applying to a picture.</pre>
  
The code is a bit messy right now, but I will do my best to clean it up before I set this project to rest.  Currently, the code is only deployed on a private server with no outside accessibility, so you'll have to run it using:

<code>  python manage.py runserver </code>
  
Required installs to run:
* Python 3
* Django 1.3
* NLTK (Natural Language Toolkit)
* (additionally, Nodebox is used, however, we included the source of that with the distribution)

====


Beyond that, this was a collaborative effort between Chad Brantley and Tim Phan for their Cal Poly, San Luis Obispo Senior Project.  Our adviser was Foaad Khosmood, a professor of computer science at Cal Poly, SLO.

Any questions, feel free to contact us via github, or email:

*  Chad Brantley: cbrantley91@gmail.com 
*  Timothy Phan: tphan12@gmail.com
