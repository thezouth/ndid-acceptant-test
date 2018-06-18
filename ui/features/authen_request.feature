Feature: Authentication Request
    Background: Ensure user Roofimon is in system
        Given Ensure user `Roofimon` is in system

    Scenario: Request success without AS
        When Roofimon request to verify identity
        And Roofimon successfully authenticate with IdP
        And Roofimon approve the request
        Then The request become fullfiled
