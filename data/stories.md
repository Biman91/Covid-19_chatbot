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
  - action_joke

## story_joke_01
* joke
  - action_joke
  
## abhay_name_1
* abhay_name
  - utter_abhay
 
## Form_path
* form_details
  - covid_form
  - form{"name":"covid_form"}
  - form{"name":null}
  - utter_slots_values
  
## covid_path
* covid
  - covid_case
  - form{"name":"covid_case"}
  - form{"name":null}
  - utter_question
