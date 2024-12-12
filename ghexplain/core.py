import os
import re
from typing import Optional
import requests
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from .exceptions import InvalidURLError, APIError, AuthenticationError

load_dotenv()

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
GITHUB_API_BASE = "https://api.github.com"
ISSUE_URL_PATTERN = r"https://github\.com/([^/]+)/([^/]+)/issues/(\d+)"

def _parse_issue_url(url: str) -> tuple[str, str, int]:
	"""Parse a GitHub issue URL into owner, repo, and issue number."""
	match = re.match(ISSUE_URL_PATTERN, url)
	if not match:
		raise InvalidURLError("Invalid GitHub issue URL format")
	return match.groups()

def _fetch_issue_data(owner: str, repo: str, issue_number: int) -> dict:
	"""Fetch issue data from GitHub API."""
	if not GITHUB_TOKEN:
		raise AuthenticationError("GitHub token not found in environment variables")

	headers = {
		"Authorization": f"token {GITHUB_TOKEN}",
		"Accept": "application/vnd.github.v3+json"
	}
	
	url = f"{GITHUB_API_BASE}/repos/{owner}/{repo}/issues/{issue_number}"
	response = requests.get(url, headers=headers)
	
	if response.status_code == 404:
		raise APIError("Issue not found")
	elif response.status_code != 200:
		raise APIError(f"GitHub API error: {response.status_code}")

	return response.json()

def _fetch_issue_comments(owner: str, repo: str, issue_number: int) -> list:
	"""Fetch comments for a GitHub issue from the GitHub API."""
	if not GITHUB_TOKEN:
		raise AuthenticationError("GitHub token not found in environment variables")

	headers = {
		"Authorization": f"token {GITHUB_TOKEN}",
		"Accept": "application/vnd.github.v3+json"
	}
	
	url = f"{GITHUB_API_BASE}/repos/{owner}/{repo}/issues/{issue_number}/comments"
	response = requests.get(url, headers=headers)
	
	if response.status_code == 404:
		raise APIError("Comments not found")
	elif response.status_code != 200:
		raise APIError(f"GitHub API error: {response.status_code}")
	
	return response.json()

def _create_summary_prompt(issue_data: dict, language: str) -> str:
	"""Create a prompt for the LLM to summarize the issue."""
	return ChatPromptTemplate.from_messages([
		("system", f"""You are an expert at explaining technical GitHub issues in simple terms. Your goal is to make complex 
		technical issues understandable to developers who might not be familiar with the project internals. Write in {language}.
		Keep explanations concise but ensure they include enough context to understand the issue's significance."""),
		("user", """Explain this GitHub issue in a way that's clear to any technical person, even if they don't know the codebase. 
		Focus on:
		- What problem needs to be solved (in plain terms)
		- Why it matters to users or developers
		- Current state of the issue

		Here's the issue:
		Title: {title}
		Body: {body}
		Status: {state}
		Comments Count: {comments}
		""")
	])

def issue(url: str, language: str = "english") -> str:
	"""
	Generate an AI-powered summary of a GitHub issue.
	
	Args:
		url (str): The GitHub issue URL
		language (str, optional): The language for the summary. Defaults to "english".
	
	Returns:
		str: A summary of the issue in the specified language
	
	Raises:
		InvalidURLError: If the URL format is invalid
		APIError: If there's an error accessing the GitHub API
		AuthenticationError: If GitHub token is missing or invalid
	"""

	# Parse the GitHub issue URL
	owner, repo, issue_number = _parse_issue_url(url)
	
	# Fetch the issue data from GitHub
	issue_data = _fetch_issue_data(owner, repo, int(issue_number))
	issue_comments = _fetch_issue_comments(owner, repo, int(issue_number))
	
	issue = {
		"title": issue_data["title"],
		"body": issue_data["body"],
		"state": issue_data["state"],
		"comments": [comment["body"] for comment in issue_comments]
	}

	# Create the LLM chain
	llm = ChatOpenAI(
		model="gpt-4o",
		api_key=GITHUB_TOKEN,
		base_url="https://models.inference.ai.azure.com"
	)

	prompt = _create_summary_prompt(issue_data, language)
	
	# Generate the summary
	response = llm.invoke(prompt.format(
		title=issue_data["title"],
		body=issue_data["body"],
		state=issue_data["state"],
		comments="\n".join([comment["body"] for comment in issue_comments])
	))
	
	return response.content