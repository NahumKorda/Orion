from dotenv import load_dotenv

from agents.keywords.crew import KeywordExtractingCrew
from utils.pdf_reader import get_text


def run():

    load_dotenv()

    survey_results = get_text("/Users/nahumkorda/code/Orion/data/Survey.pdf")

    inputs = {
        'survey_results': survey_results
    }

    result = KeywordExtractingCrew().crew().kickoff(inputs=inputs)
    print(result)

if __name__ == "__main__":
    run()
