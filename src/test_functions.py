from functions import (split_nodes_delimiter, extract_markdown_images, extract_markdown_links, split_nodes_link, split_nodes_image, text_to_textnodes)
import unittest
from textnode import TextNode, TextType

class TestSplitNodesDelimiter(unittest.TestCase):
    
    def test_text_to_textnodes(self):
        node = text_to_textnodes("This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)")
        self.assertEqual([
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev")
        ],
                         node)


    def test_bold(self):
        node = TextNode("This is a **bolded** node", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("This is a ", TextType.TEXT),
                TextNode("bolded", TextType.BOLD),
                TextNode(" node", TextType.TEXT)
            ],
            new_nodes
        )
    
    def test_doubled_bold(self):
        node = TextNode("This is a **bolded** node **twice**", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("This is a ", TextType.TEXT),
                TextNode("bolded", TextType.BOLD),
                TextNode(" node ", TextType.TEXT),
                TextNode("twice", TextType.BOLD)
            ],
            new_nodes
        )

    def test_multiword(self):
        node = TextNode("This is a **multiword bolded** node **twice**", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], '**', TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("This is a ", TextType.TEXT),
                TextNode("multiword bolded", TextType.BOLD),
                TextNode(" node ", TextType.TEXT),
                TextNode("twice", TextType.BOLD)
            ],
            new_nodes
        )
    def test_bold_and_italic(self):
        node = TextNode("**bold** and _italic_", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        new_nodes = split_nodes_delimiter(new_nodes, "_", TextType.ITALIC)
        self.assertListEqual(
            [
                TextNode("bold", TextType.BOLD),
                TextNode(" and ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
            ],
            new_nodes,
        )

    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is a text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")],
                             matches)

    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is a text with a [link](https://google.com) and [another link](https://brave.com)"
        )
        self.assertListEqual([("link", "https://google.com"), ("another link", "https://brave.com")],
                             matches)

    def test_split_image(self):
        node = TextNode(
            "This is a text with an ![image](https://i.imgur.com/zjjcJKZ.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is a text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png")
            ],
            new_nodes
        )
    
    def test_split_image_single(self):
        node = TextNode(
            "![image](https://www.whatever.com/image.png)",
            TextType.TEXT
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("image", TextType.IMAGE, "https://www.whatever.com/image.png")
            ],
            new_nodes
        )

    def test_split_link(self):
        node = TextNode(
            "This is a text with a [link](https://google.com) and [another link](https://boot.dev) plus text",
            TextType.TEXT
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is a text with a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://google.com"),
                TextNode(" and ", TextType.TEXT),
                TextNode("another link", TextType.LINK, "https://boot.dev"),
                TextNode(" plus text", TextType.TEXT)
            ],
            new_nodes

        )


if __name__ == "__main__":
    unittest.main()
