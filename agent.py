from config import SYSTEM_PROMPT, Settings
from openai import OpenAI
from tool_schemas import tools
from tools import web_search, read_url, write_report
import json

class ResearchAgent:
    def __init__(self):
        self.settings = Settings()

        self.client = OpenAI(
            api_key=self.settings.openai_api_key.get_secret_value(),
            base_url=self.settings.openai_api_base
        )

        self.tool_map = {
            "web_search": web_search,
            "read_url": read_url,
            "write_report": write_report
        }

        self.messages = [
            {"role": "system", "content": SYSTEM_PROMPT}
        ]

    def run(self, user_input):
        self.messages.append(
            {"role": "user", "content": user_input}
        )

        for step in range(self.settings.max_iterations):
            # try:
            response = self.client.chat.completions.create(
                model=self.settings.openai_lm_model,
                messages=self.messages,
                temperature=self.settings.temperature,
                tools=tools,
                tool_choice="auto",
                parallel_tool_calls=True
            )

            message = response.choices[0].message
            self.messages.append(message)

            if not message.tool_calls:
                return message.content
            
            for tool_call in message.tool_calls:
                args = json.loads(tool_call.function.arguments)
                name = tool_call.function.name

                print(f"\n🔧 Tool call: {name}({args})")

                tool = self.tool_map[name]

                try:
                    result = tool(**args)
                except Exception as e:
                    result = f"Tool error: {e}"

                print(f"📎 Result: {str(result)[:200]}")

                self.messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": str(result)
                })

        return "Max iterations reached"
    # while True:
    #     call LLM
    #     if tool_call:
    #         execute tool
    #         append result