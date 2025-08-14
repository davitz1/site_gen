import unittest


from htmlnode import HTMLNode, LeafNode, ParentNode

class TestHTMLNode(unittest.TestCase):

    #TESTING HTML NODE
    def test_to_html_props(self):
        node = HTMLNode(
            'a',
            'link',
            None,
            {"type": "link", "href": "https://www.google.com"}
        )
        self.assertEqual(
            ' type="link" href="https://www.google.com"',
            node.props_to_html()
        )

    def test_values(self):
        node = HTMLNode(
            "div",
            "Its not a fashion statement",
        )
        self.assertEqual(
            node.tag,
            "div",
        )
        self.assertEqual(
            node.value,
            "Its not a fashion statement",
        )
        self.assertEqual(
            node.children,
            None,
        )
        self.assertEqual(
            node.props,
            None,
        )

    def test_repr(self):
        node = HTMLNode(
            "p",
            "its a deathwish",
            None,
            {'class': 'primary'}
        )
        self.assertEqual(
            repr(node),
            "HTMLNode(p, its a deathwish, children: None, {'class': 'primary'})"
        )
        

    #TESTING LEAF NODE
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "and when we go dont blame us")
        self.assertEqual(node.to_html(), "<p>and when we go dont blame us</p>")

    def test_leaf_to_html_a(self):
        node = LeafNode("a", "Click here", {"href":"https://www.google.com"})
        self.assertEqual(node.to_html(), '<a href="https://www.google.com">Click here</a>')

    def test_repr_leaf(self):
        node = LeafNode(
            "p",
            "a place for you and just your mind",
            {'class': 'primary'}
        )
        self.assertEqual(
            repr(node),
            "LeafNode(p, a place for you and just your mind, {'class': 'primary'})"
        )

    def test_leaf_to_html_no_tag(self):
        node = LeafNode(None, "Hello, world!")
        self.assertEqual(node.to_html(), "Hello, world!")

    
    #TESTING PARENT NODE   
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")
    
    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )
    
    def test_to_html_many_children(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "normal text"),
            ],
        )
        self.assertEqual(
            node.to_html(),
            "<p><b>Bold text</b>Normal text<i>italic text</i>normal text</p>"
        )
    
       


        

if __name__ == "__main__":
    unittest.main()
