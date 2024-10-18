# Image API

This is a Django REST API that allows users to authenticate, upload images, and retrieve images based on various filters.

## Features

- User registration and authentication
- Image upload functionality
- Image retrieval with filtering options:
  - By author (case-insensitive)
  - By maximum width
  - By maximum height
- Pagination for image retrieval
- Database seeded with initial images from an external source
- Dynamic test data generation for robust testing

## Technologies Used

- Python 3.x
- Django 5.x
- Django REST Framework
- PostgreSQL
- Docker (for containerization)
- django-pgbulk (for efficient bulk operations)

## Setup

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/image-api.git
   cd image_django_api
   ```

2. Set up a virtual environment:
   ```
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Install dependencies:
   ```
   python3 -m pip install -r requirements.txt
   ```

4. Create a `.env` file in the root directory and add the following line:
   ```
   IMAGE_SEED_URL=https://picsum.photos/v2/list?page=2&limit=100
   ```

5. Set up the PostgreSQL database and update the `DATABASES` configuration in `settings.py`.

6. Run migrations:
   ```
   python3 manage.py migrate
   ```

7. Seed the database with initial images:
   ```
   python3 manage.py seed_images
   ```

8. Run the development server:
   ```
   python3 manage.py runserver
   ```

## API Endpoints

- `POST /api/register/`: Register a new user
- `POST /api/login/`: Login and receive an authentication token
- `GET /api/images/`: Retrieve all images (supports pagination)
- `GET /api/images/?page=2`: Retrieve all images on page 2
- `GET /api/images/?author=<name>`: Retrieve images by author
- `GET /api/images/?max_width=<width>`: Retrieve images with width <= specified value
- `GET /api/images/?max_height=<height>`: Retrieve images with height <= specified value

## Automated Testing

Run the test suite with:

python3 manage.py test

## Manual Testing

### Register a New User

To register a new user, use the following `curl` command:

```bash
curl -X POST -H "Content-Type: application/json" -d '{"username": "your_username", "password": "your_password", "email": "your_email@example.com"}' http://localhost:8000/api/register/
```

### Login to Obtain a Token

After registering, log in to obtain an authentication token:

```bash
curl -X POST -H "Content-Type: application/json" -d '{"username": "your_username", "password": "your_password"}' http://localhost:8000/api/login/
```

The response will include a token:

```json
{
    "token": "your_token_here"
}
```

### Access the Images Endpoint

Now that you have the token, you can access the `/api/images/` endpoint:

```bash
curl -H "Authorization: Token your_token_here" http://localhost:8000/api/images/
```

Replace `your_token_here` with the actual token you received from the login response.


## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License.

This README provides a comprehensive overview of your project, including its features, setup instructions, API endpoints, and deployment information. As you develop your project, you can update this README to reflect any changes or additional features you implement.
Remember to replace yourusername in the clone URL with your actual GitHub username or the appropriate repository URL. Also, you may want to adjust the Python and Django versions to match your actual project setup