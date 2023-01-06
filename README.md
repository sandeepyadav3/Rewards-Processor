# Rewards-Processor

An API service that calculates the reward points earned for every receipt.

Endpoint: Process Receipts

- Path: /receipts/process
- Method: POST
- Payload: Receipt JSON
- Response: JSON containing an id for the receipt

Endpoint: Fetch Points

- Path: /receipts/{id}/points
- Method: GET
- Response: A JSON object containing the number of points awarded.

# Environment Setup
### Installing pip
- python get-pip.py

### Installing Flask
- pip install flask

### Deploying the web-server
- python ReceiptProcessor.py
