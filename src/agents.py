from datetime import datetime
from urllib import response
from aisuite import Client
from src.research_tools import (
    arxiv_search_tool,
    tavily_search_tool,
    wikipedia_search_tool,
)

client = Client()


# === Research Agent ===
def research_agent(
    prompt: str, model: str = "openai:gpt-4.1-mini", return_messages: bool = False
):
    print("==================================")
    print("🔍 Research Agent")
    print("==================================")

     current_time = datetime.now().strftime('%Y-%m-%d')
    
    ### START CODE HERE ###

    # Create a customizable prompt by defining the role (e.g., "research assistant"),
    # listing tools (arxiv_tool, tavily_tool, wikipedia_tool) for various searches,
    # specifying the task with a placeholder, and including a current_time placeholder.
    prompt = f"""
    
    You are a research agent.
    
    Task: {task}, Current time: {current_time}
    
    Your goal:
    1. Determine what the topic is from the task 
    2. Explore the current consensus understanding and information of the topic by using the tools available to you.
    3. Summarize your findings and highlight key findings
    
    Tools for you
    
    arxiv_search_tool(query) → search academic papers from arXiv

    tavily_search_tool(query) → perform web searches with the Tavily API

    wikipedia_search_tool(query) → retrieve summaries from Wikipedia
    
    Output:
    Summarize your findings and highlight key findings
    Be sure to add references to statements

    """
    
    # Create the messages dict to pass to the LLM. Remember this is a user prompt!
    messages = [{"role": "user", "content": prompt}]

    # Save all of your available tools in the tools list. These can be found in the research_tools module.
    # You can identify each tool in your list like this: 
    # research_tools.<name_of_tool>, where <name_of_tool> is replaced with the function name of the tool.
    tools = [research_tools.arxiv_search_tool,research_tools.tavily_search_tool,research_tools.wikipedia_search_tool]
    
    # Call the model with tools enabled
    response = CLIENT.chat.completions.create(  
        # Set the model
        model=model,
        # Pass in the messages. You already defined this!
        messages=messages,
        # Pass in the tools list. You already defined this!
        tools=tools,
        # Set the LLM to automatically choose the tools
        tool_choice=model,
        # Set the max turns to 6
        max_turns=5
    )  
    
    ### END CODE HERE ###

    content = response.choices[0].message.content
    print("✅ Output:\n", content)
    return (content, messages) if return_messages else content 

    except Exception as e:
        print("❌ Error:", e)
        return f"[Model Error: {str(e)}]", messages


def writer_agent(
    prompt: str,
    model: str = "openai:gpt-4.1-mini",
    min_words_total: int = 2400,
    min_words_per_section: int = 400,
    max_tokens: int = 15000,
    retries: int = 1,
):
    print("==================================")
    print("✍️ Writer Agent")
    print("==================================")

    ### START CODE HERE ###
    
    # Create the system prompt.
    # This should assign the LLM the role of a writing agent specialized in generating well-structured academic or technical content
    system_prompt = f"""
    
    You are an expert, educated writer. 
    Present the context in an objective and organized report. 
    Be concise and correct based on the facts given to you. 
    Be sure to use all of the research material given to you
    and cite the sources.

    Output of the report should be in a well structured format with sections and subsections. 
    The report should be detailed and self-contained.
    Use HTML markdown formatting to structure the report.

    The report should be in this format:
    # Title
    ## Summary
    ## Key Findings
    ## Discussion
    ## Conclusion
    ## References
    
    """

    # Define the system msg by using the system_prompt and assigning the role of system
    system_msg =   {
            "role": "system",
            "content": system_prompt
        }

    # Define the user msg. In this case the user prompt should be the task passed to the function
    user_msg = {"role": "user", "content": task}

    # Add both system and user messages to the messages list
    messages = [system_msg, user_msg]
    
    ### END CODE HERE ###

    response = CLIENT.chat.completions.create(
        model=model, 
        messages=messages,
        temperature=1.0
    )

    return response.choices[0].message.content


def editor_agent(
    prompt: str,
    model: str = "openai:gpt-4.1-mini",
    target_min_words: int = 2400,
):
    print("==================================")
    print("🧠 Editor Agent")
    print("==================================")

    ### START CODE HERE ###

    # Create the system prompt.
    # This should assign the LLM the role of an editor agent specialized in reflecting on, critiquing, or improving existing drafts.
    system_prompt = f"""
    
    Critique the given task
    
    Task: {task}
    
    Ensure it is correct and concise and 
    can be easy to understand. Remove any redunancy and make statements clearer if needed.
    Make sure all citations are provided and correct. Ensure the report is well structured and organized.
    
    """
    
    # Define the system msg by using the system_prompt and assigning the role of system
    system_msg = {
        "role": "system",
        "content": system_prompt
    }
    
    # Define the user msg. In this case the user prompt should be the task passed to the function
    user_msg = {"role": "user", "content": task}
    
    # Add both system and user messages to the messages list
    messages = [system_msg, user_msg]
    ### END CODE HERE ###
    
    response = CLIENT.chat.completions.create(
        model=model, 
        messages=messages,
        temperature=0.7 
    )
    
    return response.choices[0].message.content