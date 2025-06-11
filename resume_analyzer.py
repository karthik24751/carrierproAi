from .utils.file_utils import read_file_content
from .utils.nlp_utils import NLPProcessor
import json
import os
import time
from PyPDF2 import PdfReader
import re
# from pdfminer.pdfparser import PdfParser
# from pdfminer.pdfdocument import PdfDocument
# from pdfminer.pdfpage import PdfPage
# from pdfminer.pdfinterp import PdfInterpreter
# from pdfminer.pdfdevice import PdfDevice

class ResumeAnalyzer:
    def __init__(self):
        self.nlp_processor = NLPProcessor()
        self.cache_dir = 'cache/resume_analysis'
        os.makedirs(self.cache_dir, exist_ok=True)

    def analyze(self, filepath):
        """Analyze a resume and extract key information."""
        # Read resume content
        content = read_file_content(filepath)
        
        # Extract information using NLP
        analysis = {
            'skills': self.nlp_processor.extract_skills(content),
            'education': self.nlp_processor.extract_education(content),
            'experience': self.nlp_processor.extract_experience(content),
            'keywords': self.nlp_processor.extract_keywords(content),
            'sentiment_score': self.nlp_processor.analyze_sentiment(content)
        }
        
        # Cache the analysis
        self._cache_analysis(filepath, analysis)
        
        return analysis

    def calculate_match_score(self, resume_path, job_description):
        """Calculate how well the resume matches a job description."""
        # Read both documents
        resume_content = read_file_content(resume_path)
        
        # Calculate similarity
        similarity_score = self.nlp_processor.calculate_similarity(
            resume_content,
            job_description
        )
        
        # Extract skills from both
        resume_skills = set(self.nlp_processor.extract_skills(resume_content))
        job_skills = set(self.nlp_processor.extract_skills(job_description))
        
        # Calculate skill match
        if not job_skills:
            skill_match = 0
        else:
            skill_match = len(resume_skills.intersection(job_skills)) / len(job_skills)
        
        # Combine scores (70% similarity, 30% skill match)
        final_score = (0.7 * similarity_score) + (0.3 * skill_match)
        
        return {
            'overall_score': round(final_score * 100, 2),
            'similarity_score': round(similarity_score * 100, 2),
            'skill_match_score': round(skill_match * 100, 2),
            'matching_skills': list(resume_skills.intersection(job_skills)),
            'missing_skills': list(job_skills - resume_skills)
        }

    def _cache_analysis(self, filepath, analysis):
        """Cache the analysis results for future use."""
        cache_file = os.path.join(
            self.cache_dir,
            f"{os.path.basename(filepath)}.json"
        )
        
        with open(cache_file, 'w') as f:
            json.dump(analysis, f)

    def get_cached_analysis(self, filepath):
        """Retrieve cached analysis if available."""
        cache_file = os.path.join(
            self.cache_dir,
            f"{os.path.basename(filepath)}.json"
        )
        
        if os.path.exists(cache_file):
            with open(cache_file, 'r') as f:
                return json.load(f)
        return None

    def get_skill_gaps(self, resume_path, job_description):
        """Identify skill gaps between resume and job description."""
        resume_content = read_file_content(resume_path)
        
        # Extract skills from both
        resume_skills = set(self.nlp_processor.extract_skills(resume_content))
        job_skills = set(self.nlp_processor.extract_skills(job_description))
        
        # Find missing and extra skills
        missing_skills = job_skills - resume_skills
        extra_skills = resume_skills - job_skills
        
        return {
            'missing_skills': list(missing_skills),
            'extra_skills': list(extra_skills),
            'matching_skills': list(resume_skills.intersection(job_skills))
        }

    def get_experience_summary(self, resume_path):
        """Generate a summary of work experience."""
        content = read_file_content(resume_path)
        experience = self.nlp_processor.extract_experience(content)
        
        # Analyze experience for key achievements and responsibilities
        summary = {
            'experience_sentences': experience,
            'key_achievements': [],
            'responsibilities': []
        }
        
        # Simple rule-based classification of experience sentences
        achievement_indicators = ['achieved', 'increased', 'improved', 'developed',
                                'implemented', 'created', 'led', 'managed']
        responsibility_indicators = ['responsible for', 'duties included', 'managed',
                                   'oversaw', 'coordinated', 'handled']
        
        for sentence in experience:
            if any(indicator in sentence.lower() for indicator in achievement_indicators):
                summary['key_achievements'].append(sentence)
            elif any(indicator in sentence.lower() for indicator in responsibility_indicators):
                summary['responsibilities'].append(sentence)
        
        return summary

    def _extract_text_from_pdf(self, pdf_path):
        """Extract text from a PDF file."""
        print(f"Attempting to extract text from PDF: {pdf_path}")
        try:
            with open(pdf_path, 'rb') as file:
                reader = PdfReader(file)
                text = ""
                for page in reader.pages:
                    text += page.extract_text() or ""
            print("Successfully extracted text from PDF.")
            return text
        except Exception as e:
            print(f"Error extracting text from PDF {pdf_path}: {e}")
            raise Exception(f"Failed to extract text from PDF: {e}")

    def _extract_name(self, text):
        # Simple placeholder for name extraction
        match = re.search(r"^[A-Z][a-z]+(?: [A-Z][a-z]+){1,3}", text)
        return match.group(0) if match else ""

    def _extract_email(self, text):
        # Simple placeholder for email extraction
        match = re.search(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b", text)
        return match.group(0) if match else ""

    def _extract_phone(self, text):
        # Simple placeholder for phone extraction
        match = re.search(r"\b(?:\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}\b", text)
        return match.group(0) if match else ""

    def _extract_summary(self, text):
        # Placeholder for summary extraction (e.g., first few sentences)
        lines = text.split('\n')
        summary_lines = []
        for line in lines:
            if len(summary_lines) < 3 and line.strip() and not line.strip().startswith(("EXPERIENCE", "EDUCATION", "SKILLS")):
                summary_lines.append(line.strip())
            elif len(summary_lines) >= 3:
                break
        return " ".join(summary_lines)

    def _extract_skills(self, text):
        # Placeholder for skills extraction (simple keyword spotting)
        skills_keywords = ["Python", "Java", "JavaScript", "SQL", "AWS", "Azure", "Docker", "Kubernetes", "React", "Angular", "Vue", "Machine Learning", "Data Analysis", "Project Management"]
        found_skills = [skill for skill in skills_keywords if re.search(r'\b' + re.escape(skill) + r'\b', text, re.IGNORECASE)]
        return found_skills

    def _extract_experience(self, text):
        # Placeholder for experience extraction
        experience_entries = []
        # This is a very basic example; a more robust solution would involve NLP
        return experience_entries

    def _extract_education(self, text):
        # Placeholder for education extraction
        education_entries = []
        # This is a very basic example; a more robust solution would involve NLP
        return education_entries

    def extract_resume_data(self, resume_path):
        """Extract resume data in an editable format."""
        print(f"Starting resume data extraction for: {resume_path}")
        try:
            # Extract text from PDF
            text = self._extract_text_from_pdf(resume_path)
            print(f"Extracted text length: {len(text)}")
            
            # Extract structured data
            data = {
                'name': self._extract_name(text),
                'email': self._extract_email(text),
                'phone': self._extract_phone(text),
                'summary': self._extract_summary(text),
                'skills': self._extract_skills(text),
                'experience': self._extract_experience(text),
                'education': self._extract_education(text)
            }
            print("Successfully extracted structured data.")
            return data
        except Exception as e:
            print(f"Error in extract_resume_data: {e}")
            raise Exception(f"Error extracting resume data: {str(e)}")

    def update_resume(self, resume_path, resume_data):
        """Update resume with new data and generate a new PDF."""
        try:
            # Create a new PDF with the updated data
            output_path = os.path.join(
                os.path.dirname(resume_path),
                f"updated_{os.path.basename(resume_path)}"
            )
            
            # Generate PDF using reportlab
            from reportlab.lib.pagesizes import letter
            from reportlab.pdfgen import canvas
            from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
            from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
            
            doc = SimpleDocTemplate(output_path, pagesize=letter)
            styles = getSampleStyleSheet()
            story = []
            
            # Add name
            name_style = ParagraphStyle(
                'NameStyle',
                parent=styles['Heading1'],
                fontSize=24,
                spaceAfter=30
            )
            story.append(Paragraph(resume_data['name'], name_style))
            
            # Add contact info
            contact_info = f"{resume_data['email']} | {resume_data['phone']}"
            story.append(Paragraph(contact_info, styles['Normal']))
            story.append(Spacer(1, 20))
            
            # Add summary
            story.append(Paragraph("Professional Summary", styles['Heading2']))
            story.append(Paragraph(resume_data['summary'], styles['Normal']))
            story.append(Spacer(1, 20))
            
            # Add skills
            story.append(Paragraph("Skills", styles['Heading2']))
            skills_text = ", ".join(resume_data['skills'])
            story.append(Paragraph(skills_text, styles['Normal']))
            story.append(Spacer(1, 20))
            
            # Add experience
            story.append(Paragraph("Experience", styles['Heading2']))
            for exp in resume_data['experience']:
                exp_text = f"{exp['position']} at {exp['company']}<br/>"
                exp_text += f"{exp['start_date']} - {exp['end_date']}<br/>"
                exp_text += exp['description']
                story.append(Paragraph(exp_text, styles['Normal']))
                story.append(Spacer(1, 12))
            
            # Add education
            story.append(Paragraph("Education", styles['Heading2']))
            for edu in resume_data['education']:
                edu_text = f"{edu['degree']} at {edu['institution']}<br/>"
                edu_text += f"{edu['start_date']} - {edu['end_date']}"
                story.append(Paragraph(edu_text, styles['Normal']))
                story.append(Spacer(1, 12))
            
            # Build PDF
            doc.build(story)
            
            return output_path
        except Exception as e:
            raise Exception(f"Error updating resume: {str(e)}")

    def create_portfolio(self, portfolio_data):
        """Create a portfolio website based on the provided data."""
        try:
            # Create a unique directory for the portfolio
            portfolio_dir = os.path.join(
                os.path.dirname(os.path.dirname(__file__)),
                'static',
                'portfolios',
                f"portfolio_{int(time.time())}"
            )
            os.makedirs(portfolio_dir, exist_ok=True)
            
            # Create portfolio HTML
            html_content = f"""
            <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>{portfolio_data['title']}</title>
                <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
                <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
                <style>
                    .project-card {{ margin-bottom: 2rem; }}
                    .skill-badge {{ margin: 0.2rem; }}
                    .social-links a {{ margin-right: 1rem; }}
                </style>
            </head>
            <body>
                <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
                    <div class="container">
                        <a class="navbar-brand" href="#">{portfolio_data['title']}</a>
                    </div>
                </nav>
                
                <div class="container my-5">
                    <div class="row">
                        <div class="col-md-4">
                            <div class="card mb-4">
                                <div class="card-body">
                                    <h3 class="card-title">About Me</h3>
                                    <p class="card-text">{portfolio_data['about']}</p>
                                    
                                    <h4>Skills</h4>
                                    <div class="skills-section">
                                        {self._generate_skill_badges(portfolio_data['skills'])}
                                    </div>
                                    
                                    <h4 class="mt-4">Contact</h4>
                                    <div class="social-links">
                                        <a href="mailto:{portfolio_data['contact']['email']}">
                                            <i class="fas fa-envelope"></i> Email
                                        </a>
                                        {self._generate_social_links(portfolio_data['contact'])}
                                    </div>
                                </div>
                            </div>
                        </div>
                        
                        <div class="col-md-8">
                            <h2>Projects</h2>
                            {self._generate_project_cards(portfolio_data['projects'])}
                        </div>
                    </div>
                </div>
                
                <footer class="bg-dark text-light py-4 mt-5">
                    <div class="container text-center">
                        <p>&copy; {time.strftime('%Y')} {portfolio_data['title']}</p>
                    </div>
                </footer>
                
                <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
            </body>
            </html>
            """
            
            # Save HTML file
            html_path = os.path.join(portfolio_dir, 'index.html')
            with open(html_path, 'w') as f:
                f.write(html_content)
            
            # Return the URL to access the portfolio
            return f"/static/portfolios/{os.path.basename(portfolio_dir)}/index.html"
        except Exception as e:
            raise Exception(f"Error creating portfolio: {str(e)}")

    def get_enhancement_suggestions(self, resume_path):
        """Get AI-powered resume enhancement suggestions."""
        try:
            # Extract current resume data
            resume_data = self.extract_resume_data(resume_path)
            
            # Generate enhancement suggestions
            enhancements = []
            
            # Check summary
            if len(resume_data['summary'].split()) < 50:
                enhancements.append({
                    'title': 'Professional Summary',
                    'description': 'Your professional summary could be more detailed.',
                    'suggestions': [
                        'Add more specific achievements and skills',
                        'Include your career objectives',
                        'Highlight your unique value proposition'
                    ]
                })
            
            # Check skills
            if len(resume_data['skills']) < 5:
                enhancements.append({
                    'title': 'Skills Section',
                    'description': 'Your skills section could be more comprehensive.',
                    'suggestions': [
                        'Add more technical skills',
                        'Include soft skills',
                        'Specify proficiency levels for key skills'
                    ]
                })
            
            # Check experience
            for exp in resume_data['experience']:
                if len(exp['description'].split()) < 30:
                    enhancements.append({
                        'title': f'Experience: {exp["position"]}',
                        'description': 'This experience entry could be more detailed.',
                        'suggestions': [
                            'Add specific achievements and metrics',
                            'Include technologies and tools used',
                            'Describe your impact on the organization'
                        ]
                    })
            
            # Check education
            if not resume_data['education']:
                enhancements.append({
                    'title': 'Education Section',
                    'description': 'Education section is missing.',
                    'suggestions': [
                        'Add your educational background',
                        'Include relevant certifications',
                        'List any academic achievements'
                    ]
                })
            
            return enhancements
        except Exception as e:
            raise Exception(f"Error generating enhancement suggestions: {str(e)}")

    def _generate_skill_badges(self, skills):
        """Generate HTML for skill badges."""
        return ''.join([
            f'<span class="badge bg-primary skill-badge">{skill}</span>'
            for skill in skills
        ])

    def _generate_social_links(self, contact):
        """Generate HTML for social media links."""
        links = []
        if contact.get('linkedin'):
            links.append(f'<a href="{contact["linkedin"]}" target="_blank"><i class="fab fa-linkedin"></i> LinkedIn</a>')
        if contact.get('github'):
            links.append(f'<a href="{contact["github"]}" target="_blank"><i class="fab fa-github"></i> GitHub</a>')
        return ''.join(links)

    def _generate_project_cards(self, projects):
        """Generate HTML for project cards."""
        if not projects:
            return '<p>No projects listed yet.</p>'
        
        return ''.join([
            f'''
            <div class="card project-card">
                <div class="card-body">
                    <h3 class="card-title">{project['title']}</h3>
                    <p class="card-text">{project['description']}</p>
                    <div class="technologies mb-3">
                        {self._generate_skill_badges(project['technologies'])}
                    </div>
                    {f'<a href="{project["url"]}" class="btn btn-primary" target="_blank">View Project</a>' if project.get('url') else ''}
                </div>
            </div>
            '''
            for project in projects
        ]) 