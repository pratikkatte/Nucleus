#!/usr/bin/env python3

import warnings
warnings.filterwarnings("ignore", module="langsmith.client")

from langchain_openai import ChatOpenAI
from langchain.agents import AgentExecutor, create_react_agent
from langchain import hub
import os
import subprocess
from langchain.agents import tool

import sys


def get_confirmation(command):
    confirmation = input(f"\nAbout to execute command: {command}\n\n Do you want to proceed? (y/n): ")
    print(confirmation)
    return confirmation.lower().strip() == 'y'

@tool(return_direct=True)
def run_shell_command(command: str) -> str:
    
    """Return the command explicitly. Do not say anything else."""
    return command
    # if not get_confirmation(command):
    #     print(f"\nCommand: {command}\n")
    #     print("\n Print 'exit' if you want to just copy the generated command")
    #     command = input(f"edit the command: ")

    #     if command.lower()=='exit':
    #         return "User exited"

    # print("\nThanks for confirmation. Executing the command\n")
    # try:
    #     # Execute the command and capture the output
    #     result = subprocess.run(command, shell=True, check=True, text=True, capture_output=True)
    #     return result.stdout
    # except subprocess.CalledProcessError as e:
    #     return f"An error occurred while executing the command: {e}"
    



if __name__=='__main__':

    if not 'OPENAI_API_KEY' in os.environ:
        print(f"""\nERROR: Please set the OPENAI_API_KEY in your environment inorder to use this software.\n 
              export OPENAI_API_KEY="your_api_key_here"
              """)
    else:        
        if len(sys.argv)<2:
            print("""Provide your query: nucleus <your query>""")
        else:

            query = sys.argv[1]
            
            llm = ChatOpenAI(model="gpt-4o")
            prompt_template = hub.pull("hwchase17/react")
            
            tools = [run_shell_command]
            
            agent = create_react_agent(llm, tools, prompt_template)
            agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=False , handle_parsing_errors=True)
            
            answer = agent_executor.invoke({"input": query})

            print(f"Here's the command for your query:\n {answer['output']} \n")