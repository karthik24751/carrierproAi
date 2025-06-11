from flask import Flask, render_template, request, jsonify, send_from_directory
import os
from werkzeug.utils import secure_filename
from modules.resume_analyzer import ResumeAnalyzer
from modules.cover_letter import CoverLetterGenerator
from modules.interview import InterviewSystem
from modules.career_recommender import CareerRecommender
from modules.utils.file_utils import allowed_file

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Ensure upload directory exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Initialize components
print("Initializing ResumeAnalyzer...")
resume_analyzer = ResumeAnalyzer()
print("ResumeAnalyzer initialized.")
print("Initializing CoverLetterGenerator...")
cover_letter_gen = CoverLetterGenerator()
print("CoverLetterGenerator initialized.")
print("Initializing InterviewSystem...")
interview_system = InterviewSystem()
print("InterviewSystem initialized.")
print("Initializing CareerRecommender...")
career_recommender = CareerRecommender()
print("CareerRecommender initialized.")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload-resume', methods=['POST'])
def upload_resume():
    if 'resume' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['resume']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        # Pass the absolute path to the resume analyzer
        absolute_filepath = os.path.abspath(filepath)
        return jsonify({'message': 'Resume uploaded successfully', 'resume_path': absolute_filepath}), 200
    else:
        return jsonify({'error': 'Invalid file type. Only PDF is allowed.'}), 400

@app.route('/analyze-match', methods=['POST'])
def analyze_match():
    data = request.json
    if not data or 'resume_path' not in data or 'job_description' not in data:
        return jsonify({'error': 'Missing required data'}), 400
    
    match_score = resume_analyzer.calculate_match_score(
        data['resume_path'],
        data['job_description']
    )
    return jsonify({'match_score': match_score})

@app.route('/generate-cover-letter', methods=['POST'])
def generate_cover_letter():
    data = request.json
    if not data or 'resume_path' not in data or 'job_description' not in data:
        return jsonify({'error': 'Missing required data'}), 400
    
    cover_letter = cover_letter_gen.generate(
        data['resume_path'],
        data['job_description']
    )
    return jsonify({'cover_letter': cover_letter})

@app.route('/start-interview', methods=['POST'])
def start_interview():
    data = request.json
    role = data.get('role')
    level = data.get('level')
    focus = data.get('focus')

    print(f"Received /start-interview request with role: {role}, level: {level}, focus: {focus}")
    print(f"Type of focus received: {type(focus)}")

    if not data or 'role' not in data or 'level' not in data or 'focus' not in data:
        print("Missing required parameters for /start-interview")
        return jsonify({'error': 'Missing required parameters'}), 400
    
    try:
        questions = interview_system.generate_questions(role, level, focus)
        print(f"Generated {len(questions)} questions for role: {role}, level: {level}, focus: {focus}")
        # Store the questions in a session or a temporary storage if needed
        # For now, let's just return them directly
        return jsonify({'questions': questions}), 200
    except ValueError as e:
        print(f"ValueError caught in /start-interview: {e}")
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        print(f"An unexpected error occurred in /start-interview: {e}")
        # Catch any other unexpected errors
        return jsonify({'error': 'An unexpected error occurred: ' + str(e)}), 500

@app.route('/process-answer', methods=['POST'])
def process_answer():
    question = request.form.get('question')
    selected_option = request.form.get('selected_option')
    role = request.form.get('role')
    level = request.form.get('level')
    focus = request.form.get('focus')
    
    if not all([question, selected_option, role, level, focus]):
        return jsonify({'error': 'Missing required parameters'}), 400
    
    try:
        # Process the quiz answer
        analysis = interview_system.process_quiz_answer(question, selected_option, role, level)
        
        return jsonify(analysis)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/get-interview-history', methods=['GET'])
def get_interview_history():
    role = request.args.get('role')
    level = request.args.get('level')
    
    history = interview_system.get_interview_history(role, level)
    return jsonify({'history': history})

@app.route('/get-career-recommendations', methods=['POST'])
def get_career_recommendations():
    data = request.json
    if not data or 'skills' not in data or 'education' not in data:
        return jsonify({'error': 'Missing required data'}), 400
    
    recommendations = career_recommender.get_recommendations(
        data['skills'],
        data['education'],
        data.get('interests', [])
    )
    return jsonify({'recommendations': recommendations})

@app.route('/get-resume-recommendations', methods=['POST'])
def get_resume_recommendations():
    data = request.get_json()
    resume_path = data.get('resume_path')
    
    if not resume_path:
        return jsonify({'error': 'Resume path is required'}), 400
    
    try:
        # Extract skills and experience from resume
        resume_data = resume_analyzer.extract_resume_data(resume_path)
        
        # Get career recommendations based on resume data
        recommendations = career_recommender.get_recommendations_from_resume(resume_data)
        
        return jsonify({'recommendations': recommendations})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/get-resume-data', methods=['POST'])
def get_resume_data():
    try:
        data = request.get_json()
        if not data or 'resume_path' not in data:
            return jsonify({'error': 'Resume path not provided'}), 400

        resume_path = data['resume_path']
        if not os.path.exists(resume_path):
            return jsonify({'error': 'Resume file not found'}), 404

        # Extract resume data using ResumeAnalyzer
        resume_data = resume_analyzer.extract_resume_data(resume_path)
        if not resume_data:
            return jsonify({'error': 'Failed to extract resume data'}), 500

        # Return structured resume data
        return jsonify({
            'name': resume_data.get('name', ''),
            'email': resume_data.get('email', ''),
            'phone': resume_data.get('phone', ''),
            'summary': resume_data.get('summary', ''),
            'skills': resume_data.get('skills', []),
            'experience': resume_data.get('experience', []),
            'education': resume_data.get('education', []),
            'projects': resume_data.get('projects', []),
            'certifications': resume_data.get('certifications', [])
        })

    except Exception as e:
        print(f"Error in get_resume_data: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/update-resume', methods=['POST'])
def update_resume():
    data = request.get_json()
    resume_path = data.get('resume_path')
    resume_data = data.get('resume_data')
    
    if not all([resume_path, resume_data]):
        return jsonify({'error': 'Resume path and data are required'}), 400
    
    try:
        # Update the resume with new data
        updated_path = resume_analyzer.update_resume(resume_path, resume_data)
        return jsonify({'resume_path': updated_path})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/create-portfolio', methods=['POST'])
def create_portfolio():
    data = request.get_json()
    
    if not data:
        return jsonify({'error': 'Portfolio data is required'}), 400
    
    try:
        # Create a portfolio website based on the provided data
        portfolio_url = resume_analyzer.create_portfolio(data)
        return jsonify({'portfolio_url': portfolio_url})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/enhance-resume', methods=['POST'])
def enhance_resume():
    data = request.get_json()
    resume_path = data.get('resume_path')
    
    if not resume_path:
        return jsonify({'error': 'Resume path is required'}), 400
    
    try:
        # Get AI-powered resume enhancement suggestions
        enhancements = resume_analyzer.get_enhancement_suggestions(resume_path)
        return jsonify({'enhancements': enhancements})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/static/<path:filename>')
def serve_static(filename):
    return send_from_directory('static', filename)

if __name__ == '__main__':
    app.run(debug=True, port=5001) 