import argparse
import requests
import json

def main():
    """
    This script calls a Flask API endpoint to measure and mitigate bias in advertising data.
    
    The script accepts two arguments:
    - `url`: The OpenShift route URL where the Flask API is accessible.
    - `random_seed`: An integer value used as the random seed for the request. Default is 42.
    
    The request data sent to the API includes:
    - `target_label_name`: The name of the target label column, which is "predicted_conversion".
    - `scores_name`: The name of the scores column, which is "predicted_probability".
    - `random_seed`: The random seed value provided as an argument.
    
    The `predicted_conversion` field represents the binary predicted conversion obtained by thresholding the predicted probability.
    The `predicted_probability` field represents the probability of a user clicking the advertisement according to the model.
    
    Example usage:
        python call_api.py --url <your-openshift-route-url> --random_seed 42
    """
    parser = argparse.ArgumentParser(description="Call Flask API with specified parameters.")
    parser.add_argument('--url', type=str, required=True, help="The OpenShift route URL.")
    parser.add_argument('--random_seed', type=int, default=42, help="Random seed for the request.")
    
    args = parser.parse_args()

    url = f"http://{args.url}/measure_mitigate_bias"
    data = {
        "target_label_name": "predicted_conversion",
        "scores_name": "predicted_probability",
        "random_seed": args.random_seed
    }

    response = requests.post(url, json=data)
    print(response.json())

if __name__ == "__main__":
    main()
