import hvplot.pandas
import numpy as np
import panel as pn
import pandas as pd
import openai
from llama_index import VectorStoreIndex, download_loader
from langchain.agents import initialize_agent, Tool
from langchain.llms import OpenAI
from langchain.chains.conversation.memory import ConversationBufferMemory
from panel.chat import ChatInterface
import time
pn.extension("perspective")

def callback(contents: str, user: str, instance: pn.chat.ChatInterface):
    message = f"Echoing {user}: {contents}"
    return message
chat_interface = pn.chat.ChatInterface(callback=callback)
msg_panel = chat_interface.send(
    "Enter a WEB link and ask anything!-\nNote: images in the link will be ignored!!!",
    user="assistant",
    respond=False,
)
apikey = pn.widgets.TextInput(name='OPENAI API KEY', placeholder="sk-********")
apply = pn.widgets.Button(name='Apply', button_type='default')
website_url_input = pn.widgets.TextInput(name='Website URL', placeholder="https://www.google.com/")
submit = pn.widgets.Button(name='Submit', button_type='primary')


def on_submit(event, contents, ):

    try:
        SimpleWebPageReader = download_loader("SimpleWebPageReader")

        # Set OpenAI API key
        openai.api_key = apikey.value  # Replace with your actual API key

        # Get the entered website URL
        website_url = website_url_input.value

        if website_url:
            # Initialize SimpleWebPageReader with the provided website URL
            loader = SimpleWebPageReader()
            documents = loader.load_data(urls=[website_url])

            # Create VectorStoreIndex from documents
            index = VectorStoreIndex.from_documents(documents)

            # Initialize LangChain OpenAI
            index = VectorStoreIndex.from_documents(documents)
            llm = OpenAI(openai_api_key=apikey.value, temperature=0, streaming = True
                         )

            # Initialize ConversationBufferMemory
            memory = ConversationBufferMemory(memory_key="chat_history")

            # Initialize agent chain
            tools = [
                Tool(
                    name="Website Index",
                    func=lambda q: index.as_query_engine(),
                    description="Useful when you want to answer questions about the text on websites.",
                ),
            ]


            query_engine = index.as_query_engine()
            response = query_engine.query(contents)

            return str(response),

    except Exception as e:
        print(f"Error: {e}")
def even_or_odd(contents, user, instance):
    response_tuple = on_submit(event='', contents=contents)

    # Extracting the first element of the tuple and converting it to a string
    response_string = str(response_tuple)

    return response_string
# Set the callback function for the button click event
submit.on_click(on_submit)

# Instantiate the template with widgets displayed in the sidebar
template = pn.template.FastListTemplate(
    title='Chat with Web',
    sidebar=[apikey,website_url_input, submit,
             msg_panel],
    header=[],

)

ChatInterface(callback=even_or_odd)
def callback(contents: str, user: str, instance: pn.chat.ChatInterface):
    message = query_engine.query(contents)
    return message

template.main.append(

    ChatInterface(
        callback=even_or_odd,
        user="User",
        avatar="🧑",
        callback_user="System",
    )
)

# Display the app
template.servable()