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
       ${output} =    Open the door    ${dev}  ${open}  ${get}
       Should be equal     ${output}  1
      
Verify close door
       [Tags]    Non Critical
       ${output} =    Close the Door    ${dev}  ${close}  ${get}
       Should be equal     ${output}  0



*** Keywords ***
Creating serial device
       ${dev} =    Init      ${device_name}
       Set Suite Variable    ${dev}

Get Gpio Value
       [Arguments]   ${dev}  ${action}  ${get}
       Gpio write    ${dev}  ${action}
       ${output} =    Gpio read    ${dev}  ${get}
       [Return]    ${output}

Open the Door
       [Arguments]   ${dev}  ${action}  ${get}
       ${output} =    Get Gpio Value    ${dev}  ${action}  ${get}
       [Return]    ${output}

Close the Door
       [Arguments]   ${dev}  ${action}  ${get}
       ${output} =    Get Gpio Value    ${dev}  ${action}  ${get}
       [Return]    ${output}
