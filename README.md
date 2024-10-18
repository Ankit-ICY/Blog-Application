# Django Blog Application

This is a Django-based blog application that provides a fully functional blogging platform with advanced search, commenting, tagging, pagination, and user authentication features. The project uses both SQLite and PostgreSQL databases. By default, SQLite is used, but PostgreSQL can be enabled with minor configuration changes.

---

## Table of Contents

- [Features](#features)
- [Installation](#installation)
  - [Database Setup](#database-setup)
- [Data Schema](#data-schema)
- [Advanced Features](#advanced-features)
  - [Trigram Similarity Search](#trigram-similarity-search)
  - [Stemming and Ranking Results](#stemming-and-ranking-results)
  - [Pagination](#pagination)
  - [Comment System with Likes](#comment-system-with-likes)
  - [Sharing Blog via Email](#sharing-blog-via-email)
  - [User Authentication & Password Hashing](#user-authentication-and-password-hashing)
- [PostgreSQL Configuration](#postgresql-configuration)
- [License](#license)

---

## Features

1. **User Authentication**:
   - Users can sign up, log in, and log out.
   - Passwords are securely hashed using Django's built-in authentication system.
   - Session management for authenticated users.
   
2. **Blog Post Management**:
   - Create, edit, and delete blog posts via the Django admin interface.
   - Blog posts can be tagged with multiple tags for easy categorization and search.

3. **Search & Ranking**:
   - Full-text search with stemming and trigram similarity.
   - Results are ranked based on relevance.
   - Fuzzy search using trigram similarity allows typo-tolerant search results.

4. **Pagination**:
   - Blog posts are paginated with 5 posts per page for easier navigation through large datasets.

5. **Comments and Likes**:
   - Users can comment on blog posts.
   - Comments can be liked by authenticated users.

6. **Share via Email**:
   - Blog posts can be shared with others via email by sending the blog content and link.

7. **Database Support**:
   - SQLite is used by default.
   - PostgreSQL is supported and can be enabled by uncommenting the configuration in `settings.py` (see PostgreSQL section below).

---

## Installation

### Prerequisites

- Python 3.x
- Django 5.x
- PostgreSQL (optional, for advanced search features)

### Steps

1. Clone the repository:

    ```bash
    git clone https://github.com/yourusername/blog-app.git
    ```

2. Navigate into the project directory:

    ```bash
    cd blog-app
    ```

3. Create a virtual environment and activate it:

    ```bash
    python -m venv venv
    source venv/bin/activate  # For Windows: venv\Scripts\activate
    ```

4. Install dependencies:

    ```bash
    pip install -r requirements.txt
    ```

### Database Setup

By default, the application is configured to use **SQLite**. To switch to **PostgreSQL**, follow the [PostgreSQL Configuration](#postgresql-configuration) section below.

5. Run migrations to set up the database schema:

    ```bash
    python manage.py migrate
    ```

6. Create a superuser for accessing the admin panel:

    ```bash
    python manage.py createsuperuser
    ```

7. Start the development server:

    ```bash
    python manage.py runserver
    ```

---

## Data Schema

The blog app uses the following models:

- **Blog**: The primary model representing a blog post, containing fields such as `title`, `content`, `author`, `tags`, and `published_date`.
- **Tag**: Used to categorize blog posts with relevant keywords.
- **Comment**: Allows users to post comments on blog posts, including a "like" feature.
- **User**: Built-in Django user model used for authentication and managing sessions.

---

## Advanced Features

### Trigram Similarity Search

To improve search capabilities, trigram similarity is used for fuzzy matching of blog titles and content. This feature allows users to search even with minor typos or partial matches.

**Example:**

```python
from django.db.models.functions import TrigramSimilarity

query = 'search term'
blogs = Blog.objects.annotate(similarity=TrigramSimilarity('title', query)).filter(similarity__gt=0.1).order_by('-similarity')
