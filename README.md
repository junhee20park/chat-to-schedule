# TimeFinder
TimeFinder is like a personal assistant for your calendar. Talk to TimeFinder about what you want to do, and it'll automatically find the perfect place on your calendar for it.

### Sample Query Examples
"I need to do Laundry on Wednesday before 4pm, but it's probably going to take 2 hours or more."
https://github.com/junhee20park/time-finder/assets/69227966/7b8a5704-bcaf-42f9-9a96-caa3d0ec633b

"Schedule a grocery shopping trip sometime Thursday night, maybe 1 hour or so."
https://github.com/junhee20park/time-finder/assets/69227966/136ab0dd-b845-41ba-8c75-3e0778fa7a68

"Find me 3 hours sometime Monday night or Tuesday night so I can work on my project."


### Technical Aspects
TimeFinder parses user input into a JSON file through the OpenAI API (GPT3.5).
It uses Google Cloud Platform to make calls to the Google Calendar API.

###### Prompt Engineering
After multiple attempts, I found the following query worked best at outputting consistent JSON file formats:
> Generate a JSON file that is an array of events named 'events'. Each event has the following fields: eventName, duration (in minutes), possibleIntervals[ { date, timePeriod: {startTime, endTime} ]. timePeriod indicates the full range of time that event could happen. startTime and endTime are in “HH:MM” format. Today is {Sunday 2023-06-18}. Query: {user input}


### To-Do
- Build front-end for easy use
- Add speech-to-text input method
- Add location to events
- Solve prompt engineering problem of GPT not being able to understand recurring events (such as "Find me a 10-minute block Monday, Tuesday and Wednesday"
