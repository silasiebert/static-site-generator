import re


class MarkdownBlock:
    block_type_paragraph = "paragraph"
    block_type_code = "code"
    block_type_heading = "heading"
    block_type_quote = "quote"
    block_type_unordered_list = "unordered list"
    block_type_ordered_list = "ordered list"


def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    clean_blocks = map(lambda string: string.strip(" \n"), blocks)
    non_empty_blocks = filter(lambda block: block != "", clean_blocks)
    block_list = list(non_empty_blocks)
    print(f"Block list: {block_list} is of type: {type(block_list)}")
    return block_list


def block_to_block_type(block):
    if re.match(r"(^```[\S\s]*```$)", block):
        block_type = MarkdownBlock.block_type_code
    elif re.match(r"(^#{1,6} \w+)", block) is not None:
        block_type = MarkdownBlock.block_type_heading
    elif (
        len(list(filter(lambda line: not line.startswith(">"), block.split("\n")))) == 0
    ):
        block_type = MarkdownBlock.block_type_quote
    elif (
        len(
            list(
                filter(
                    lambda line: not line.startswith("- ")
                    and not line.startswith("* "),
                    block.split("\n"),
                )
            )
        )
        == 0
    ):
        block_type = MarkdownBlock.block_type_unordered_list
    elif block.startswith("1. "):
        block_lines = block.split("\n")
        block_type = MarkdownBlock.block_type_ordered_list
        for i in range(0, len(block_lines)):
            print(i)
            if not block_lines[i].startswith(f"{i+1}. "):
                print(block_lines[i])
                block_type = MarkdownBlock.block_type_paragraph
                continue
    else:
        block_type = MarkdownBlock.block_type_paragraph
    return block_type
