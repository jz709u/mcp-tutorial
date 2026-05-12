from os import name

from pydantic import Field

from mcp.server.fastmcp import FastMCP

mcp = FastMCP("DocumentMCP", log_level="ERROR")


docs = {
    "deposition.md": "This deposition covers the testimony of Angela Smith, P.E.",
    "report.pdf": "The report details the state of a 20m condenser tower.",
    "financials.docx": "These financials outline the project's budget and expenditures.",
    "outlook.pdf": "This document presents the projected future performance of the system.",
    "plan.md": "The plan outlines the steps for the project's implementation.",
    "spec.txt": "These specifications define the technical requirements for the equipment.",
}

@mcp.tool(
  name="read_doc_content",
  description="Reads the contents of a document and return it as a string.",
)
def read_doc_content(doc_id: str = Field(description="ID of the document to read")):
    if doc_id not in docs:
        raise ValueError(f"Document with ID `{doc_id}' not found.")
    return docs[doc_id]

@mcp.tool(
    name="edit_doc_content",
    description="Replaces the `content_to_replace` in the document with `new_content`.  If `Content_to_replace` doesn't exist in the document then it doesn't replace"
)
def edit_doc_content(
    doc_id: str = Field(description="ID of the document to edit"), 
    new_content: str = Field(description="New content for the document"),
    content_to_replace: str = Field(description="Content to replace in the document.")
    ):
    if doc_id not in docs:
        raise ValueError(f"Document with ID `{doc_id}' not found.")
    docs[doc_id] = docs[doc_id].replace(content_to_replace, new_content)
    return f"Document `{docs[doc_id]}` updated successfully."

@mcp.resource(
    "docs://documents",
    mime_type="application/json",
    name="list_doc_ids",
    description="Return a list of all document IDs available in the system."
)
def list_doc_ids() -> list[str]:
    return list(docs.keys())

@mcp.resource(
    "docs://documents/{doc_id}",
    mime_type="text/plain",
    name="get_doc_content",
    description="Return the content of a document given its ID."
)
def get_doc_content(doc_id: str = Field(description="ID of the document to retrieve")) -> str:
    if doc_id not in docs:
        raise ValueError(f"Document with ID `{doc_id}' not found.")
    return docs[doc_id]

# TODO: Write a prompt to rewrite a doc in markdown format
# TODO: Write a prompt to summarize a doc


if __name__ == "__main__":
    mcp.run(transport="stdio")
