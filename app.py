import uuid
import boto3
from flask import Flask, request, jsonify
from pypdf import PdfReader, PdfWriter

from config import Config

app = Flask(__name__)
global_config = Config("config.yml")
s3_client = boto3.client("s3", region_name=global_config.aws['region'],
                         aws_access_key_id=global_config.aws['access_key'],
                         aws_secret_access_key=global_config.aws['secret_access_key'])


def render_with_type(template=global_config.customer_contract):
    payload = request.get_json()

    reader = PdfReader(template)
    writer = PdfWriter()
    writer.append(reader)

    for index in range(0, len(reader.pages)):
        writer.update_page_form_field_values(
            writer.pages[index],
            payload
        )

    with open("/tmp/out.pdf", "wb") as output_stream:
        writer.write(output_stream)

    with open("/tmp/out.pdf", "rb") as input_stream:
        filename = uuid.uuid4()
        s3_client.put_object(Body=input_stream, Bucket=global_config.aws['bucket'],
                             Key=str(filename) + ".pdf",
                             ACL="public-read")

    return jsonify({"uuid": filename})


@app.route('/render_customer_contract', methods=['POST'])
def render_customer_contract():
    return render_with_type(global_config.customer_contract)


@app.route('/render_partner_contract', methods=['POST'])
def render_partner_contract():
    return render_with_type(global_config.partner_contract)


if __name__ == "__main__":
    app.run(debug=True)
