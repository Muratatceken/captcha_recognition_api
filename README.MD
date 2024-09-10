# Captcha Recognition API

An API for recognizing text in captcha images using a pretrained TrOCR model. This API is built using FastAPI and provides endpoints for recognizing text from uploaded images.

## Table of Contents

* [Project Structure](#project-structure)
* [Installation](#installation)
* [Configuration](#configuration)
* [Usage](#usage)
* [Endpoints](#endpoints)
* [Authentication](#authentication)
* [Logging](#logging)
* [Error Handling](#error-handling)
* [Contributing](#contributing)
* [License](#license)


## Project Structure

The project is organized as follows:

app/
├── config/
│   └── config.yml          # Configuration file
├── model/
│   └── model.py            # TrOCR model class for image processing and text recognition
├── routes/
│   └── captcha_routes.py   # FastAPI routes for the API
├── security/
│   └── auth.py             # Authentication logic
├── utils/
│   └── yaml_loader.py      # Utility for loading YAML configuration
├── constants/
│   └── status_code.py      # Status codes for API responses
└── main.py                 # Entry point for the FastAPI application


## Installation

1. Clone the repository:

   ```
   git clone `<repository-url>`
   cd captcha-recognition
   ```
2. **Install dependencies:** Make sure you have Python 3.8 or higher. Install required packages using pip:

   ```
   pip install -r requirements.txt
   ```
3. Run the FastAPI server:

   ```
   uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

   ```


## Usage

* **API endpoint:** `/recognize`
* **Method:** `POST`
* **Content-Type:** `multipart/form-data`
* **Authorization:** Bearer Token (see** **[Authentication](#authentication))

### Example Request

To recognize text from a captcha image, use the following command:

```
curl -X 'POST' \
  'http://0.0.0.0:8000/recognize' \
  -H 'accept: application/json' \
  -H 'Authorization: Bearer your_token_here' \
  -F 'file=@/path/to/your/image.png'

```


### Response

* **Success:** `{"status": 0, "details": {"recognized_text": "sample_text"}}`
* **Failure:** `{"status": 1, "details": "Error message"}`

## Endpoints

* **`POST /recognize`** : Recognize text in a captcha image.
* **Request Parameters:**
  * `file`: UploadFile (PNG or JPEG format)
* **Response:**
  * JSON object containing status code and details.

## Authentication

This API uses token-based authentication. Include an** **`Authorization` header with the token in your requests:

```
Authorization: Bearer your_token_here

```


The default token is set in the** **`config.yml` file.

## Logging

Logging configuration is defined in the** **`config.yml` file. Logs are saved to** **`logs/app.log`.

## Error Handling

Error messages are handled via status codes defined in** **`app/constants/status_code.py`. The following error codes are used:

* `0`: Successful
* `1`: Missing file input
* `2`: Unsupported file type
* `3`: File processing failed
* `4`: Error during recognition

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository.
2. Create a new branch:** **`git checkout -b feature-name`.
3. Make your changes.
4. Commit and push your changes:** **`git commit -am 'Add new feature'`.
5. Open a pull request.

## License

This project is licensed under the MIT License.
