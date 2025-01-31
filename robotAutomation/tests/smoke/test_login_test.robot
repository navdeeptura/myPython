*** Settings ***
Library    SeleniumLibrary    run_on_failure=Nothing
Library    DebugLibrary
Resource    ../../resources/variables.robot
Resource    ../../resources/locators.robot

*** Variables ***
${LOGIN BUTTON IN MENU BAR}    xpath://a[normalize-space()='Login']
${EMAIL_ADDRESS_TEXTBOX}    xpath://input[@id='input-email']
${PASSWORD_TEXTBOX}    xpath://input[@id='input-password']
${LOGIN_BUTTON}    xpath://input[@value='Login']
${MY_ACCOUNT_TEXT}    xpath://*[@id="content"]/h2[1]
${LINK_TEXT}    link:Edit your account information
${element}   class:list-group-item

*** Test Cases ***
LoginTest
    Open browser    ${ecommerceURL}}    ${browser}
    LoginToApplication
    #Click link    ${LINK_TEXT}
    #CountLists
    #FindH2Elements


*** Keywords ***
loginToApplication
    Click element    ${clickMyAccount}
    Click element    ${LOGIN BUTTON IN MENU BAR}
    Input text    ${EMAIL_ADDRESS_TEXTBOX}    ${email}
    Input text    ${PASSWORD_TEXTBOX}    ${password}
    Click button    ${LOGIN_BUTTON}
    Wait until element is visible    ${MY_ACCOUNT_TEXT}
    Element should contain    ${MY_ACCOUNT_TEXT}    My Account

countLists
    ${countElements}=    Get length    ${element}
    Log    ${countElements}

findH2Elements
    ${H2_TAGS}=    Get WebElements    tag:h2
    Log    ${H2_TAGS}
#    FOR    ${H2}    IN    ${H2_TAGS}
#        ${text}=  Get text    ${H2}
#        Log    ${text}
#    END
