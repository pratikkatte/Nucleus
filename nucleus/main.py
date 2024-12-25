import os
import subprocess
import shlex
import sys
import argparse
import re
import random
import subprocess
import readline
from tools import command_provider





def completer(text, state):
    """
    Tab completion logic for files, directories, and commands.
    """
    # Get the current input buffer
    line = readline.get_line_buffer().split()

    # If completing the first word, look for commands
    if len(line) == 1:
        options = [cmd for cmd in os.listdir(os.getcwd()) if cmd.startswith(text)]
    else:
        # For subsequent words, complete file and directory names
        options = [f for f in os.listdir(os.getcwd()) if f.startswith(text)]

    return options[state] if state < len(options) else None

def setup_readline():
    """
    Configure readline for tab completion.
    """
    readline.parse_and_bind("tab: complete")
    readline.set_completer(completer)





def extract_command(text):
    """
    Extracts a command from a text block surrounded by triple backticks and in bash syntax.
    
    Args:
        text (str): The input text containing the command.
        
    Returns:
        str: The extracted command, or None if no command is found.
    """
    match = re.search(r"```bash\n(.+?)```", text, re.DOTALL)
    if match:
        return match.group(1).strip()
    return None


def confirm_ask():
    """
    Prompt the user to decide whether to run or not.
    """
    ask_text = "\n[bold cyan]Do you want to run?[/bold cyan] [green](Yes or No):[/green] "
    # console.print(ask_text, end=" ")
    response = console.input(ask_text).strip().lower()
    if response in ['yes', 'y']:
        return True
    elif response in ['no', 'n']:
        return False
    else:
        print("Invalid input. Please respond with 'Yes' or 'No'.")
        confirm_ask()  # Re-prompt the user





def args_parser():

    # input_vals = {
    #  'model':'openai',
    #  'api':''
    # }
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
        
        return input_vals
    
    if args.anthropic_api_key:
        model = "anthropic"
        api_key = args.anthropic_api_key

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

    # openai_api_key = os.getenv("OPENAI_API_KEY")
    # if openai_api_key is None and args.openai_api_key is None:
    #     input_vals = {}
    # else:
    #     input_vals['api'] = api_key
    # return input_vals
    
def main():
    
    setup_readline()

    input_vals = {}

    input_args = args_parser()
    if not len(input_args['LLM']):
        print("Provide API-KEY...")
        return

    if len(input_args['LLM'])==1:
        input_vals = input_args['LLM'][0]

    if len(input_args["LLM"])>1:
        print("You have not provided the api-key but found two api-keys in your environment variable.")
        llm = random.choice(input_args["LLM"])
        print(1)
        print(f"randomly chose model {llm['model']}")
        input_vals['LLM'] = llm

    print("Type commands as usual. ask anything u want")
    print("Type 'exit' or 'quit' to stop the program.\n")

    while True:
        try:
            # Prompt for user input
            user_input = input("> ")

            # Check if the user wants to exit
            if user_input.lower() in ["exit", "quit"]:
                print("Exiting custom shell. Goodbye!")
                break

            if user_input.lower()[0] in "/!":
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

                # Run other normal terminal commands
                else:
                    subprocess.run(shlex.split(user_input), check=False)
            else:
                input_vals['message'] = user_input
                command_provider(input_vals)
                

        except KeyboardInterrupt:
            print("\n Exiting custom shell. Goodbye!")
            break
        except Exception as e:
            print(f"Error: {e}")


if __name__ == "__main__":
    main()