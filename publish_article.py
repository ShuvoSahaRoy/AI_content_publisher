from wordpress_xmlrpc import Client, WordPressPost
from wordpress_xmlrpc.methods.posts import NewPost
from wordpress_xmlrpc.methods import media


def publish_article(topic, article, tags, image_path, site_url, username, password,slug, catagory, status):
    # # Connect to your WordPress site
    site_url = site_url
    wp = Client(site_url, username, password)

    # Generate the image based on the topic
    image_path = image_path

    # Create a new WordPress post
    post = WordPressPost()
    post.title = f"<strong>{topic}</strong>"
    post.content = article
    post.post_status = status
    post.slug = slug
    post.terms_names = {'post_tag': tags, 'category': catagory}

    # Upload and attach the image to the post
    data = {
        'name': f"{topic}.jpg",
        'type': 'image/jpeg',
    }
    with open(image_path, 'rb') as img_file:
        data['bits'] = img_file.read()
    response = wp.call(media.UploadFile(data))
    attachment_id = response['id']
    post.thumbnail = attachment_id

    # Publish the post
    post_id = wp.call(NewPost(post))
    print(f"Article published successfully! Post ID: {post_id}")