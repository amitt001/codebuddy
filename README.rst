Real-Time code and document + Paste pad
+++++++++++++++++++++++++++++++++++++++++++

About
+++++++++

**CodeBuddy** is a real-time code and document collaboration web app. It can be used for real-time collaboration. While developing a project many a times developers need help from their peer, teacher or any other person who is more experienced. At that time the CodeBuddy can be used to collaborate. Similarly, many times a common document pad is required for sharing some information, facts, story, etc. There is a docpad which offers this facility. 
The code pad offers the syntax highlighting facility using Ace code highlighter. Docpad shows who are online.

Neither your code nor document is saved in the database. So, codes can be shared privately and without any worry of code or any other information getting leaked.

When a user wants to save codes, notes or some other docs a paste pad can be created. This paste pad is similar to Fedora fpaste, pastepad.org, Github gist etc. 

Once you paste the text, it is saved in the database permanently. It is a secure way to save data and share important textual data. As the pasted information is permanent and can't be modified.


Technical specification
+++++++++++++++++++++++++

* Created using Flask-Python, Fask-socketio, Javascript, Jquery, Bootstrap, CSS, HTML. 

* Extensive use of jquery and flask sockets.

* Database: MongoDB 

Screenshots
++++++++++++

.. image:: screenshots/home.png
    :height: 300px
    :width: 400px
    :alt: CodeBuddy Home Page
    :align: center

-------------------------------------------

.. image:: screenshots/code.png
    :height: 300px
    :width: 400px
    :alt: codebuddy code pad
    :align: center    

--------------------------------------------

.. image:: screenshots/doc.png
    :height: 300px
    :width: 400px
    :alt: codebuddy docpad
    :align: center

---------------------------------------------

.. image:: screenshots/paste.png
    :height: 300px
    :width: 400px
    :alt: codebuddy pastepad
    :align: center
