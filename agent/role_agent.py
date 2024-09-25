import json
from typing import Dict, Any
from langchain_core.messages.ai import AIMessage
from services.model_service import ModelService
from utils.general.helpers import get_current_utc_datetime


class RoleAgent:

    def __init__(self, role: str, ollama_service: ModelService, sys_prompt: str = ""):
        self.role = role
        self.ollama_service = ollama_service
        self.sys_prompt = sys_prompt

    def invoke_model(self, user_prompt: str):
        """
        Prepare the payload, send the request to the model, and process the response.
        """
        # Prepare the payload
        payload = self.ollama_service.prepare_payload(
            user_prompt,
            self.sys_prompt,
        )

        # Invoke the model and get the response
        response_json = self.ollama_service.request_model_generate(
            payload,
        )

        # Process the model's response
        response_content = self.ollama_service.process_model_response(response_json)

        # Return the processed response
        return response_content

    def work(
        self,
        user_request: str,
    ) -> str:
        """
        Execute a simple task based on the user's request.
        """

        user_prompt = f"""<|start_header_id|>user<|end_header_id|>\n\n{user_request}<|eot_id|>
            <|start_header_id|>assistant<|end_header_id|>"""

        # Invoke the model with the user's request
        response = self.invoke_model(user_prompt=user_prompt)

        # Return the processed response
        return {
            f"{self.role}_response": AIMessage(content=response),
        }
