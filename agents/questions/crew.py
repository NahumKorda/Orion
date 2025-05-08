from typing import Literal

from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from pydantic import BaseModel, Field


class OutputAnswer(BaseModel):
	answer: str = Field(..., description="Answer option of a survey question.")
	value: float = Field(..., description="Count or percentage that the answer received in a survey.")


class OutputQuestion(BaseModel):
	question: str = Field(..., description="A survey question.")
	data_type: Literal["count", "percent"] = Field(..., description="Data type of the values received for the answer options.")
	answers: list[OutputAnswer] = Field(..., description="List of answer options provided for a survey question.")


class OutputJSON(BaseModel):
	questions: list[OutputQuestion] = Field(..., description="A list of all questions and their answer options with values extracted from survey results.")


@CrewBase
class SurveyAnalyzingCrew:

	@agent
	def survey_analyst(self) -> Agent:
		return Agent(
			config=self.agents_config['survey_analyst'],
			verbose=True,
		)

	@task
	def survey_result_analysis(self) -> Task:
		return Task(
			config=self.tasks_config['survey_result_analysis'],
			output_json=OutputJSON,
			output_format="json"
		)

	@crew
	def crew(self) -> Crew:
		return Crew(
			agents=self.agents,
			tasks=self.tasks,
			process=Process.sequential,
			verbose=True,
		)
