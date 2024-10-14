# Image API

This is a Django REST API that allows users to authenticate, upload images, and retrieve images based on various filters.

## Features

- User registration and authentication
- Image upload functionality
- Image retrieval with filtering options:
  - By author (case-insensitive)
  - By maximum width
  - By maximum height
- Database seeded with 100 initial images

## Technologies Used

- Python 3.x
- Django 5.x
- Django REST Framework
- PostgreSQL
- Docker (for containerization)

## Setup

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/image-api.git
   cd image-api
   ```

2. Set up a virtual environment:
   ```
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Set up the PostgreSQL database and update the `DATABASES` configuration in `settings.py`.

5. Run migrations:
   ```
   python manage.py migrate
   ```

6. Seed the database with initial images:
   ```
   python manage.py seed_images
   ```

7. Run the development server:
   ```
   python manage.py runserver
   ```

## API Endpoints

- `POST /api/register/`: Register a new user
- `POST /api/login/`: Login and receive an authentication token
- `GET /api/images/`: Retrieve all images
- `GET /api/images/?author=<name>`: Retrieve images by author
- `GET /api/images/?max_width=<width>`: Retrieve images with width <= specified value
- `GET /api/images/?max_height=<height>`: Retrieve images with height <= specified value
- `POST /api/images/`: Upload a new image (authenticated users only)

## Testing

Run the test suite with:

python manage.py test

## Deployment

This project can be deployed using Docker. Build and run the Docker container:
docker build -t image-api .
docker run -p 8000:8000 image-api

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License.

This README provides a comprehensive overview of your project, including its features, setup instructions, API endpoints, and deployment information. As you develop your project, you can update this README to reflect any changes or additional features you implement.
Remember to replace yourusername in the clone URL with your actual GitHub username or the appropriate repository URL. Also, you may want to adjust the Python and Django versions to match your actual project setup