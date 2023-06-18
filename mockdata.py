# Mock data was generated through https://platform.openai.com/playground
# using the prompt in gen_prompt in main.py

# Query: "I want to go book shopping Wednesday afternoon for an hour.
#  And then I want to go to a 20-minute yoga class either Monday night or Friday night."
mock_data_0 = {
        "events": [
            {
                "eventName": "Book shopping",
                "duration": 60,
                "possibleIntervals": [
                    {
                        "date": "2023-06-21",
                        "timePeriod": {
                            "startTime": "13:00",
                            "endTime": "17:00"
                        }
                    }
                ]
            },
            {
                "eventName": "Yoga class",
                "duration": 20,
                "possibleIntervals": [
                    {
                        "date": "2023-06-19",
                        "timePeriod": {
                            "startTime": "18:00",
                            "endTime": "22:00"
                        }
                    },
                    {
                        "date": "2023-06-23",
                        "timePeriod": {
                            "startTime": "18:00",
                            "endTime": "22:00"
                        }
                    }
                ]
            }
        ]
    }

# Query: "I would like to schedule 10-minute mental health breaks on Wednesday around lunchtime."
mock_data_1 = {
  "events": [
    {
      "eventName": "Mental Health Break",
      "duration": 10,
      "possibleIntervals": [
        {
          "date": "2023-06-21",
          "timePeriod": {
            "startTime": "12:00",
            "endTime": "12:30"
          }
        }
      ]
    }
  ]
}

# Query: "Hey, I need to do my laundry sometime Friday before 6pm. Also hold space for 3 hours on Tuesday evening for
# me to  finish my essay."
mock_data_2 = {
  "events": [
    {
      "eventName": "Laundry",
      "duration": 120,
      "possibleIntervals": [
        {
          "date": "2023-06-23",
          "timePeriod": {
            "startTime": "12:00",
            "endTime": "18:00"
          }
        }
      ]
    },
    {
      "eventName": "Essay Writing",
      "duration": 180,
      "possibleIntervals": [
        {
          "date": "2023-06-20",
          "timePeriod": {
            "startTime": "18:00",
            "endTime": "21:00"
          }
        }
      ]
    }
  ]
}

mock_data_arr = [mock_data_0, mock_data_1, mock_data_2]


def get_mock_data(user_input):
    index = int(user_input)
    return mock_data_arr[index]