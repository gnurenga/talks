*** Settings ***
Library     OperatingSystem
Library     BuiltIn

*** Variables ***

${url}     www.chennaipy.org


*** Test Cases ***
Verify traffic is generated
      open the log in the background
      map the user
      verify the user is mapped
      send traffic v2
      verify the traffic is generated


*** Keywords ***
open the log in the background
     log    file is opened
map the user
     log    user mapping request has be sent
     
verify the user is mapped
     log    user is mapped
     
send traffic v1
      run   wget $url

send traffic v2
     ${ret}=   run and return rc   wget ${url}
     should be equal as integers    ${ret}  0


verify the traffic is generated
     log   traffic is generated   