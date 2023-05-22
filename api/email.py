import boto3
from botocore.exceptions import ClientError
from jinja2 import Environment, FileSystemLoader

# boto3.set_stream_logger('botocore', level='DEBUG')

class ASes:
    def __init__(self, config, templates_folder='templates'):
        self.sender = config['sender']
        # removed this to instead pass in email_address as arguement from order["order"]["Account"]["email"] in app.py
        # self.recipents = config['recipients']
        self.aws_region = config['aws_region']
        self.charset = config['charset']
        self.template_env = Environment(loader=FileSystemLoader(templates_folder))
        self.client = boto3.client('ses',region_name=config['aws_region'])
        self.template = None
        self._rendered_template = ''

    '''
    template: template filename
    args: dictionary of arguments to load into the template

    Return:
        rendered_template: rendered template object
    '''
    
    def load_template(self, template, args=None):
        self.template = self.template_env.get_template(template)
        
        if args:
            return self.render_template(args)

    def render_template(self, args):
        self._rendered_template = self.template.render(args)
        return self._rendered_template

    def send(self, subject, email_address, body=None):
        if not body:
            body = self._rendered_template
        try:
            response = self.client.send_email(
                Destination={
                    'ToAddresses': [email_address]
                },
                Message={
                    'Body': {
                        'Html': {
                            'Charset': self.charset,
                            'Data': body
                        }
                    },
                    'Subject': {
                        'Charset': self.charset,
                        'Data': subject,
                    },
                },
                Source=self.sender
            )
        except ClientError as e:
            print(e.response['Error']['Message'])
        else:
            print("Email sent! Message ID:"),
            print(response['MessageId'])
