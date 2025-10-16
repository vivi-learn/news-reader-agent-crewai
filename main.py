import dotenv

dotenv.load_dotenv()    # Load environment variables from .env file

from crewai import Crew, Agent, Task
from crewai.project import CrewBase, agent, task, crew
from tools import search_tool, scrape_tool


@CrewBase
class NewsReaderAgent:

    @agent
    def news_hunter_agent(self):
        return Agent(
            config=self.agents_config["news_hunter_agent"], # 뉴스 검색 및 수집 에이전트 구성
            tools=[search_tool, scrape_tool],   # 검색 및 스크래핑 도구 추가
        )

    @agent
    def summarizer_agent(self):
        return Agent(
            config=self.agents_config["summarizer_agent"],
            tools=[
                scrape_tool,
            ],  # 스크래핑 도구 추가
        )

    @agent
    def curator_agent(self):
        return Agent(
            config=self.agents_config["curator_agent"],
        )

    @task
    def content_harvesting_task(self):
        return Task(
            config=self.tasks_config["content_harvesting_task"],
        )

    @task
    def summarization_task(self):
        return Task(
            config=self.tasks_config["summarization_task"],
        )

    @task
    def final_report_assembly_task(self):
        return Task(
            config=self.tasks_config["final_report_assembly_task"],
        )

    @crew
    def crew(self):
        return Crew(
            tasks=self.tasks,
            agents=self.agents,
            verbose=True,
        )

# 실행 예시
result = NewsReaderAgent().crew().kickoff(inputs={"topic": "Cambodia Thailand War."})

# 출력 결과
for task_output in result.tasks_output:
    print(task_output)