import yaml
from flask import Flask, request, jsonify
from pypdf import PdfReader, PdfWriter

app = Flask(__name__)

global config

with open("config.yml") as f:
    config = yaml.safe_load(f)


@app.route('/render_customer_contract', methods=['POST'])
def render_customer_contract():
    payload = request.get_json()

    reader = PdfReader(config['customer_contract'])
    writer = PdfWriter()
    writer.append(reader)

    for index in range(0, len(reader.pages)):
        writer.update_page_form_field_values(
            writer.pages[index],
            payload
        )

    # TODO: upload file to S3 storage
    with open("out.pdf", "wb") as output_stream:
        writer.write(output_stream)

    return jsonify({"url": "awss3.com"})


if __name__ == "__main__":
    app.run(debug=True)
