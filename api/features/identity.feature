Feature: Create new Identity
    Scenario: : Identity is new in environment
        When User create a new identity
        Then Id Provider successfully created the new identity
        And Underlying block contains identity created block
