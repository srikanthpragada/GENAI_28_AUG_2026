from PySide6.QtWidgets import QApplication, QLabel, QPushButton, QTextBrowser, QTextEdit, QVBoxLayout, QWidget
from PySide6.QtCore import Qt
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain.agents import create_agent
from langchain.chat_models import init_chat_model
from langchain_core.messages import SystemMessage, HumanMessage
import asyncio

from qasync import QEventLoop, asyncSlot


clients = MultiServerMCPClient(
    {"Todos Server": {
        "url": "http://localhost:9999/mcp",
        "transport": "streamable_http"},
     }
)

system_message = SystemMessage(content="""You are a very helpful todos assistant. 
  Filter or classify todos retrieved from a tool based on the user requirement whenever needed. 
  Display output as bullets and display as much information as possible for each todo
  """)


# create agent


async def create_todo_agent():
    tools = await clients.get_tools()
    model = init_chat_model("gemini-2.5-flash", model_provider="google-genai")
    agent = create_agent(model, tools)
    return agent


async def process_request(agent, prompt: str):
    human_message = HumanMessage(prompt)
    response = await agent.ainvoke({"messages": [system_message, human_message]})
    return response["messages"][-1].content


class GreetingApp(QWidget):
    def __init__(self, agent):
        super().__init__()
        self.setWindowTitle("Todos Assistant")
        self.resize(800, 500)
        self.agent = agent

        self.name_input = QTextEdit()
        self.name_input.setPlaceholderText("Ask the todos assistant...")
        self.name_input.setMinimumHeight(120)

        self.greeting_output = QTextBrowser()
        self.greeting_output.setReadOnly(True)

        self.greet_button = QPushButton("Send")
        self.greet_button.clicked.connect(self.show_result)

        layout = QVBoxLayout()
        layout.addWidget(QLabel("Prompt:"))
        layout.addWidget(self.name_input)
        layout.addWidget(self.greet_button)
        layout.addWidget(QLabel("Response:"))
        layout.addWidget(self.greeting_output)

        self.setLayout(layout)

    @asyncSlot()
    async def show_result(self):
        self.greet_button.setEnabled(False)
        try:
            prompt = self.name_input.toPlainText().strip()
            if not prompt:
                return
            self.greeting_output.setMarkdown("**Thinking...**")
            result = await process_request(self.agent, prompt)
            self.greeting_output.setMarkdown(result)
        except Exception as ex:
            self.greeting_output.setPlainText(str(ex))
        finally:
            self.greet_button.setEnabled(True)


async def main():
    # Create the agent before showing the UI
    agent = await create_todo_agent()
   
    window = GreetingApp(agent)
    window.show()
    # Keep the application alive
    await asyncio.Event().wait()


app = QApplication([])
loop = QEventLoop(app)
asyncio.set_event_loop(loop)

with loop:
    loop.create_task(main())
    loop.run_forever()
