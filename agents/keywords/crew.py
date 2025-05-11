from typing import Literal

from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from pydantic import BaseModel, Field


class OutputJSON(BaseModel):
	keywords: list[str] = Field(..., description="A list of extracted keywords.")


@CrewBase
class KeywordExtractingCrew:

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
