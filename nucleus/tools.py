from rich.markdown import Markdown
from rich.console import Console
from rich.text import Text
from langchain_openai import ChatOpenAI
import re
import subprocess

from nucleus.logger import log

console = Console()

class MessagePrinter:
    def __init__(self):
        self.console = Console()
        self.style="#fafcfb"

    def system_message(self, message):
        """
        Prints a system message with specific styling.
        """
        system_text = Text(message, style="yellow")
        self.console.print(system_text)

    def user_message(self, message):
        """
        Prints a user message with Markdown rendering.
        """
        user_text = Text(f"{message}")
        self.console.print(user_text, style=self.style)

    def assistant_message(self, message, type=None):
        """
        Prints an assistant message with optional Markdown rendering.
        """
        if type=='command':
            print("\n"+ message)
        else:
            # pprint(message)
            assistant_text = Markdown(f"<br>{message}")
            self.console.print(assistant_text)

def command_provider(message , model_name):
    """
    """

    llm = None

    if model_name == 'openai':
        llm = ChatOpenAI(
                model="gpt-4o",
                temperature=0,
                max_tokens=None,
                timeout=None,
                max_retries=2
            )
        
    if llm is not None:
        message = f"Be precise in your response. Here is the question: {message}"
        response = llm.invoke(message)
    else:
        return "No LLM chosen"
    
    return response.content

def format_message(message, role):
    """
    """
    if role=='user':
        return (
            'human', message
        )
    else:
        return (
            'assistant', message
        )



def get_response(response, message_printer):

    try:
        # print_response(response)

        message_printer.assistant_message(response)
   
        command = extract_command(response)
        if command:
            # ask
            if confirm_ask():
                # print_response(command)
                result = subprocess.run(command, shell=True, capture_output=True, text=True)

                if result.returncode==0:
                    
                    # print_response(f"command executed \n {result.stdout}", type='command')
                    message_printer.assistant_message(f"command executed \n {result.stdout}", type='command')
                else:
                    message_printer.assistant_message(result.stderr, type='command')
                    # print_response(result.stderr, type='command')
    except Exception as e:
        log.error("Error in get_response", e)

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

# Example usage
if __name__ == "__main__":
    printer = MessagePrinter()

    # Print system messages
    printer.print_system_message("Type commands as usual. Ask anything you want.")
    printer.print_system_message("Type 'exit' or 'quit' to stop the program.\n")

    # Print user message
    printer.print_user_message("Hello, how do I use this program?")

    # Print assistant message
    printer.print_assistant_message("Sure! Let me explain how it works.")

    # Print messages with Markdown rendering
    printer.print_user_message("### This is a Markdown heading")
    printer.print_assistant_message("**This text is bold in Markdown**")

