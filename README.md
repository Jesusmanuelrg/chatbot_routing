# Chatbot for Research Questions using Cohere LLM

## Introduction
This project is a chatbot that leverages the Cohere LLM to answer research questions by searching online for answers. It can provide text-based citations and links to sources for verification. The Semantic Router is used to manage responses, ensuring confidentiality and appropriate user behavior.

## Features
- **General Responses:** Answers common questions to reduce costs.
- **Confidentiality:** Does not reply to confidential inquiries.
- **Anti-Discrimination:** Warns users for discriminatory remarks and blocks chat after three warnings.
- **Citation and Sources:** Provides citations and links to sources for answers.

## Installation
1. Clone the repository:
    ```bash
    git clone https://github.com/yourusername/your-repo-name.git
    ```
2. Navigate to the project directory:
    ```bash
    cd your-repo-name
    ```
3. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```
4. Set up environment variables (e.g., API keys for Cohere and other services).
    ```markdown
    Create a `.env` file in the root directory and add the necessary environment variables.
    ```

## Usage
1. Start the chatbot:
    ```bash
    python main.py
    ```
2. Interact with the chatbot via the provided interface.

## Configuration
- **API Keys:** Configure your API keys in the `.env` file.
- **Router Settings:** Modify settings for the Semantic Router in the `config/router_config.py` file.

## Examples
### General Question
**User:** Hello, how is everything?
**Chatbot:** Everything is great! How can I assist you today?

### Research Question
**User:** What are the benefits of renewable energy?
**Chatbot:** Renewable energy sources have several benefits including reduced greenhouse gas emissions, sustainability, and economic growth. [Source](https://www.example.com/renewable-energy-benefits)

### Confidential Inquiry
**User:** Can you tell me confidential information about XYZ company?
**Chatbot:** I'm sorry, but I cannot provide information on that topic.

### Discriminatory Remark
**User:** [Discriminatory remark]
**Chatbot:** Warning: Please refrain from using discriminatory language. This is your first warning.

## Screenshots
![Chatbot Interaction](path/to/your/image.png)

## Contributing
1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Commit your changes (`git commit -m 'Add new feature'`).
4. Push to the branch (`git push origin feature-branch`).
5. Create a new Pull Request.

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
