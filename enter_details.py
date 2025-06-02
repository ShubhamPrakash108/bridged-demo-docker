import json

api_key = input("Enter your API KEY: ")
index_name = input("Enter the name of the Index: ").lower()

valid_metrics = ["cosine", "dotproduct", "euclidean"]
metric = input("Enter the metric (Options: cosine, dotproduct, euclidean): ").lower()
while metric not in valid_metrics:
    print("Invalid input. Please enter one of the following: cosine, dotproduct, euclidean.")
    metric = input("Enter the metric (Options: cosine, dotproduct, euclidean): ").lower()

print(f"You selected: {metric}")

config = {
    "api_key": api_key,
    "index_name": index_name,
    "metric": metric
}

with open("config.json", "w") as f:
    json.dump(config, f, indent=4)

print("Configuration saved to config.json")
