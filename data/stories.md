## happy path
* greet
  - utter_greet
* mood_great
  - utter_happy

## sad path 1
* greet
  - utter_greet
* mood_unhappy
  - utter_cheer_up
  - utter_did_that_help
* affirm
  - utter_happy

## sad path 2
* greet
  - utter_greet
* mood_unhappy
  - utter_cheer_up
  - utter_did_that_help
* deny
  - utter_goodbye

## say goodbye
* goodbye
  - utter_goodbye

## bot challenge
* bot_challenge
  - utter_iamabot

## state_covid_path
* state_cases
  - state_covid_case
  - form{"name":"state_covid_case"}
  - form{"name":null}
  - utter_question
 
## country_covid_path
* country_cases
  - country_covid_case
  - form{"name":"country_covid_case"}
  - form{"name":null}
  - utter_question1
 
## pincode_covid_path
* pincode_cases
  - pin_covid_case
  - form{"name":"pin_covid_case"}
  - form{"name":null}
  - utter_question2
 
## pincode_covid_path
* dist_cases
  - dist_covid_case
  - form{"name":"dist_covid_case"}
  - form{"name":null}
  - utter_question3
 
 ## corona_cases
 * corona_cases
  - utter_cases