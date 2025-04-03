# 3340-04-Web-Application

Only modify what is in the SEApp folder.

Add a function within views.py to make a new html file. 

Then add a path into urls.py for that html file.

To modify/add html files themselves. Go in SEApp -> templates -> SEApp -> name_of_file.html.

base.html will be inherited in every other file necessary using {%extends 'SEApp/base.html'%} and will have content necessary for most if not all web pages.
