Django Blog Application
This is a Django-based blog application that provides a fully functional blogging platform with advanced search, commenting, tagging, pagination, and user authentication features. The project uses both SQLite and PostgreSQL databases. By default, SQLite is used, but PostgreSQL can be enabled with minor configuration changes.

Table of Contents
-Features
-Installation
-Database Setup
-Data Schema
-Advanced Features
-Trigram Similarity Search
-Stemming and Ranking Results
-Pagination
-Comment System with Likes
-Sharing Blog via Email
-User Authentication & Password Hashing
-PostgreSQL Configuration
-License
-Features
-User Authentication:

Users can sign up, log in, and log out.
Passwords are securely hashed using Django's built-in authentication system.
Session management for authenticated users.
Blog Post Management:

Create, edit, and delete blog posts via the Django admin interface.
Blog posts can be tagged with multiple tags for easy categorization and search.
Search & Ranking:

Full-text search with stemming and trigram similarity.
Results are ranked based on relevance.
Fuzzy search using trigram similarity allows typo-tolerant search results.
Pagination:

Blog posts are paginated with 5 posts per page for easier navigation through large datasets.
Comments and Likes:

Users can comment on blog posts.
Comments can be liked by authenticated users.
Share via Email:

Blog posts can be shared with others via email by sending the blog content and link.
Database Support:

SQLite is used by default.
PostgreSQL is supported and can be enabled by uncommenting the configuration in settings.py (see PostgreSQL section below).
Installation
Prerequisites
Python 3.x
Django 5.x
PostgreSQL (optional, for advanced search features)
Steps
Clone the repository:

bash
Copy code
git clone https://github.com/yourusername/blog-app.git
Navigate into the project directory:

bash
Copy code
cd blog-app
Create a virtual environment and activate it:

bash
Copy code
python -m venv venv
source venv/bin/activate  # For Windows: venv\Scripts\activate
Install dependencies:

bash
Copy code
pip install -r requirements.txt
Database Setup
By default, the application is configured to use SQLite. To switch to PostgreSQL, follow the PostgreSQL Configuration section below.

Run migrations to set up the database schema:

bash
Copy code
python manage.py migrate
Create a superuser for accessing the admin panel:

bash
Copy code
python manage.py createsuperuser
Start the development server:

bash
Copy code
python manage.py runserver
Data Schema
The blog app uses the following models:

Blog: The primary model representing a blog post, containing fields such as title, content, author, tags, and published_date.
Tag: Used to categorize blog posts with relevant keywords.
Comment: Allows users to post comments on blog posts, including a "like" feature.
User: Built-in Django user model used for authentication and managing sessions.
Advanced Features
Trigram Similarity Search
To improve search capabilities, trigram similarity is used for fuzzy matching of blog titles and content. This feature allows users to search even with minor typos or partial matches.

Example:

python
Copy code
from django.db.models.functions import TrigramSimilarity

query = 'search term'
blogs = Blog.objects.annotate(similarity=TrigramSimilarity('title', query)).filter(similarity__gt=0.1).order_by('-similarity')
Stemming and Ranking Results
Full-text search functionality is powered by stemming and ranking algorithms, providing search results that are more relevant to the user's query. This improves search accuracy by matching words with similar roots.

Pagination
The blog list view is paginated, displaying 5 posts per page to improve readability and ease of navigation.

Example of pagination in views:

python
Copy code
from django.core.paginator import Paginator

blogs = Blog.objects.all().order_by('-published_date')
paginator = Paginator(blogs, 5)  # 5 blogs per page
Comment System with Likes
Users can comment on blog posts and like comments. The number of likes is shown next to each comment.

Sharing Blog via Email
A blog post can be shared via email using Django's send_mail function. Users can send the blog link to any email address.

Example:

python
Copy code
from django.core.mail import send_mail

def share_blog(request, blog_id):
    blog = get_object_or_404(Blog, id=blog_id)
    send_mail(
        subject=f"Check out this blog: {blog.title}",
        message=blog.content,
        from_email='your_email@example.com',
        recipient_list=[recipient_email],
    )
User Authentication and Password Hashing
Django's built-in authentication system ensures secure handling of user credentials:

Password Hashing: Passwords are hashed before being stored in the database using Django’s default password hashing mechanism (PBKDF2).
Authentication: Session-based authentication allows users to securely log in, log out, and manage their profiles.
PostgreSQL Configuration
If you want to use PostgreSQL for full-text search and trigram similarity, follow these steps:

Install PostgreSQL and create a new database.

Uncomment the PostgreSQL settings in settings.py:

python
Copy code
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'your_database_name',
        'USER': 'your_postgres_user',
        'PASSWORD': 'your_postgres_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
Enable the pg_trgm extension in PostgreSQL to use trigram similarity:

sql
Copy code
CREATE EXTENSION pg_trgm;
Run the database migrations:

bash
Copy code
python manage.py migrate
Now, PostgreSQL will be used, and full-text search and trigram similarity will be fully functional.
