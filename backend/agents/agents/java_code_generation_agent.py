from typing import List
import json
import os
from concurrent.futures import ThreadPoolExecutor, as_completed

from agents.types import LLMResponse
from orchestrator.models.models import ChatMessage
from .java_file_code_generation_agent import JavaFileCodeGenerationAgent
from .agent_interface import AgentInterface


class JavaCodeGenerationAgent(AgentInterface):
    """
    An agent responsible for generating java code based on the system design document.
    Takes the complete design document as input and generates actual java code files.
    """

    def __init__(self) -> None:
        self.folder_path = os.path.join(
            os.path.dirname(__file__), "../../../../generated_code"
        )
        self.max_threads = 5  # Set the maximum number of threads

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
        # file_locations = file_locations[:3]

        # Generate code for each file in parallel
        generated_files = []
        communications = []

        def generate_code(file_location):
            # Create a new instance of JavaFileCodeGenerationAgent for each thread
            file_generator = JavaFileCodeGenerationAgent()

            # Prepare message for file generator with file location and LLD
            message = {"document": latest_document_elements, "file name": file_location}

            # Generate code for this file
            response = file_generator.process(json.dumps(message))

            # Collect results
            result = {
                "path": file_location,
                "content": response["updated_doc_element"],
                "response_message": (
                    f"For {file_location}: {response['response_message']}"
                    if response["response_message"]
                    else ""
                ),
            }

            return result

        with ThreadPoolExecutor(max_workers=self.max_threads) as executor:
            futures = {
                executor.submit(generate_code, file_location): file_location
                for file_location in file_locations
            }
            for future in as_completed(futures):
                result = future.result()
                generated_files.append(
                    {"path": result["path"], "content": result["content"]}
                )
                if result["response_message"]:
                    communications.append(result["response_message"])

        # Return combined results
        resp = LLMResponse()
        resp["raw_response"] = ""
        resp["updated_doc_element"] = generated_files
        resp["response_message"] = "\n".join(communications)
        self.generate_code_base(generated_files)
        return resp

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
        sections = ["controllers", "dtos", "services", "repositories", "entities"]
        for section in sections:
            section_data = java_lld.get(section, [])
            for item in section_data:
                package = item.get("package")
                class_name = item.get("name")
                if package and class_name:
                    file_locations.append(construct_file_path(package, class_name))

        return file_locations

    def generate_code_base(self, generated_files):
        """
        Creates a folder (and any necessary parent folders) at `folder_path` if it doesn't exist,
        then creates each file specified in generated_files (a list of dictionaries with 'path' and 'content').

        :param folder_path: Path to the top-level folder to create if it doesn't exist.
        :param generated_files:  List of dicts, each of which must contain:
                            {
                                "path": "relative/path/to/file.txt",
                                "content": "File content..."
                            }
        """
        # Ensure the base folder exists
        os.makedirs(self.folder_path, exist_ok=True)

        # Create each file inside the folder
        for file_info in generated_files:
            # Join the base folder path with the relative path for the current file
            file_path = os.path.join(self.folder_path, file_info["path"])

            # Make sure the sub-directories for this file exist
            os.makedirs(os.path.dirname(file_path), exist_ok=True)

            # Write the specified content to the file
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(file_info["content"])
