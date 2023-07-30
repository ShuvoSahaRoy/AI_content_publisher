from publish_article import publish_article
from article_writer import generate_article
from image_generator import generate_image

retry_limit = 3


def publish(openai_api_key, site_url, username, password, topic, tags, points, slug, catagory, status, max_tokens):
    
    try:
        retry_count = 0
        success = False

        while retry_count < retry_limit and not success:
            try:
                article = retry_generate_article(topic, openai_api_key,points, max_tokens)
                image_path = retry_generate_image(topic)
                retry_publish_article(topic, article, tags, image_path, site_url, username, password,slug, catagory, status)
                success = True
            except RetryException as e:
                print(f"Failed to publish topic: {e.topic}\nError: {e.reason}")
            except Exception as e:
                print(f"Failed to publish topic: {topic}\nError: {str(e)}")
                break

            retry_count += 1

    except Exception as e:
        print(str(e))

class RetryException(Exception):
    def __init__(self, topic, reason):
        self.topic = topic
        self.reason = reason
        super().__init__(f"Failed to publish topic: {topic}. Reason: {reason}")


def retry_generate_article(topic, openai_api_key,points,max_tokens):
    retry_count = 0
    while retry_count < retry_limit:
        try:
            article = generate_article(topic, openai_api_key,points,max_tokens)
            return article
        except Exception as e:
            retry_count += 1

    raise RetryException(topic, f"Failed to generate article")


def retry_generate_image(topic):
    retry_count = 0
    while retry_count < retry_limit:
        try:
            return generate_image(topic)
        except Exception as e:
            retry_count += 1

    raise RetryException(topic, f"Failed to generate image")


def retry_publish_article(topic, article, tags, image_path, site_url, username, password,slug, catagory, status):
    retry_count = 0
    while retry_count < retry_limit:
        try:
            publish_article(topic, article, tags, image_path, site_url, username, password,slug, catagory, status)
            return
        except Exception as e:
            retry_count += 1

    raise RetryException(topic, f"Failed to publish article")
