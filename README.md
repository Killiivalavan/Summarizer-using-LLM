# Text Summarizer with Ollama

A powerful Python-based text summarization tool that leverages Ollama's language models to generate accurate and concise summaries of text content. This tool is designed to help users quickly extract key information from lengthy documents, articles, or any text input.

## Description

The Text Summarizer with Ollama is a robust solution for automated text summarization. It utilizes Ollama's advanced language models to analyze and condense text while preserving the most important information. This tool is particularly useful for:

- Researchers needing to summarize academic papers
- Content creators processing large amounts of text
- Students summarizing study materials
- Professionals needing quick summaries of documents
- Anyone looking to extract key points from lengthy texts

## Features

- **Intelligent Summarization**: Leverages Ollama's language models for context-aware summarization
- **Flexible Input**: Accepts various text input methods (file upload, direct text input)
- **Customizable Output**: Adjust summary length and style based on your needs
- **Preservation of Key Information**: Maintains critical points while reducing text length
- **Easy-to-Use Interface**: Simple command-line interface for straightforward operation

## Prerequisites

Before using this tool, ensure you have the following installed:

- Python 3.6 or higher
- Ollama installed and running on your system
- Required Python packages:
  ```bash
  pip install ollama
  pip install requests
  pip install [other-dependencies]
  ```

## Installation

1. First, clone this repository to your local machine:
   ```bash
   git clone https://github.com/yourusername/text-summarizer-ollama.git
   ```

2. Navigate to the project directory:
   ```bash
   cd text-summarizer-ollama
   ```

3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Ensure Ollama is properly installed and running on your system:
   ```bash
   ollama --version
   ```

## Usage

### Basic Usage

Run the summarizer with default settings:
```bash
python summarizer-ollama.py --input "path/to/your/text/file.txt"
```

### Advanced Options

The tool supports various command-line arguments for customization:

```bash
python summarizer-ollama.py \
    --input "path/to/file.txt" \
    --model "llama2" \
    --length "medium" \
    --output "summary.txt"
```

### Command Line Arguments

- `--input`: Path to input text file or direct text string
- `--model`: Choose the Ollama model (default: llama2)
- `--length`: Desired summary length (short/medium/long)
- `--output`: Output file path (optional)

## Example

Input:
```bash
python summarizer-ollama.py --input "article.txt" --length "short"
```

Output:
```
[Your summary will appear here, maintaining key points while being concise]
```

## Configuration

### Model Selection

The tool supports various Ollama models. You can specify your preferred model using the `--model` argument:

- llama2 (default)
- mistral
- [other supported models]

### Summary Length Options

- `short`: ~20% of original length
- `medium`: ~40% of original length
- `long`: ~60% of original length

## Troubleshooting

Common issues and solutions:

1. **Ollama Connection Error**
   - Ensure Ollama is running
   - Check your network connection
   - Verify Ollama installation

2. **Memory Issues**
   - Try processing smaller chunks of text
   - Use a more memory-efficient model

## Contributing

Contributions are welcome! To contribute:

1. Fork the repository
2. Create a new branch (`git checkout -b feature/improvement`)
3. Make your changes
4. Commit your changes (`git commit -am 'Add new feature'`)
5. Push to the branch (`git push origin feature/improvement`)
6. Create a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Ollama team for their excellent language models
- Contributors to the project
- Open source community for various dependencies

## Contact

For questions, suggestions, or issues, please:
- Open an issue in the GitHub repository
- Contact: [Your Contact Information]

## Project Status

This project is actively maintained and under continuous development. Check the releases page for the latest updates and improvements. 