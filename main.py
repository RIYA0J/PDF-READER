from flask import Flask, request, render_template, jsonify
from pdf import process_pdf, chat_with_pdf

app = Flask(__name__)


# Route to render the home page
@app.route('/')
def home():
    return render_template('index.html')


# Route to handle PDF upload
@app.route('/upload_pdf', methods=['POST'])
def upload_pdf():
    if 'pdf' not in request.files:
        return jsonify({"error": "No PDF file provided."}), 400

    pdf_file = request.files['pdf']

    try:
        # Process the uploaded PDF
        process_pdf(pdf_file)
        return jsonify({"message": "PDF processed successfully."})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Route to handle user questions
@app.route('/ask', methods=['POST'])
def ask():
    user_question = request.json.get('question')

    if not user_question:
        return jsonify({"error": "No question provided."}), 400

    try:
        # Get the response from the model
        response = chat_with_pdf(user_question)
        return jsonify({"answer": response})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
