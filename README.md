# Multi-Agent Research Assistant

An open-source research assistant that combines web search, web-page extraction,
LLM-based report writing, and automated critique into one LangChain workflow.
Enter a topic in the Streamlit app and the system gathers current sources,
extracts supporting content, produces a structured report, and evaluates the
result.

## Features

- Search the web for recent and relevant information with Tavily.
- Scrape and extract readable content from selected URLs.
- Generate concise research reports with a Groq-hosted language model.
- Review reports with a dedicated critic chain that returns a score,
	strengths, and areas for improvement.
- View each pipeline stage in the Streamlit interface and download the report
	as Markdown.

## Architecture

The project uses a sequential pipeline with two tool-using agents followed by
two LangChain chains:

```text
Research topic
		 |
		 v
Search Agent -- Tavily web search --> Search results
		 |
		 v
Reader Agent -- requests + extraction libraries --> Scraped content
		 |
		 v
Writer Chain -- Groq LLM --> Research report
		 |
		 v
Critic Chain -- Groq LLM --> Score and feedback
```

The Streamlit UI in `app.py` runs the same stages interactively and stores the
intermediate outputs in Streamlit session state. The reusable pipeline in
`src/pipelines/pipeline.py` returns all outputs as a dictionary for programmatic
use.

## Technologies

- Python 3.13
- Streamlit for the web interface
- LangChain and LangChain Core for agents, prompts, tools, and chains
- Groq via `langchain-groq` for language-model inference
- Tavily for web search
- Requests, Trafilatura, Readability, BeautifulSoup, and lxml for web content
	retrieval and extraction
- `python-dotenv` for environment configuration
- Rich for terminal output

## Installation

### 1. Clone the repository

```bash
git clone <repository-url>
cd Langchain_Multiagent_Asst
```

### 2. Create and activate an environment

Using Conda:

```bash
conda create -n langagent python=3.13 -y
conda activate langagent
```

Or using a standard Python virtual environment:

```bash
python -m venv .venv
```

Activate it on Windows:

```powershell
.venv\Scripts\Activate.ps1
```

Activate it on macOS or Linux:

```bash
source .venv/bin/activate
```

### 3. Install dependencies

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

## Configuration

Create a `.env` file in the project root:

```env
GROQ_API_KEY=your_groq_api_key
TAVILY_API_KEY=your_tavily_api_key
```

Get credentials from [Groq](https://console.groq.com/keys) and
[Tavily](https://app.tavily.com/). Never commit `.env` or publish API keys.

## Usage

### Streamlit application

```bash
streamlit run app.py
```

Open the local URL printed by Streamlit, enter a research topic, and select
**Run Research Pipeline**.

### Programmatic pipeline

Edit the topic in `main.py`, then run:

```bash
python main.py
```

The pipeline prints the search results, extracted content, generated report,
and critic feedback to the terminal.

## Project Structure

```text
Langchain_Multiagent_Asst/
├── app.py                      # Streamlit user interface
├── main.py                     # Programmatic example entry point
├── requirements.txt            # Python dependencies
└── src/
		├── agents/agents.py        # LLM setup, agents, writer, and critic chains
		├── pipelines/pipeline.py   # Sequential research workflow
		└── tools/tools.py          # Tavily search and URL extraction tools
```

## Notes

- Search and scraping depend on external services and network access.
- The writer truncates oversized inputs and is configured to produce reports
	under 500 tokens.
- Model availability, rate limits, and provider pricing are controlled by
	Groq and Tavily.

## License

See [LICENSE](LICENSE) for license information.