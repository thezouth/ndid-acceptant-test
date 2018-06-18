Feature: Create new Identity
    Scenario: Identity is new in environment
        Given User enters IdP
        When User creates a new identity
        Then System successfully created the new id
