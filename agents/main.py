from dotenv import load_dotenv

from agents.crew import QuestionAnsweringCrew


def run():

    load_dotenv()

    inputs = {
        'report': 'Today is a sunny day and the temperature is 32 degrees Celsius.',
        'question': 'What color is sky?'
    }

    result = QuestionAnsweringCrew().crew().kickoff(inputs=inputs)
    print(result)

if __name__ == "__main__":
    run()
