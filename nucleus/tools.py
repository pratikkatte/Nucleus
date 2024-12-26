from nucleus.models import load_model
from nucleus.prompts import model_prompt
from rich.markdown import Markdown
from rich.console import Console
import re
import subprocess

console = Console()


def format_message(message, role):

    if role=='user':
        return (
            'human', message
        )
    else:
        return (
            'assistant', message
        )
    

def command_provider(input_dict):
    """
    Define the task to be executed when the keyword is typed.
    """
    main_model = load_model(input_dict)

    get_response(main_model, input_dict['message'])


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
