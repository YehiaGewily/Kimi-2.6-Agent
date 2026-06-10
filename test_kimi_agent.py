import unittest
from unittest.mock import patch

from kimi_agent import KimiAgent, parse_args


class KimiAgentTests(unittest.TestCase):
    def test_parse_args_supports_required_mode_and_prompt(self):
        args = parse_args(["--mode", "coding", "--prompt", "hello"])
        self.assertEqual(args.mode, "coding")
        self.assertEqual(args.prompt, "hello")

    def test_rejects_unsupported_mode(self):
        agent = KimiAgent(api_key="dummy-key")
        with self.assertRaises(ValueError):
            agent.ask(mode="unknown", prompt="x")

    def test_rejects_empty_prompt(self):
        agent = KimiAgent(api_key="dummy-key")
        with self.assertRaises(ValueError):
            agent.ask(mode="coding", prompt="   ")

    @patch("urllib.request.urlopen")
    def test_builds_request_and_returns_content(self, mock_urlopen):
        mock_response = mock_urlopen.return_value.__enter__.return_value
        mock_response.read.return_value = (
            b'{"choices":[{"message":{"content":"Result text"}}]}'
        )

        agent = KimiAgent(api_key="dummy-key")
        result = agent.ask(mode="summarising", prompt="summarise this")
        self.assertEqual(result, "Result text")


if __name__ == "__main__":
    unittest.main()
