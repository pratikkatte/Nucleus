import os
import subprocess
import shlex
import argparse
import re
import random
import subprocess

from data_viz.planner import plan
from terminal.suggestion import session, PLACEHOLDER
from terminal.planner import QueryManager
from nucleus.tools import MessagePrinter
from nucleus.logger import log

# data viz server
from data_viz.server import FastAPIServer
from data_viz.app import app


data_viz_server = FastAPIServer(app)
app.state.server_instance = data_viz_server

data_viz_server.start()

file_requirements = {
    '.bam': "",
    '.bai': "",
    '.fa': "",
    '.fai': ""
}

def args_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("--openai-api-key",  help="Specify the OpenAI API key")
    parser.add_argument("--anthropic-api-key", help="Specify the Anthropic API key")
    args = parser.parse_args()

    model, api_key = None, None

    input_vals = {
        'LLM': []
    }

    if args.openai_api_key:
        model = 'openai'
        api_key = args.openai_api_key

        input_vals['LLM'] = [{
            'model': model, 
            "api_key": api_key
            }]
        
        os.environ["OPENAI_API_KEY"] = api_key
        
        return input_vals
    
    if args.anthropic_api_key:
        model = "anthropic"
        api_key = args.anthropic_api_key

        os.environ["ANTHROPIC_API_KEY"] = api_key

        input_vals['LLM'] = [{
            'model': model, 
            "api_key": api_key
            }]
        
        return input_vals

    openai_api_key = os.getenv("OPENAI_API_KEY")
    anthropic_api_key = os.getenv("ANTHROPIC_API_KEY")
    gemini_api_key = os.getenv("GEMINI_API_KEY")
    
    

    if openai_api_key:
        model='openai'
        api_key = openai_api_key
        
        input_vals['LLM'].append({
            "model":model,
            "api_key": api_key
        })
    
    if anthropic_api_key:
        model='anthropic'
        api_key = anthropic_api_key

        input_vals['LLM'].append({
            "model":model,
            "api_key": api_key
        })
    
    if gemini_api_key:
        model='gemini'
        api_key = gemini_api_key

        input_vals['LLM'].append({
            "model":model,
            "api_key": api_key
        })
    
    return input_vals
    
def main():
    """
    """

    input_vals = {}

    input_args = args_parser()
    
    if not len(input_args['LLM']):
        log.error("Error: No API key provided. Please provide an API key to proceed.")
        return

    if len(input_args['LLM'])==1:
        input_vals['LLM'] = input_args['LLM'][0]

    if len(input_args["LLM"])>1:
        log.warning("Multiple API keys found in your environment variables, but none explicitly provided.")
        llm = random.choice(input_args["LLM"])
        log.info(f"Randomly selected API key for the model '{llm['model']}'.")
        input_vals['LLM'] = llm

    message_printer = MessagePrinter()

    message_printer.system_message("\nExecute terminal commands with prefix '!'. Ask questions as usual. Ask questions as usual.")
    message_printer.system_message("Type 'exit' or 'quit' to terminate the program. \n")


    query_responder = QueryManager(input_vals, message_printer)
    while True:
        try:
            # Prompt for user input

            user_input = session.prompt("\n> ", placeholder=PLACEHOLDER)

            # Check if the user wants to exit
            if user_input.lower() == "":
                continue

            if user_input.lower() in ["exit", "quit"]:
                data_viz_server.stop()
                message_printer.system_message("Exiting shell. Goodbye!")
                break

            if user_input.lower()[0] in "!":
                # handle 'cd' command to change directory
                user_input = user_input[1:]
                if user_input.startswith("cd"):
                    parts = shlex.split(user_input)
                    if len(parts) > 1:
                        new_dir = parts[1]
                    else:
                        new_dir = os.path.expanduser("~")
                    try:
                        os.chdir(new_dir)
                    except FileNotFoundError:
                        print(f"cd: {new_dir}: No such file or directory")
                    except Exception as e:
                        print(f"cd: {e}")
                else:
                    subprocess.run(shlex.split(user_input), check=False)

            elif user_input.startswith("/show"):
                file_input = user_input.split("/show", 1)[-1].strip()
                config = plan(file_input, session, message_printer)
                if config:
                    # data_queue.put(config)
                    data_viz_server.send_data(config)

                    message_printer.system_message("You can view the file at http://localhost:8000")
                else:
                    message_printer.system_message("\n Provided file doesn't exist.")
                    continue

            elif user_input == "/close":
                data_viz_server.stop()

            else:
                query_responder.execute_query(user_input)

        except KeyboardInterrupt:
            data_viz_server.stop()
            message_printer.system_message("\n Exiting shell. Goodbye!")
            break
        except Exception as e:

            log.error(f"Error : {e}")

if __name__ == "__main__":
    main()