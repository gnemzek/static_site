from textnode import *
from markdown import *
from textnode import TextNode, TextType
from markdown import *

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    # create new list to store result nodes
    result = []

    #loop through each node in the old_nodes list
    for old_node in old_nodes:
        #if the node is not a text type, add it as-is
        if old_node.text_type != TextType.text:
            result.append(old_node)
            continue
        
        text = old_node.text

        pieces = []

        if text.count(delimiter) < 2:
            #no matching pairs, keep node as is
            result.append(old_node)
            continue

        # start checking for delimiter pairs
        while delimiter in text:
            # find first delimiter
            start_index = text.find(delimiter)

            #add text before delimiter to pieces list 
            if start_index > 0:
                pieces.append((text[:start_index], TextType.text))

            #find closing delimiter 
            end_index = text.find(delimiter, start_index + len(delimiter))

            #if no closing delimiter found, that is an error
            if end_index == -1:
                raise Exception(f"No closing delimiter found for {delimiter}")
            
            #extract the text between delimiters, without the delimiters themselves
            between_text = text[start_index + len(delimiter):end_index]
            pieces.append((between_text, text_type))

            #continue with text after closing delimiter

            text = text[end_index + len(delimiter):]

        if text:
            pieces.append((text, TextType.text))

        #create TextNodes from the pieces and add to result list 
        for text_piece, node_type in pieces:
            result.append(TextNode(text_piece, node_type))

    return result

def split_nodes_image(old_nodes):
    # create new list to store result nodes
    result = []

    for old_node in old_nodes:
        # Skip non-text nodes - they can't contain images to extract
        if old_node.text_type != TextType.text:
            result.append(old_node)
            continue
        
        # Check if there are images to extract
        images = extract_markdown_images(old_node.text)
    
        # If no images, keep the node as is
        if not images:
            result.append(old_node)
            continue
         
         # Start with the current text
        remaining_text = old_node.text

        # process each image found
        for image_alt, image_url in images:
            # Split at the image markdown
            image_markdown = f"![{image_alt}]({image_url})"
            sections = remaining_text.split(image_markdown, 1)
        
            # Add text before the image (if it exists)
            if sections[0]:
                result.append(TextNode(sections[0], TextType.text))

            # Add the image node
            result.append(TextNode(image_alt, TextType.image, image_url))
            
            # Update remaining text for next iteration
            if len(sections) > 1:
                remaining_text = sections[1]
            else:
                remaining_text = ""
        
        # Add any remaining text after the last image
        if remaining_text:
            result.append(TextNode(remaining_text, TextType.text))
    
    return result


def split_nodes_link(old_nodes):
    # create new list to store result nodes
    result = []

    for old_node in old_nodes:
        # Skip non-text nodes - they can't contain links to extract
        if old_node.text_type != TextType.text:
            result.append(old_node)
            continue
        
        # Check if there are links to extract
        links = extract_markdown_links(old_node.text)
    
        # If no links, keep the node as is
        if not links:
            result.append(old_node)
            continue
         
         # Start with the current text
        remaining_text = old_node.text

        # process each link found
        for link_alt, link_url in links:
            # Split at the link markdown
            link_markdown = f"[{link_alt}]({link_url})"
            sections = remaining_text.split(link_markdown, 1)
        
            # Add text before the image (if it exists)
            if sections[0]:
                result.append(TextNode(sections[0], TextType.text))

            # Add the image node
            result.append(TextNode(link_alt, TextType.link, link_url))
            
            # Update remaining text for next iteration
            if len(sections) > 1:
                remaining_text = sections[1]
            else:
                remaining_text = ""
        
        # Add any remaining text after the last image
        if remaining_text:
            result.append(TextNode(remaining_text, TextType.text))
    
    return result


def text_to_textnodes(text):
    # start with single text node that contains all the text
    nodes = [TextNode(text, TextType.text)]

    # apply the splitting functions in sequence

    nodes = split_nodes_delimiter(nodes, "**", TextType.bold)
    nodes = split_nodes_delimiter(nodes, "_", TextType.italic)
    nodes = split_nodes_delimiter(nodes, "`", TextType.code)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)

    return nodes

def text_to_children(text):
    # Start by creating a TextNode with the raw text
    text_node = TextNode(text, TextType.text)
    
    # Split the TextNode based on delimiters for bold, italic, code
    text_nodes = split_nodes_delimiter([text_node], "**", TextType.bold)
    text_nodes = split_nodes_delimiter(text_nodes, "_", TextType.italic)
    text_nodes = split_nodes_delimiter(text_nodes, "`", TextType.code)
    
    # Convert each TextNode to an HTMLNode
    html_nodes = []
    for node in text_nodes:
        html_node = text_node_to_html_node(node)
        html_nodes.append(html_node)
    
    return html_nodes

def create_new_HTML_node(block_type, block):
    if block_type == BlockType.heading:
        # count number of # to see what heading level
        level = 0
        for char in block:
            if char == "#":
                level += 1
            else:
                break
        # extract heading text
        heading_text = block[level:].strip()

        # create HTML node
        heading_node = HTMLNode(f"h{level}", None, text_to_children(heading_text))
        return heading_node

    elif block_type == BlockType.code:
         # Extract the code content (remove the ``` at the beginning and end)
        lines = block.strip().split("\n")[1:-1]  # Skip the first and last lines which contain ```
        # Skip the first and last lines which contain the ```
        if len(lines) >= 2:
            code_content = "\n".join(lines[1:-1])
            # Create a text node (without parsing inline markdown)
            text_node = TextNode(code_content, TextType.text)
            code_node = text_node_to_html_node(text_node)
            # Wrap in pre tag
            return HTMLNode("pre", None, [HTMLNode("code", None, [code_node])])
        else:
            # Handle empty code blocks
            return
    
    elif block_type == BlockType.quote:
         # Remove the '>' prefix from each line and join them with spaces
        text = block.strip()
        text = text.replace("\n> ", " ").replace("> ", "")
        return HTMLNode("blockquote", None, text_to_children(text))
    
    elif block_type == BlockType.unordered_list:
        # Split the block into lines
        items = []
        for line in block.strip().split("\n"):
            if line.startswith("* "):
                item_text = line[2:]  # Remove the "* " prefix
                items.append(HTMLNode("li", None, text_to_children(item_text)))
        return HTMLNode("ul", None, items)
    
    elif block_type == BlockType.ordered_list:
        # Split the block into lines
        lines = block.split("\n")
        list_items = []
        
        for line in lines:
            # Check if line starts with a number followed by a period
            line = line.strip()
            # Use regex or simple parsing to check for "number." pattern
            if line and line[0].isdigit() and "." in line:
                # Find position after the first period
                pos = line.find(".") + 1
                # Extract content after "number."
                item_content = line[pos:].strip()
                # Create li node with inline markdown parsed
                li_node = HTMLNode("li", None, text_to_children(item_content))
                list_items.append(li_node)
        
        # Create ol node with all list items as children
        ol_node = HTMLNode("ol", None, list_items)
        return ol_node
    
    elif block_type == BlockType.paragraph:
        para_content = block.replace("\n", " ")
        para_node = HTMLNode("p", None, text_to_children(para_content))
        return para_node


def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    children = []
    for block in blocks:
        html_node = block_to_html_node(block)
        children.append(html_node)
    return ParentNode("div", children, None)


def block_to_html_node(block):
    block_type = block_to_block_type(block)
    if block_type == BlockType.paragraph:
        return paragraph_to_html_node(block)
    if block_type == BlockType.heading:
        return heading_to_html_node(block)
    if block_type == BlockType.code:
        return code_to_html_node(block)
    if block_type == BlockType.ordered_list:
        return olist_to_html_node(block)
    if block_type == BlockType.unordered_list:
        return ulist_to_html_node(block)
    if block_type == BlockType.quote:
        return quote_to_html_node(block)
    raise ValueError("invalid block type")

def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    children = []
    for text_node in text_nodes:
        html_node = text_node_to_html_node(text_node)
        children.append(html_node)
    return children


def paragraph_to_html_node(block):
    lines = block.split("\n")
    paragraph = " ".join(lines)
    children = text_to_children(paragraph)
    return ParentNode("p", children)


def heading_to_html_node(block):
    level = 0
    for char in block:
        if char == "#":
            level += 1
        else:
            break
    if level + 1 >= len(block):
        raise ValueError(f"invalid heading level: {level}")
    text = block[level + 1 :]
    children = text_to_children(text)
    return ParentNode(f"h{level}", children)


def code_to_html_node(block):
    if not block.startswith("```") or not block.endswith("```"):
        raise ValueError("invalid code block")
    text = block[4:-3]
    raw_text_node = TextNode(text, TextType.text)
    child = text_node_to_html_node(raw_text_node)
    code = ParentNode("code", [child])
    return ParentNode("pre", [code])


def olist_to_html_node(block):
    items = block.split("\n")
    html_items = []
    for item in items:
        text = item[3:]
        children = text_to_children(text)
        html_items.append(ParentNode("li", children))
    return ParentNode("ol", html_items)


def ulist_to_html_node(block):
    items = block.split("\n")
    html_items = []
    for item in items:
        text = item[2:]
        children = text_to_children(text)
        html_items.append(ParentNode("li", children))
    return ParentNode("ul", html_items)


def quote_to_html_node(block):
    lines = block.split("\n")
    new_lines = []
    for line in lines:
        if not line.startswith(">"):
            raise ValueError("invalid quote block")
        new_lines.append(line.lstrip(">").strip())
    content = " ".join(new_lines)
    children = text_to_children(content)
    return ParentNode("blockquote", children)

