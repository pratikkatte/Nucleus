import os
from pydantic import BaseModel, Field
from typing import List
import enum
from langchain_openai import ChatOpenAI
from nucleus.tools import get_response, format_message
from langchain_core.prompts import ChatPromptTemplate
from nucleus.logger import log
from nucleus.tools import command_provider
from nucleus.prompts import model_prompt, planner_prompt

class ComputeQuery(BaseModel):
    """
    computation of a query
    """
    query: str
    response: dict = {}
    done: bool = False

    def execute(self, input_dict):
        """
        """
        message = []
        message.append(model_prompt())
        message.append(format_message(self.query, role='user'))

        model_name = input_dict["LLM"]['model']
        try:
            result = command_provider(self.query, model_name)
            self.response = result
            if self.response:
                self.done = True
        except Exception as e:
            log.error("Exception in compute query", e)


class MergedResponses(BaseModel):
    """
    Models a merged response of multiple queries.
    Currently we just concatinate them but we can do much more complex things.
    """
    dependent_queries: list[ComputeQuery]
    query: str = '...'

    def execute(self, input_dict):
        """
        """
        prompt = ""
        for dependent in self.dependent_queries:
            prompt += f"Assistant: {dependent.query} \n"
            prompt += f"User: {dependent.response} \n"


        # prompt = ""
        # "\n".join([f"Question: {subquries.query} \n Answer: {subquries.response}"  for subquries in self.dependent_queries])
        
        self.query = f"These are the list of questions and its' responses. {prompt} Based on this, answer this Question: {self.query}"

        merger_query = ComputeQuery(query=self.query)
        merger_query.execute(input_dict)

        return merger_query

class QueryType(str, enum.Enum):
    """
    Enumeration representing the types of queries that can be asked to a question answer system.
    """
    # When i call it anything beyond 'merge multiple responses' the accuracy drops significantly.
    SINGLE_QUESTION = "SINGLE"
    MULTI_DEPENDENCY = "MULTI_DEPENDENCY"

class QueryTask(BaseModel):
    """
    """
    id: int = Field(..., description="unique id to the query")
    query: str = Field(default=None, description="the sub query")
    dependencies: list[int] = Field(
        default = [],
        description="no of dependecies to respond to this query"
    )
    query_type: QueryType = Field(
        default=QueryType.SINGLE_QUESTION,
        description="Type of question, either a single question or a multi question merge when there are multiple questions",
    )
    
    answer : str = ""
    completed: str = False

    def execute(self, input_dict, dependency_func):

        if self.completed:
            return self.answer
    
        if self.query_type == QueryType.SINGLE_QUESTION:
            compute_query = ComputeQuery(query=self.query,)
            compute_query.execute(input_dict)
            self.completed = True

            self.answer = compute_query

            return self.answer
        else:
            sub_queries = dependency_func(self.dependencies)
            computed_queries = [q.execute(input_dict, dependency_func) for q in sub_queries]

            merge_responses = MergedResponses(query=self.query, dependent_queries=computed_queries)
            
            self.answer = merge_responses.execute(input_dict)
            self.completed = True
            return self.answer

class QueryPlanner(BaseModel):
    """
    """
    query_tasks: List[QueryTask] = Field(..., description="List of subqueries to the main from the user.")

    def dependencies(self, idz: list[int]) -> list[QueryTask]:
        """
        Returns the dependencies of the query with the given id.
        """
        return [q for q in self.query_tasks if q.id in idz]

    def execute(self, input_dict):
        """
        """
        result = []

        for query in self.query_tasks[::-1]:

            if not query.completed:
                query.execute(input_dict,
                    dependency_func=self.dependencies,
                )
                if query.completed:
                    result.append(query.answer)

        return result
     
class QueryManager:
    """
    """
    planner_prompt = ChatPromptTemplate.from_messages(
        planner_prompt()
        )
    

    def __init__(self, input_dict, message_printer):
        """
        """

        self. planner = self.planner_prompt | ChatOpenAI(
            model="gpt-4o", temperature=0,
            ).with_structured_output(QueryPlanner)

        self.input_dict = input_dict
        self.model = input_dict['LLM']['model']
        self.message_printer = message_printer

    def handle_response(self, results):
        """
        """

        if len(results)>1:

            responses = "\n".join([res.response for res in results])
            prompt = "rewrite these: "
            prompt += responses
            prompt += "for this question: \n"
            prompt += self.input_dict['question']
            
            llm = ChatOpenAI(   
                model="gpt-4o",
                temperature=0,
                max_tokens=None,
                timeout=None,
                max_retries=2
            )
            merged_response = command_provider(prompt, self.model)
         
        else:
            merged_response = results[0].response

        get_response(merged_response, self.message_printer)

    def execute_query(self, question):
        """
        """
        try:

            self.input_dict['question'] = question
            plan = self.planner.invoke({"question": question})
            result = plan.execute(self.input_dict)
            
            self.handle_response(result)

        except Exception as e:
            print("error", e)



if __name__ == '__main__':
    while True:
        user_input = input("> ")
        input_dict = {}

        input_dict['LLM'] = {'model':'openai'}
        input_dict['question'] = user_input
        plan = QueryManager(input_dict)
        print()
        plan.execute_query(user_input)

