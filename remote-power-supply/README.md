# Remote power supply Server

This code actually simulates  behaviour of a 
remote power supply.

## Concept

Imagine we are going to control four power supply socket
using rps-server.py.

### Power supply port

- P60 
- P61
- P62
- P63

Assign 1 to ON and 0 to OFF each port.
By default all the ports are off.
We need to send a http request in order to control all the four port

Say for example

### To Turn on Power supply 1 

* http://user:password@localhost/Set.Cmd?CMD=SetPower&P60=1

### To get the status of all port

* http://user:password@localhost/Set.Cmd?CMD=GetPower
 
## How to run ?

```
$ export FLASK_APP=rps-server.py
$ flask run
```

