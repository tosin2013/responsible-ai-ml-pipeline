#!/bin/bash

# Function to display help
display_help() {
    echo "Usage: $0 [options]"
    echo ""
    echo "Options:"
    echo "  --install                      Install aider-chat"
    echo "  --create-venv                  Create a virtual environment for installation"
    echo "  --set-deepseek-key <key>       Set the DeepSeek API key"
    echo "  --set-openai-key <key>         Set the OpenAI API key"
    echo "  --set-openrouter-key <key>     Set the OpenRouter API key"
    echo "  --set-gemini-key <key>         Set the Gemini API key"
    echo "  --set-groq-key <key>           Set the Groq API key"
    echo "  --set-azure-key <key>          Set the Azure API key"
    echo "  --set-cohere-key <key>         Set the Cohere API key"
    echo "  --set-anthropic-key <key>      Set the Anthropic API key"
    echo "  --deepseek                     Start aider with DeepSeek Coder V2"
    echo "  --openai <option> [args]       Start aider with OpenAI models"
    echo "    --default                    Use default OpenAI model"
    echo "    --4-turbo                    Use GPT-4 Turbo model"
    echo "    --35-turbo                   Use GPT-3.5 Turbo model"
    echo "    --models                     List models available from OpenAI"
    echo "    --custom <endpoint> <model>  Use custom OpenAI endpoint and model"
    echo "  --ollama <model>               Pull and serve an Ollama model"
    echo "  --openrouter <option> [args]   Start aider with OpenRouter models"
    echo "    --model <provider>/<model>   Use specific OpenRouter model"
    echo "    --models                     List models available from OpenRouter"
    echo "  --gemini                       Start aider with Gemini models"
    echo "    --models                     List models available from Gemini"
    echo "  --groq                         Start aider with Groq models"
    echo "    --models                     List models available from Groq"
    echo "  --azure <deployment>           Start aider with Azure models"
    echo "    --models                     List models available from Azure"
    echo "  --cohere                       Start aider with Cohere models"
    echo "    --models                     List models available from Cohere"
    echo "  --anthropic                    Start aider with Anthropic models"
    echo "    --opus                       Use Claude 3 Opus model"
    echo "    --models                     List models available from Anthropic"
    echo "  --help                         Display this help message"
    echo ""
    echo "For more information, visit: https://aider.chat/"
}

# Function to create and activate virtual environment
create_venv() {
    python3 -m venv aider-env
    source aider-env/bin/activate
}

# Function to activate virtual environment if it exists
activate_venv() {
    if [ -d "aider-env" ]; then
        source aider-env/bin/activate
    fi
}

# Function to install aider-chat
install_aider() {
    activate_venv
    pip install aider-chat
}

# Helper function to update or add keys to model_keys.conf
update_model_keys_conf() {
    model=$1
    key_name=$2
    key_value=$3
    model_keys_file=~/model_keys.conf

    # Ensure the configuration file exists
    touch "$model_keys_file"

    # Remove existing entry if it exists
    grep -v "^$model:" "$model_keys_file" > "$model_keys_file.tmp"
    mv "$model_keys_file.tmp" "$model_keys_file"

    # Add new key entry
    echo "$model:$key_name:$key_value" >> "$model_keys_file"
}

# Function to set DeepSeek API key
set_deepseek_key() {
    update_model_keys_conf "deepseek/deepseek-coder" "DEEPSEEK_API_KEY" $1
}

# Function to set OpenAI API key
set_openai_key() {
    update_model_keys_conf "openai-gpt-4" "OPENAI_API_KEY" $1
}

# Function to set OpenRouter API key
set_openrouter_key() {
    update_model_keys_conf "openrouter-model-x" "OPENROUTER_API_KEY" $1
}

# Function to set Gemini API key
set_gemini_key() {
    update_model_keys_conf "gemini/gemini-1.5-pro-latest" "GEMINI_API_KEY" $1
}

# Function to set Groq API key
set_groq_key() {
    update_model_keys_conf "groq/llama3-70b-8192" "GROQ_API_KEY" $1
}

# Function to set Azure API key
set_azure_key() {
    update_model_keys_conf "azure-model" "AZURE_API_KEY" $1
    export AZURE_API_VERSION="2023-05-15"
    export AZURE_API_BASE="https://myendpt.openai.azure.com"
}

# Function to set Cohere API key
set_cohere_key() {
    update_model_keys_conf "command-r-plus" "COHERE_API_KEY" $1
}

# Function to set Anthropic API key
set_anthropic_key() {
    update_model_keys_conf "opus" "ANTHROPIC_API_KEY" $1
}

# Function to check if Ollama model exists
ollama_model_exists() {
    model=$1
    ollama list | grep -q "^$model$"
}

# Function to pull and serve Ollama model if necessary
setup_ollama() {
    model=$1

    if lsof -Pi :11434 -sTCP:LISTEN -t >/dev/null ; then
        echo "Port 11434 is already in use."
        if ollama_model_exists $model ; then
            echo "Model $model already exists."
        else
            echo "Model $model does not exist, pulling the model..."
            if ! ollama pull $model ; then
                echo "Error: Failed to pull model $model"
                exit 1
            fi
        fi
    else
        echo "Pulling and serving model $model..."
        if ! ollama pull $model ; then
            echo "Error: Failed to pull model $model"
            exit 1
        fi
        ollama serve &
    fi
}

# Function to start aider with specified model
start_aider() {
    activate_venv
    model=$1
    model_keys_file=~/model_keys.conf

    if [[ $model == ollama/* ]]; then
        echo "Starting aider with local Ollama model: $model"
        aider --model "$model"
        return
    fi

    # Check if the model configuration file exists
    if [ ! -f "$model_keys_file" ]; then
        echo "Model configuration file not found: $model_keys_file"
        exit 1
    fi

    # Extract model entry
    model_entry=$(grep "^$model:" "$model_keys_file")
    if [ -z "$model_entry" ]; then
        echo "Model not found in configuration file: $model"
        exit 1
    else
        key_name=$(echo $model_entry | cut -d ':' -f 2)
        api_key=$(echo $model_entry | cut -d ':' -f 3)
        export $key_name="$api_key"
        echo "Starting aider with model: $model and API key name: $key_name"
        aider --model "$model"
    fi
}

# Parse arguments
if [[ $# -eq 0 ]]; then
    display_help
    exit 0
fi

# Variable to check if virtual environment should be created
create_venv_flag=false

while [[ $# -gt 0 ]]; do
    case $1 in
        --install)
            if $create_venv_flag; then
                create_venv
            fi
            install_aider
            shift
            ;;
        --create-venv)
            create_venv_flag=true
            shift
            ;;
        --set-deepseek-key)
            if [[ -z $2 ]]; then
                echo "Missing argument for --set-deepseek-key"
                display_help
                exit 1
            fi
            set_deepseek_key $2
            shift 2
            ;;
        --set-openai-key)
            if [[ -z $2 ]]; then
                echo "Missing argument for --set-openai-key"
                display_help
                exit 1
            fi
            set_openai_key $2
            shift 2
            ;;
        --set-openrouter-key)
            if [[ -z $2 ]]; then
                echo "Missing argument for --set-openrouter-key"
                display_help
                exit 1
            fi
            set_openrouter_key $2
            shift 2
            ;;
        --set-gemini-key)
            if [[ -z $2 ]]; then
                echo "Missing argument for --set-gemini-key"
                display_help
                exit 1
            fi
            set_gemini_key $2
            shift 2
            ;;
        --set-groq-key)
            if [[ -z $2 ]]; then
                echo "Missing argument for --set-groq-key"
                display_help
                exit 1
            fi
            set_groq_key $2
            shift 2
            ;;
        --set-azure-key)
            if [[ -z $2 ]]; then
                echo "Missing argument for --set-azure-key"
                display_help
                exit 1
            fi
            set_azure_key $2
            shift 2
            ;;
        --set-cohere-key)
            if [[ -z $2 ]]; then
                echo "Missing argument for --set-cohere-key"
                display_help
                exit 1
            fi
            set_cohere_key $2
            shift 2
            ;;
        --set-anthropic-key)
            if [[ -z $2 ]]; then
                echo "Missing argument for --set-anthropic-key"
                display_help
                exit 1
            fi
            set_anthropic_key $2
            shift 2
            ;;
        --deepseek)
            start_aider "deepseek/deepseek-coder"
            shift
            ;;
        --openai)
            case $2 in
                --default)
                    start_aider "openai-gpt-4"
                    ;;
                --4-turbo)
                    start_aider "openai-gpt-4-turbo"
                    ;;
                --35-turbo)
                    start_aider "openai-gpt-3.5-turbo"
                    ;;
                --models)
                    aider --models openai/
                    ;;
                --custom)
                    if [[ -z $3 || -z $4 ]]; then
                        echo "Missing arguments for --custom"
                        display_help
                        exit 1
                    fi
                    export OPENAI_API_BASE=$3
                    aider --model openai/$4
                    shift 2
                    ;;
                *)
                    echo "Invalid OpenAI option"
                    display_help
                    exit 1
                    ;;
            esac
            shift 2
            ;;
        --ollama)
            if [[ -z $2 ]]; then
                echo "Missing argument for --ollama"
                display_help
                exit 1
            fi
            setup_ollama $2
            start_aider "ollama/$2"
            shift 2
            ;;
        --openrouter)
            case $2 in
                --model)
                    if [[ -z $3 ]]; then
                        echo "Missing argument for --model"
                        display_help
                        exit 1
                    fi
                    start_aider "openrouter/$3"
                    shift 1
                    ;;
                --models)
                    aider --models openrouter/
                    ;;
                *)
                    echo "Invalid OpenRouter option"
                    display_help
                    exit 1
                    ;;
            esac
            shift 2
            ;;
        --gemini)
            start_aider "gemini/gemini-1.5-pro-latest"
            shift
            ;;
        --groq)
            start_aider "groq/llama3-70b-8192"
            shift
            ;;
        --azure)
            if [[ -z $2 ]]; then
                echo "Missing argument for --azure"
                display_help
                exit 1
            fi
            start_aider "azure/$2"
            shift 2
            ;;
        --cohere)
            start_aider "cohere/command-r-plus"
            shift
            ;;
        --anthropic)
            case $2 in
                --opus)
                    start_aider "anthropic/claude-3-opus"
                    ;;
                --models)
                    aider --models anthropic/
                    ;;
                *)
                    start_aider "anthropic/claude-3-sonnet"
                    ;;
            esac
            shift 2
            ;;
        --help)
            display_help
            exit 0
            ;;
        *)
            echo "Invalid option. Use --help for usage information."
            display_help
            exit 1
            ;;
    esac
done

# Specific handling for Ollama address in use
if [[ $1 == "--ollama" ]]; then
    setup_ollama $2
    if lsof -Pi :11434 -sTCP:LISTEN -t >/dev/null ; then
        echo "Error: Port 11434 is already in use."
        if ollama_model_exists $2 ; then
            echo "Model $2 already exists."
        else
            echo "Model $2 does not exist, pulling the model..."
            if ! ollama pull $2 ; then
                echo "Error: Failed to pull model $2"
                exit 1
            fi
        fi
    else
        echo "Pulling and serving model $2..."
        if ! ollama pull $2 ; then
            echo "Error: Failed to pull model $2"
            exit 1
        fi
        ollama serve &
    fi
fi
