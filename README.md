app.py => Flask - SocketIO Server

data.py => MongoDB connection module

user.py => User class model

templates/index.html => Landing Page

templates/readPage.html => Working/Reading/Accessing page to be accessed only when loggedin

static => CSS & JS files

static/images => profile avatars

jsonmodule.py => module to deal with json storage of users list in case you dont want to use mongoDB

jsonreset.py => script to reset json userlist database(used by jsonmodule.py)

requirements.txt => dependency list

**

Put your server address in line 108 of templates/readPage.html
as mentioned below:

const socket = io.connect('\<server-address\>');

For localhost
const socket = io.connect('http://localhost:5000');

**
