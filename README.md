# remailable

Email documents to your ReMarkable tablet.

You can use this by emailing a PDF to remailable@[your-custom-domain].

## Using the public instance of _remailable_ for free

I host a version of this that you can use for free. Emails are not kept and do not go to a real mailbox. (Email binaries are deleted after 24 hours automatically.)

### Setup

Write a new email to [remailable@getneutrality.org](mailto:remailable@getneutrality.org) with nothing in the body and your new-device ReMarkable code in the subject line.

### Usage

Email [remailable@getneutrality.org](mailto:remailable@getneutrality.org) with a PDF attachment. It will be delivered to your ReMarkable tablet.

### Limitations

-   Under 30MB please!
-   That's it :)

## Making Your Own

## To Set Up Before You Start

-   [ ] You'll need to set up an SES domain ([AWS Docs](https://docs.aws.amazon.com/ses/latest/DeveloperGuide/receiving-email-getting-started-before.html)).
-   [ ] Verify the domain ([AWS Docs](https://docs.aws.amazon.com/ses/latest/DeveloperGuide/receiving-email-getting-started-verify.html)).
-   [ ] Set up a S3 hook upon email receipt so that emails are routed to an S3 bucket. (See docs above)
-   [ ] Create a `config.py` file in this directory with the following contents:

```python
class Config:
    BUCKET_NAME = "[YOUR BUCKET NAME]"
    BUCKET_PREFIX = "attachments" # optional; based upon your S3 rule above
```

## To Set Up While You Start

```shell
zappa init
```

You'll need to configure your Zappa file to look like the following:

```js
{
    "production": {
        "app_function": "lambda_main.APP",
        "aws_region": "us-east-1",
        "project_name": "remailable", // call this something cute :)
        "runtime": "python3.7",
        "s3_bucket": [NEW BUCKET NAME] // different bucket name than above
        "events": [
            {
                "function": "lambda_main.upload_handler",
                "event_source": {
                    "arn": "arn:aws:s3:::[Config.BUCKET_NAME GOES HERE]",
                    "events": ["s3:ObjectCreated:*"]
                }
            }
        ]
    }
}
```
