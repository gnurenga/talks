= Script to check all the Server is up =

== About ==

The ping server script will ping all the available server present in
`server.yaml` file and if any of the server is down it will send a mail
to recipents given in the code and also if the server comes from down to up
recipents will receive mail regarding the server up.

== Files ==

----
server_status_scripts/
|-- ping_server.py
|-- readme.txt
`-- server.yaml
----

== Usage ==

----
$ python ping_server.py 
----

When we run the above script it will take server details from
`server.yaml` and check whether the server is reachable or not.
If the server is not reachable, this script will send mail to
recipients mentioned in the script.

It also send mail if the server comes up from down state.
i.e when ever there is a transition of server from up to down
or down to up, recipients will get a mail.


== To Do == 

* Move the mail recipeints outside the script.
* Plan to run as a service.

 
