from app import transit_to_qualitative, transit_to_keywords, transit_to_analysis, transit_to_insights


class WorkflowManager:

    @classmethod
    def extract_keywords(cls):
        transit_to_qualitative()

    @classmethod
    def extract_questions(cls):
        transit_to_keywords()

    @classmethod
    def run_processing(cls):
        transit_to_analysis()

    @classmethod
    def complete_processing(cls):
        transit_to_insights()
