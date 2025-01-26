from flask import Flask, render_template, request, jsonify
from intern_onboarding import InternOnboarding
import json

app = Flask(__name__)
onboarding = InternOnboarding()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/company_overview', methods=['GET', 'POST'])
def company_overview():
    if request.method == 'GET':
        return render_template('company_overview.html', summary=onboarding.company_summary)
    else:
        try:
            data = request.get_json()
            question = data.get('question')
            prompt = f"Using the provided company information, please answer this question: {question}\n\nCompany Information:\n{onboarding.company_info}"
            response = onboarding.get_ai_response(prompt)
            return jsonify({'response': response})
        except Exception as e:
            print(f"Error processing question: {str(e)}")
            return jsonify({'response': f"An error occurred: {str(e)}"}), 500

@app.route('/intern_responsibilities', methods=['GET', 'POST'])
def intern_responsibilities():
    if request.method == 'GET':
        return render_template('responsibilities.html')
    else:
        try:
            data = request.get_json()
            intern_type = data.get('intern_type')
            question = data.get('question')
            
            if question:
                # Handle follow-up question
                responsibilities = onboarding.load_specific_responsibilities(intern_type)
                prompt = (
                    f"Using both the intern responsibilities information and company information provided, "
                    f"please answer this question about the {intern_type} internship role: {question}\n\n"
                    f"Role-Specific Responsibilities:\n{responsibilities}\n\n"
                    f"Company Information:\n{onboarding.company_info}"
                )
                response = onboarding.get_ai_response(prompt)
                return jsonify({'response': response})
            elif intern_type:
                # Handle intern type selection
                responsibilities = onboarding.load_specific_responsibilities(intern_type)
                return jsonify({'responsibilities': responsibilities})
            else:
                return jsonify({'error': 'No intern_type or question provided'}), 400
                
        except Exception as e:
            print(f"Error processing request: {str(e)}")
            return jsonify({'error': f"An error occurred: {str(e)}"}), 500

@app.route('/tools_technologies', methods=['GET', 'POST'])
def tools_technologies():
    if request.method == 'GET':
        return render_template('tools.html', summary=onboarding.tools_summary)
    else:
        data = request.get_json()
        intern_type = data.get('intern_type')
        question = data.get('question')
        
        prompt = (
            f"Based on the following detailed information about our tools and technologies:\n\n{onboarding.tools_info}\n\n"
            f"Please answer this question for a {intern_type} intern: {question}"
        )
        response = onboarding.get_ai_response(prompt)
        return jsonify({'response': response})

@app.route('/project_expectations', methods=['GET', 'POST'])
def project_expectations():
    if request.method == 'GET':
        return render_template('expectations.html', summary=onboarding.expectations_summary)
    else:
        data = request.get_json()
        question = data.get('question')
        prompt = (
            "Based on the following detailed information:\n\n"
            f"Project Expectations:\n{onboarding.project_info}\n\n"
            f"Company Information:\n{onboarding.company_info}\n\n"
            f"Please answer this question about project expectations: {question}"
        )
        response = onboarding.get_ai_response(prompt)
        return jsonify({'response': response})

@app.route('/save_conversation', methods=['POST'])
def save_conversation():
    return jsonify({'result': onboarding.save_conversation()})

if __name__ == '__main__':
    app.run(debug=True) 