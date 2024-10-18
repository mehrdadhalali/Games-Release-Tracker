# 🚀 Extraction Scripts

This folder contains all of the web-scrapers. These currently include
- [Steam](https://store.steampowered.com/)
- [GOG](https://www.gog.com/en/games)
- [Epic Games](https://store.epicgames.com/en-US/)

---
## 🖥️ Instructions For Adding A New Web-Scraper

First, make sure, you have deployed our code using [the instructions in the Terraform README.](../terraform/README.md)

1. To add a new web-scraper that you have written, make sure it has the following configuration:
- The code should run with a single command.
- It shouldn't accept any inputs.
- The output should be the following format:
```
{
    "platform": "platform",
    "listings": [
        {
            "title": "A Game Title",
            "description": "Description of the game.",
            "release_date": "DD/MM/YYYY",
            "operating_systems": ["Windows", "MacOS", "Linux"],
            "genres": ["Action", "Adventure"],
            "is_nsfw": False,
            "tags": [],
            "current_price": 4999,
            "url": "https://www.example.com/",
            "img_url": "https://www.example.com/image"
        },
        {
            "title": "Another Game Title",
            ...
        }
    ]
}

```

2. Next, create a script called `lambda_handler.py`, it should include a function called `lambda_handler`, accepting arguments `event, session` with the following output:

```
    {
        "statusCode": 200,
        "body": {
            "data": json.dumps(output)
        }
    }

```
Where `output` is the output of your function.

3. Create a `Dockerfile`, and containerise your scripts.
4. Push your Docker image to an ECR repository.
5. Create a Lambda that uses the image.
6. Add the Lambda to the pre-existing parallel lambdas in the step-function.
7. Add a new entry to the database, to the `platform` table, with the name of your platform.