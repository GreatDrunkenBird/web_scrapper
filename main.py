from flask import Flask, render_template_string, request
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)


# Function to get webpage content
def get_webpage_content(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return response.text
    else:
        raise Exception(f"Failed to fetch webpage content. Status code: {response.status_code}")


# Function to parse webpage content
def parse_webpage_content(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')

    # Capture page title
    title = soup.title.string if soup.title else 'No title found'

    # Capture all links
    links = [a['href'] for a in soup.find_all('a', href=True)]

    # Capture all image links
    image_links = [img['src'] for img in soup.find_all('img', src=True)]

    # Capture meta description
    meta_description = ''
    description_tag = soup.find('meta', attrs={'name': 'description'})
    if description_tag and 'content' in description_tag.attrs:
        meta_description = description_tag['content']

    return {
        'title': title,
        'links': links,
        'image_links': image_links,
        'meta_description': meta_description
    }


# Main route to display form and results
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        url = request.form['url']
        html_content = get_webpage_content(url)
        scraped_data = parse_webpage_content(html_content)

        return render_template_string(template, scraped_data=scraped_data)

    return render_template_string(template)


# HTML template
template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Web Scraper</title>
</head>
<body>
    <h1>Web Scraper</h1>
    <form method="post">
        <label for="url">Enter URL:</label>
        <input type="text" id="url" name="url" required>
        <button type="submit">Scrape</button>
    </form>

    {% if scraped_data %}
    <h2>Scraped Data</h2>
    <h3>Title</h3>
    <p>{{ scraped_data.title }}</p>

    <h3>Meta Description</h3>
    <p>{{ scraped_data.meta_description }}</p>

    <h3>Links</h3>
    <ul>
        {% for link in scraped_data.links %}
        <li><a href="{{ link }}" target="_blank">{{ link }}</a></li>
        {% endfor %}
    </ul>

    <h3>Image Links</h3>
    <ul>
        {% for img_link in scraped_data.image_links %}
        <li><a href="{{ img_link }}" target="_blank">{{ img_link }}</a></li>
        {% endfor %}
    </ul>
    {% endif %}
</body>
</html>
"""

if __name__ == '__main__':
    app.run(debug=True)
