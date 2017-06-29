*** Settings ***
Library       ../library/rps/commands.py

*** Test Cases ***
Turn on Power supply 2 remotely
     ${out}=    RPS send commands     SetPower  2  1
     Should be equal    ${out}  ${True}

Verify power supply 2 is on
    ${out}=     RPS get power    GetPower
    should contain    ${out}  P62=1

Turn off Power supply 2 remotely
     ${out}=    RPS send commands     SetPower  2  0
     Should be equal    ${out}  ${True}

Verify power supply 2 is off
    ${out}=     RPS get power    GetPower
    should contain    ${out}  P62=0


*** Keywords ***
RPS send commands
    [Arguments]    ${command}    ${port}    ${state}
    ${output}=    Send cmds    ${command}  ${port}  ${state}
    [return]    ${output}

RPS get Power
    [Arguments]    ${command}
    ${output}=    Send cmds    ${command}
    [return]    ${output}

