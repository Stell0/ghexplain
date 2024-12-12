class GHExplainError(Exception):
	"""Base exception for ghexplain."""
	pass

class InvalidURLError(GHExplainError):
	"""Raised when the provided GitHub URL is invalid."""
	pass

class APIError(GHExplainError):
	"""Raised when there's an error with the GitHub API."""
	pass

class AuthenticationError(GHExplainError):
	"""Raised when authentication fails."""
	pass