*** Settings ***
Library     Collections
Library     string_operation.py


*** Test Cases ***
example test case
     # we will send lot of request before this line of code
     # to get the data
     ${rows}=   convert_to_rows    data.txt
     ${row0}=   Get from dictionary   ${rows}  0
     verify row    ${row0}  aa:bb:cc:dd:ee:ff  

*** Keywords ***
verify row
       [Arguments]    ${row}  ${mac}
       ${value}=   Get from dictionary   ${row}  mac
       Should be equal    ${value}  ${mac}
     