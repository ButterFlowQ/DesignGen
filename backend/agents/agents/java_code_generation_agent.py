from typing import List
import json

from agents.types import LLMResponse
from orchestrator.models.models import ChatMessage
from .java_file_code_generation_agent import JavaFileCodeGenerationAgent
from .agent_interface import AgentInterface

class JavaCodeGenerationAgent(AgentInterface):
    """
    An agent responsible for generating java code based on the system design document.
    Takes the complete design document as input and generates actual java code files.
    """

    def __init__(self):
        self.file_generator = JavaFileCodeGenerationAgent()

    def process(self, chat_history: List[ChatMessage]) -> LLMResponse:
        """
        Processes the given chat history by generating LLM messages and querying the LLM for a
        structured response containing generated code files.

        :param chat_history: A list of ChatMessage objects to process.
        :return: An LLMResponse containing the generated code files, communication, dependencies,
                and a boolean indicating whether to move to the next workflow.
        """
        # TODO: check for existence of java LLD
        latest_document_elements = chat_history[-1].current_document.document_elements
        java_lld = latest_document_elements["java LLD"]
        
        # Extract file locations from LLD
        file_locations = self.extract_file_locations(java_lld)
        print(file_locations)
        
        # Generate code for each file
        generated_files = []
        communications = []
        
        for file_location in file_locations:
            # Prepare message for file generator with file location and LLD
            message = {
                "document": latest_document_elements,
                "file name": file_location
            }
            
            # Generate code for this file
            response = self.file_generator.process(json.dumps(message))
            
            # Collect results
            generated_files.append({
                "path": file_location,
                "content": response["updated_doc_element"]
            })
            if response["response_message"]:
                communications.append(f"For {file_location}: {response['response_message']}")
        
        # Return combined results
        return LLMResponse(
            updated_doc_element=generated_files,
            communication="\n".join(communications),
        )
    
    def extract_file_locations(self, java_lld: dict) -> List[str]:
        """
        Extracts file locations from the Java LLD JSON structure.

        :param java_lld: A dictionary representing the Java LLD JSON structure.
        :return: A list of file paths for each class/interface in the LLD.
        """
        file_locations = []

        # Helper function to construct file path
        def construct_file_path(package: str, class_name: str) -> str:
            return f"{package.replace('.', '/')}/{class_name}.java"

        # Iterate over each section in the LLD
        sections = ['controllers', 'dtos', 'services', 'repositories', 'entities']
        for section in sections:
            section_data = java_lld.get(section, [])
            for item in section_data:
                package = item.get('package')
                class_name = item.get('name')
                if package and class_name:
                    file_locations.append(construct_file_path(package, class_name))

        return file_locations
