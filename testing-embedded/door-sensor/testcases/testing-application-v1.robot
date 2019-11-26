*** Settings ***
Library    BuiltIn
Library    ../library/gpio.py
Suite Setup    Creating serial device 

*** Variables ***
${device_name}   /dev/ttyACM0
${open}   a
${close}  b
${get}    c

*** Test Cases ***
Verify open door
       [Tags]    Critical
       Gpio write    ${dev}  ${open}
       ${output} =    Gpio read    ${dev}  c
       Should be equal     ${output}  1 
      
Verify close door
       [Tags]    Non Critical
       Gpio write    ${dev}  ${close}
       ${output} =    Gpio read    ${dev}  c
       Should be equal     ${output}  0



*** Keywords ***
Creating serial device
       ${dev} =    Init      ${device_name}
       Set Suite Variable    ${dev}


