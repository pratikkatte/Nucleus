from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic



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
            api_key=input_dict['api_key']
        )

    if model_name == 'anthropic':
        llm = ChatAnthropic(
            model="claude-3-opus-20240229",
            temperature=0,
            api_key=input_dict['api_key']
        )

    return llm