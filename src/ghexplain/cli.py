import argparse
import sys
from .core import issue
from .exceptions import GHExplainError

def main():
	parser = argparse.ArgumentParser(description="Generate AI-powered summaries of GitHub issues")
	parser.add_argument("url", help="GitHub issue URL")
	parser.add_argument("-l", "--language", default="english",
					  help="Language for the summary (default: english)")
	
	args = parser.parse_args()
	
	try:
		summary = issue(args.url, language=args.language)
		print(summary)
		return 0
	except GHExplainError as e:
		print(f"Error: {e}", file=sys.stderr)
		return 1

if __name__ == "__main__":
	sys.exit(main())