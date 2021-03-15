import unittest
import label_studio_converter.utils as utils


class TestUtils(unittest.TestCase):
    def test_create_tokens_and_tags_with_eol_tag(self):

        s = 'I need a break\nplease'
        spans = [{'end': 14,
                  'labels': ['Person'],
                  'start': 9,
                  'text': 'break',
                  'type': 'Labels'}]
        tokens, tags = utils.create_tokens_and_tags(s, spans)
        self.assertEqual(tokens[0], "I")
        self.assertEqual(tags[0], "O")
        self.assertEqual(tokens[1], "need")
        self.assertEqual(tags[1], "O")
        self.assertEqual(tokens[2], "a")
        self.assertEqual(tags[2], "O")
        self.assertEqual(tokens[3], "break")
        self.assertEqual(tags[3], "B-Person")
        self.assertEqual(tokens[4], "please")
        self.assertEqual(tags[4], "O")

    def test_create_tokens_and_tags_with_tab_tag(self):

        s = 'I need a tab\tplease'
        spans = [{'end': 12,
                  'labels': ['Person'],
                  'start': 9,
                  'text': 'tab',
                  'type': 'Labels'}]
        tokens, tags = utils.create_tokens_and_tags(s, spans)
        self.assertEqual(tokens[0], "I")
        self.assertEqual(tags[0], "O")
        self.assertEqual(tokens[1], "need")
        self.assertEqual(tags[1], "O")
        self.assertEqual(tokens[2], "a")
        self.assertEqual(tags[2], "O")
        self.assertEqual(tokens[3], "tab")
        self.assertEqual(tags[3], "B-Person")
        self.assertEqual(tokens[4], "please")
        self.assertEqual(tags[4], "O")

    def test_handles_multiple_spaces(self):
        text = 'Centerville is a  town in   Center   Township,     Wayne   County, in the U.S.   state of Indiana'
        spans = [{'end': 11, 'labels': ['Location'], 'start': 0, 'text': 'Centerville', 'type': 'Labels'},
                 {'end': 45, 'labels': ['Location'], 'start': 28, 'text': 'Center   Township', 'type': 'Labels'},
                 {'end': 65, 'labels': ['Location'], 'start': 51, 'text': 'Wayne   County', 'type': 'Labels'},
                 {'end': 81, 'labels': ['Location'], 'start': 74, 'text': 'U.S.   ', 'type': 'Labels'},
                 {'end': 97, 'labels': ['Location'], 'start': 90, 'text': 'Indiana', 'type': 'Labels'}]
        tokens,tags = utils.create_tokens_and_tags(text,spans)
        self.assertEqual(tokens, ['Centerville', 'is', 'a', 'town', 'in', 'Center', 'Township', ',', 'Wayne',
                                  'County', ',', 'in', 'the', 'U.S.', 'state', 'of', 'Indiana'])
        self.assertEqual(tags, ['B-Location', 'O', 'O', 'O', 'O', 'B-Location', 'I-Location', 'O',
                                'B-Location', 'I-Location', 'O', 'O', 'O', 'B-Location', 'O', 'O', 'B-Location'])

    def test_handles_entities_within_tokens(self):
        text = 'Roman Karl Scholz (16 January 1912 – 10 May 1944) was an Austrian author and Augustinian canon regular at Klosterneuburg.'
        spans = [{'end': 18, 'labels': ['Person'], 'start': 0, 'text': 'Roman Karl Scholz ', 'type': 'Labels'},
                 {'end': 35, 'labels': ['Date'], 'start': 19, 'text': '16 January 1912 ', 'type': 'Labels'},
                 {'end': 48, 'labels': ['Date'], 'start': 36, 'text': ' 10 May 1944', 'type': 'Labels'},
                 {'end': 66, 'labels': ['Location'], 'start': 56, 'text': ' Austrian ', 'type': 'Labels'},
                 {'end': 89, 'labels': ['Organization'], 'start': 76, 'text': ' Augustinian ', 'type': 'Labels'},
                 {'end': 120, 'labels': ['Location'], 'start': 106, 'text': 'Klosterneuburg', 'type': 'Labels'}]
        tokens,tags = utils.create_tokens_and_tags(text,spans)
        self.assertEqual(tokens, ['Roman', 'Karl', 'Scholz', '(', '16', 'January', '1912', '–',
                                  '10', 'May', '1944', ')', 'was', 'an', 'Austrian', 'author', 'and',
                                  'Augustinian', 'canon', 'regular', 'at', 'Klosterneuburg','.'])
        self.assertEqual(tags, ['B-Person', 'I-Person', 'I-Person', 'O', 'B-Date', 'I-Date', 'I-Date',
                                'O', 'B-Date', 'I-Date', 'I-Date', 'O', 'O', 'O', 'B-Location', 'O', 'O',
                                'B-Organization', 'O', 'O', 'O', 'B-Location','O'])

    def test_handles_single_entity_within_token(self):
        text = 'Clément Lépidis (1920–1997) was a French novelist of Greek descent.'
        spans = [{'end': 15, 'labels': ['Person'], 'start': 0, 'text': 'Clément Lépidis', 'type': 'Labels'},
                 {'end': 26, 'labels': ['Date'], 'start': 17, 'text': '1920–1997', 'type': 'Labels'}]
        tokens,tags = utils.create_tokens_and_tags(text,spans)
        self.assertEqual(tokens, ['Clément', 'Lépidis', '(', '1920–1997', ')', 'was', 'a', 'French', 'novelist',
                                  'of', 'Greek', 'descent.'] )
        self.assertEqual(tags, ['B-Person', 'I-Person', 'O', 'B-Date', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O'])

    def test_handles_multi_token_entity_with_leading_space(self):
        text = 'We gave Jane Smith the ball.'
        spans = [{'end': 18, 'labels': ['Person'], 'start': 7, 'text': ' Jane Smith'}]
        tokens,tags = utils.create_tokens_and_tags(text,spans)
        self.assertEqual(tokens, ['We','gave','Jane','Smith','the','ball.'])
        self.assertEqual(tags, ['O','O','B-Person','I-Person','O','O'])
