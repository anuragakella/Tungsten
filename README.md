# Tungsten
A simple (very simple) HTTP Server

Currently supports GET and HEAD requests and;

It can serve a large range of filetypes!


# Instructions 

Want to Run Tungsten? OK, look below.

## you need a working installation of python 3 on your computer to run tungsten

- Download the whole repo (usually a .zip)
- create a folder somewhere (your choice)
- Extract the zip file into that folder 
- ``cd`` into that folder and run ``python runserver.py``

That's it! 
the server can now serve files from the /serve/ folder (there's a png and an index.html (+css) to test: open ``http://127.0.0.1/`` on a browser)
[you can add more files to check]

to change the IP, PORT, index file etc -- open settings.tgs and change the fields

important: don't add extra new lines in the tgs file, don't add spaces -- the settings parser will panic

(PS: Tungsten is far far away from a usable production server. Educational only, I made this to learn how HTTP servers work)

Thank you :)
