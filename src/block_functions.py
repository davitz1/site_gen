from enum import Enum

from functions import text_to_textnodes
from htmlnode import ParentNode, LeafNode
from textnode import TextNode, TextType, text_node_to_html_node

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    ORDERED_LIST = "ordered_list"
    UNORDERED_LIST = "unordered_list"

def block_to_block_type(block):
    lines = block.split('\n')
    if block.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
        return BlockType.HEADING
    if len(lines) > 1 and lines[0].startswith("```") and lines[-1].startswith("```"):
        return BlockType.CODE
    if block.startswith(">"):
        for line in lines:
            if not line.startswith(">"):
                return BlockType.PARAGRAPH
        return BlockType.QUOTE
    if block.startswith("- "):
        for line in lines:
            if not line.startswith("- "):
                return BlockType.PARAGRAPH
        return BlockType.UNORDERED_LIST
    if block.startswith("1. "):
        i = 1
        for line in lines:
            if not line.startswith(f"{i}. "):
                return BlockType.PARAGRAPH
            i+= 1
        return BlockType.ORDERED_LIST
    return BlockType.PARAGRAPH
    

def markdown_to_blocks(markdown):
    blocks = markdown.split('\n\n')
    filtered_blocks = []
    for block in blocks:
        if block == "":
            continue
        block = block.strip()
        filtered_blocks.append(block)
    return filtered_blocks





def text_to_children(text):
    nodes = text_to_textnodes(text)
    html_nodes = []
    for node in nodes:
        html_nodes.append(text_node_to_html_node(node))
    return html_nodes

def markdown_to_html_node(markdown):
    
    blocks = markdown_to_blocks(markdown)
    block_nodes = []
    for block in blocks:
        block_type = block_to_block_type(block)
        if block_type == BlockType.HEADING:
            tag = ""
            heading_text = block
            if block.startswith("# "):
                tag = "h1"
                heading_text = block[2:]
            elif block.startswith("## "):
                tag = "h2"
                heading_text = block[3:]
            elif block.startswith("### "):
                tag = "h3"
                heading_text = block[4:]
            elif block.startswith("#### "):
                tag = "h4"
                heading_text = block[5:]
            elif block.startswith("##### "):
                tag = "h5"
                heading_text = block[6:]
            elif block.startswith("###### "):
                tag = "h6"
                heading_text = block[7:]
            children = text_to_children(heading_text)
            node = ParentNode(tag, children)
            block_nodes.append(node)
        elif block_type == BlockType.PARAGRAPH:
            lines = block.split('\n')
            block_text = " ".join(lines)
            children = text_to_children(block_text)
            node = ParentNode("p", children)
            block_nodes.append(node)

        elif block_type == BlockType.QUOTE:
            lines = block.split('\n')
            lines = [line[2:] for line in lines]
            quote_text = " ".join(lines)
            children = text_to_children(quote_text)
            node = ParentNode("blockquote", children)
            block_nodes.append(node)

        elif block_type == BlockType.UNORDERED_LIST:
            lines = block.split('\n')
            lines = [line[2:] for line in lines]
            list_items = []
            for line in lines:
                children = text_to_children(line)
                line_node = ParentNode("li", children)
                list_items.append(line_node)
            ul_node = ParentNode("ul", list_items)
            block_nodes.append(ul_node)

        elif block_type == BlockType.ORDERED_LIST:
            lines = block.split('\n')
            list_items = []
            for line in lines:
                text = line[3:]
                children = text_to_children(text)
                line_node = ParentNode("li", children)
                list_items.append(line_node)
            ol_node = ParentNode("ol", list_items)
            block_nodes.append(ol_node)

        elif block_type == BlockType.CODE:
            code_text = block[4:-3]
            text_node = TextNode(code_text, TextType.TEXT)
            text_html_node = text_node_to_html_node(text_node)
            code_node = ParentNode("code", [text_html_node])
            pre_node = ParentNode("pre", [code_node])
            block_nodes.append(pre_node)

        else:
            raise ValueError("Invalid Block Type")
    return ParentNode("div", block_nodes)
