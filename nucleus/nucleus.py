import os
import subprocess
import shlex
import sys
import argparse
from langchain_openai import ChatOpenAI
import re
from rich.console import Console
from rich.markdown import Markdown
import subprocess
import readline




console = Console()

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

def load_model(input_dict):
    """
    """
    model_name = input_dict['model']
    if model_name == 'openai':
        llm = ChatOpenAI(
            model="gpt-4o",
            temperature=0,
            max_tokens=None,
            timeout=None,
            max_retries=2,
            api_key=input_dict['api']
        )
    return llm

def model_prompt():
    return (
        "system",
        "You are a helpful assistance. Help user to write biotools commands based the query. \
            if the user types a terminal command then respond with the same command bash block back  \
            \
            Here's an example text. \
            1. USER convert haplotype.sam file to haplotype.bam \
                ASSISTANT  samtools view -S -b haplotype.sam > haplotype.bam \
            "
            )

def format_message(message, role):

    if role=='user':
        return (
            'human', message
        )
    else:
        return (
            'assistant', message
        )
    

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

def print_response(text, type=None):
    """
    """
    print()
    if type=='command':
        print(text)
        print()
        return
    
    md = Markdown(text)
    console.print(md, style="#fafcfb")
    print()

def get_response(model, user_input):
    message = []
    message.append(model_prompt())
    message.append(format_message(user_input, role='user'))
    response = model.invoke(message)

    print_response(response.content)

    command = extract_command(response.content)
    if command:
        # ask
        if confirm_ask():
            # print_response(command)
            result = subprocess.run(command, shell=True, capture_output=True, text=True)

            if result.returncode==0:
                
                print_response(f"command executed \n {result.stdout}", type='command')
            else:
                print_response(result.stderr, type='command')
            

def command_provider(input_dict):
    """
    Define the task to be executed when the keyword is typed.
    """
    main_model = load_model(input_dict)

    get_response(main_model, input_dict['message'])


def args_parser():

    input_vals = {
     'model':'openai',
     'api':''
    }
    parser = argparse.ArgumentParser()
    parser.add_argument("--openai-api-key", help="OpenAI API Key")
    args = parser.parse_args()

    api_key = os.getenv("OPENAI_API_KEY")

    if api_key is None and args.openai_api_key is None:
        print("Exception: Provide openai-api-key")
        return None
    else:
        input_vals['api'] = api_key

    return input_vals
    

def main():
    
    setup_readline()

    input_vals = args_parser()
    if not input_vals:
        return
    
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