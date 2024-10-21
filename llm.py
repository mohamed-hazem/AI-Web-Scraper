# Modules
from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
from langchain_text_splitters import RecursiveCharacterTextSplitter
from typing import Generator, Iterator
# ===================================================================== #

class LLM:
    model_name = "llama3.2"
    model = OllamaLLM(model="llama3.2")
    
    template = (
        "You are tasked with extracting specific information from the following text content: {content}. "
        "Please follow these instructions carefully: \n\n"
        "1. **Extract Information:** Only extract the information that directly matches the provided description: {description}. "
        "2. **No Extra Content:** Do not include any additional text, comments, or explanations in your response. "
        "3. **Empty Response:** If no information matches the description, return an empty string ('')."
        "4. **Direct Data Only:** Your output should contain only the data that is explicitly requested, with no other text."
    )

    splitter = RecursiveCharacterTextSplitter(
        separators=["\n"],
        chunk_size=6144,
        chunk_overlap=0,
        length_function=len,
    )

    def __init__(self, content: str, description: str):
        self.chunks = self.splitter.split_text(content)
        self.description = description
    # ---------------------------------------------- #

    def generate_response(self) -> Generator[Iterator[str], None, None]:
        prompt = ChatPromptTemplate.from_template(self.template)
        chain = prompt | self.model

        for chunk in self.chunks:
            inputs = {"content": chunk, "description": self.description}
            yield chain.stream(inputs)
# --------------------------------------------------------------------- #