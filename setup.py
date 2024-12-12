from setuptools import setup, find_packages

setup(
	name="ghexplain",
	packages=find_packages(),
	install_requires=[
		"langchain>=0.3.0",
		"langchain-openai>=0.2.0",
		"requests>=2.32.3",
		"python-dotenv>=1.0.0",
	],
	python_requires=">=3.8",
)
