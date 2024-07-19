import os
import json
from typing import List, Sequence
from google.cloud import documentai

def layout_to_text(layout: documentai.Document.Page.Layout, text: str) -> str:
    """
    Document AI identifies text in different parts of the document by their
    offsets in the entirety of the document"s text. This function converts
    offsets to a string.
    """
    if not layout.text_anchor.text_segments:
        return ""
    
    return  "".join(
        text[int(segment.start_index) : int(segment.end_index)]
        for segment in layout.text_anchor.text_segments
    )

def extract_lines(lines: Sequence[documentai.Document.Page.Line], text: str) -> List[str]:
    print(f"    {len(lines)} lines detected:")
    extracted_lines = []
    if lines:
        for line in lines:
            line_text = layout_to_text(line.layout, text)
            extracted_lines.append(line_text)
    return extracted_lines

def extract_blocks(blocks: Sequence[documentai.Document.Page.Block], text: str) -> List[str]:
    print(f"    {len(blocks)} blocks detected:")
    extracted_blocks = []
    if blocks:
        for block in blocks:
            block_text = layout_to_text(block.layout, text)
            extracted_blocks.append(block_text)
    return extracted_blocks
      
      
def extract_paragraphs(paragraphs: Sequence[documentai.Document.Page.Paragraph], text: str) -> List[str]:
    print(f"    {len(paragraphs)} paragraphs detected:")
    extracted_paragraphs = []
    if paragraphs:
        for paragraph in paragraphs:
            paragraph_text = layout_to_text(paragraph.layout, text)
            extracted_paragraphs.append(paragraph_text)
    return extracted_paragraphs
  
  
def save_extracted_data(all_blocks, all_lines, all_paragraphs):
  """
    Saves extracted blocks, lines, and paragraphs data to JSON files.

    Args:
        all_blocks (list): List of all extracted blocks.
        all_lines (list): List of all extracted lines.
        all_paragraphs (list): List of all extracted paragraphs.
  """
  with open('extracted_blocks.json', 'w') as f:
    json.dump(all_blocks, f, indent=4)

  with open('extracted_lines.json', 'w') as f:
    json.dump(all_lines, f, indent=4)

  with open('extracted_paragraphs.json', 'w') as f:
    json.dump(all_paragraphs, f, indent=4)