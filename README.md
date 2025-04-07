
<p align="center"><h1 align="center">LANGGRAPH-MCP-AGENTS</h1></p>
<p align="center">
	<em>From Protocol to Intelligence: Powering Agents with MCP.</em>
</p>
<p align="center">
	<img src="https://img.shields.io/github/license/serkanyasr/langgraph-mcp-agents?style=default&logo=opensourceinitiative&logoColor=white&color=0080ff" alt="license">
	<img src="https://img.shields.io/github/last-commit/serkanyasr/langgraph-mcp-agents?style=default&logo=git&logoColor=white&color=0080ff" alt="last-commit">
	<img src="https://img.shields.io/github/languages/top/serkanyasr/langgraph-mcp-agents?style=default&color=0080ff" alt="repo-top-language">
	<img src="https://img.shields.io/github/languages/count/serkanyasr/langgraph-mcp-agents?style=default&color=0080ff" alt="repo-language-count">
</p>
<p align="center"><!-- default option, no dependency badges. -->
</p>
<p align="center">
	<!-- default option, no dependency badges. -->
</p>
<br>



## 📍 Overview

**LangGraph MCP Agents** is an experimental project that aims to transform tools defined under MCP (Modular Communication Protocol) into autonomous **agents** using the [LangGraph](https://github.com/langchain-ai/langgraph) framework.

The aim of this project is to transform tools designed in accordance with the MCP protocol (e.g. tools with tasks such as planning, coding, execution, etc.) into agents running on the LangGraph infrastructure and to provide effective task sharing and collaboration between these agents.

---


## 📁 Project Structure

```sh
└── langgraph-mcp-agents/
    ├── LICENCE
    ├── README.md
    ├── app_cli.py
    ├── mcp_client.py
    ├── mcp_config.json
    └── requirements.txt
```


### 📂 Project Index
<details open>
	<summary><b><code>LANGGRAPH-MCP-AGENTS/</code></b></summary>
	<details> <!-- __root__ Submodule -->
		<summary><b>__root__</b></summary>
		<blockquote>
			<table>
			<tr>
				<td><b><a href='https://github.com/serkanyasr/langgraph-mcp-agents/blob/master/mcp_client.py'>mcp_client.py</a></b></td>
				<td>- MCPClient and MCPServer are the main classes in mcp_client.py<br>- MCPClient manages connections to multiple MCP servers, loads server configurations, starts servers, initializes tools, and handles resource cleanup<br>- MCPServer represents an individual server connection, manages tool execution, and handles cleanup operations<br>- The file is crucial for server communication and tool management in the project.</td>
			</tr>
			<tr>
				<td><b><a href='https://github.com/serkanyasr/langgraph-mcp-agents/blob/master/app_cli.py'>app_cli.py</a></b></td>
				<td>- App_cli.py is a command-line interface for a chatbot application that leverages the OpenAI language model<br>- It initializes the AI agent, accepts user input, and generates AI responses in real-time<br>- The script also handles server configurations, manages conversation history, and provides error handling and debugging support.</td>
			</tr>
			<tr>
				<td><b><a href='https://github.com/serkanyasr/langgraph-mcp-agents/blob/master/requirements.txt'>requirements.txt</a></b></td>
				<td>- Requirements.txt manages the necessary dependencies for the project<br>- It ensures the correct versions of libraries such as mcp, langgraph, langchain, python-dotenv, langchain-mcp-adapters, and rich are installed<br>- This contributes to the stability and reproducibility of the codebase across different environments.</td>
			</tr>
			<tr>
				<td><b><a href='https://github.com/serkanyasr/langgraph-mcp-agents/blob/master/mcp_config.json'>mcp_config.json</a></b></td>
				<td>- Mcp_config.json configures the Model Context Protocol servers, specifying the commands and arguments for different server types: filesystem, SQLite, and memory<br>- It enables the project to interact with various data storage systems, enhancing its flexibility and adaptability to diverse environments.</td>
			</tr>
			<tr>
				<td><b><a href='https://github.com/serkanyasr/langgraph-mcp-agents/blob/master/LICENCE'>LICENCE</a></b></td>
				<td>- The LICENCE file establishes the legal framework for the project, granting users the right to freely use, modify, and distribute the software under the MIT License<br>- It also disclaims warranties and limits liability, ensuring the software is provided "as is"<br>- This file is crucial for defining the terms of use and distribution of the software.</td>
			</tr>
			</table>
		</blockquote>
	</details>
</details>

---
## 🚀 Getting Started

### ☑️ Prerequisites

Before getting started with langgraph-mcp-agents, ensure your runtime environment meets the following requirements:

- **Programming Language:** Python
- **Package Manager:** Pip


### ⚙️ Installation

Install langgraph-mcp-agents using one of the following methods:

**Build from source:**

1. Clone the langgraph-mcp-agents repository:
```sh
❯ git clone https://github.com/serkanyasr/langgraph-mcp-agents
```

2. Navigate to the project directory:
```sh
❯ cd langgraph-mcp-agents
```

3. Install the project dependencies:


**Using `pip`** &nbsp; [<img align="center" src="https://img.shields.io/badge/Pip-3776AB.svg?style={badge_style}&logo=pypi&logoColor=white" />](https://pypi.org/project/pip/)

```sh
❯ pip install -r requirements.txt
```




### 🤖 Usage
Run langgraph-mcp-agents using the following command:
**Using `pip`** &nbsp; [<img align="center" src="https://img.shields.io/badge/Pip-3776AB.svg?style={badge_style}&logo=pypi&logoColor=white" />](https://pypi.org/project/pip/)

```sh
❯ python {entrypoint}
```

## 🔰 Contributing

- **💬 [Join the Discussions](https://github.com/serkanyasr/langgraph-mcp-agents/discussions)**: Share your insights, provide feedback, or ask questions.
- **🐛 [Report Issues](https://github.com/serkanyasr/langgraph-mcp-agents/issues)**: Submit bugs found or log feature requests for the `langgraph-mcp-agents` project.
- **💡 [Submit Pull Requests](https://github.com/serkanyasr/langgraph-mcp-agents/blob/main/CONTRIBUTING.md)**: Review open PRs, and submit your own PRs.

<details closed>
<summary>Contributing Guidelines</summary>

1. **Fork the Repository**: Start by forking the project repository to your github account.
2. **Clone Locally**: Clone the forked repository to your local machine using a git client.
   ```sh
   git clone https://github.com/serkanyasr/langgraph-mcp-agents
   ```
3. **Create a New Branch**: Always work on a new branch, giving it a descriptive name.
   ```sh
   git checkout -b new-feature-x
   ```
4. **Make Your Changes**: Develop and test your changes locally.
5. **Commit Your Changes**: Commit with a clear message describing your updates.
   ```sh
   git commit -m 'Implemented new feature x.'
   ```
6. **Push to github**: Push the changes to your forked repository.
   ```sh
   git push origin new-feature-x
   ```
7. **Submit a Pull Request**: Create a PR against the original project repository. Clearly describe the changes and their motivations.
8. **Review**: Once your PR is reviewed and approved, it will be merged into the main branch. Congratulations on your contribution!
</details>

<details closed>
<summary>Contributor Graph</summary>
<br>
<p align="left">
   <a href="https://github.com{/serkanyasr/langgraph-mcp-agents/}graphs/contributors">
      <img src="https://contrib.rocks/image?repo=serkanyasr/langgraph-mcp-agents">
   </a>
</p>
</details>

---

## 🎗 License

This project is licensed under the MIT License.For more details, refer to the [LICENSE](https://github.com/serkanyasr/langgraph-mcp-agents/blob/main/LICENCE) file.

---