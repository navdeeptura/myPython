*** Settings ***
Library    SeleniumLibrary    run_on_failure=Nothing
Library    DebugLibrary
Resource    ../../resources/variables.robot
Resource    ../../resources/locators.robot

*** Variables ***
${firstNameTextBox}    id:input-firstname
${lastNameTextBox}    id:input-lastname
${emailTextBox}   id:input-email
${telephoneTextBox}    id:input-telephone
${firstPasswordTextBox}    id:input-password
${confirmPasswordTextBox}    id:input-confirm
${selectNewsLetterButton}    xpath://label[normalize-space()='Yes']//input[@name='newsletter']
${termAndConditionsCheckBox}  xpath://input[@name='agree']
${continueButton}    xpath://input[@value='Continue']
${alertMessage}    //div[@class='alert alert-danger alert-dismissible']
${failureMessage}    Warning: E-Mail Address is already registered!

*** Test Cases ***
registerUser
    Open browser    ${ecommerceURL}    ${browser}
    Click link    ${clickMyAccount}
    Click element    ${registerButton}
    Input text    ${firstNameTextBox}    ${firstName}
    Input text    ${lastNameTextBox}    ${lastName}
    Input text    ${emailTextBox}    ${email}
    Input text    ${telephoneTextBox}    ${phone}
    Input text    ${firstPasswordTextBox}    ${password}
    Input text    ${confirmPasswordTextBox}    ${password}
    Click element    ${selectNewsLetterButton}
    Select checkbox    ${termAndConditionsCheckBox}
    Click element    ${continueButton}
    Wait until element is visible    ${alertMessage}
    Element Should Contain    ${alertMessage}    ${failureMessage}
    Sleep    5s