import json
import os
from .utils.nlp_utils import NLPProcessor

class CareerRecommender:
    def __init__(self):
        self.nlp_processor = NLPProcessor()
        self.career_paths = self._load_career_paths()
        self.skill_weights = self._load_skill_weights()
        self.recommendation_history_dir = 'data/recommendations'
        os.makedirs(self.recommendation_history_dir, exist_ok=True)

    def _load_career_paths(self):
        """Load career paths and their requirements."""
        return {
            'software_engineer': {
                'required_skills': [
                    'programming', 'software development', 'algorithms',
                    'data structures', 'version control', 'testing'
                ],
                'preferred_skills': [
                    'agile', 'scrum', 'ci/cd', 'cloud computing',
                    'database', 'api development', 'system design'
                ],
                'education': ['computer science', 'software engineering', 'information technology'],
                'description': 'Designs, develops, and maintains software applications and systems.',
                'growth_path': [
                    'junior software engineer',
                    'software engineer',
                    'senior software engineer',
                    'tech lead',
                    'software architect'
                ]
            },
            'data_scientist': {
                'required_skills': [
                    'statistics', 'machine learning', 'python',
                    'data analysis', 'data visualization', 'sql'
                ],
                'preferred_skills': [
                    'deep learning', 'natural language processing',
                    'big data', 'cloud computing', 'experiment design'
                ],
                'education': ['data science', 'statistics', 'computer science', 'mathematics'],
                'description': 'Analyzes complex data sets to help guide business decisions.',
                'growth_path': [
                    'data analyst',
                    'data scientist',
                    'senior data scientist',
                    'lead data scientist',
                    'data science manager'
                ]
            },
            'product_manager': {
                'required_skills': [
                    'product strategy', 'market research', 'user experience',
                    'agile', 'project management', 'data analysis'
                ],
                'preferred_skills': [
                    'user research', 'product analytics', 'stakeholder management',
                    'technical background', 'business acumen'
                ],
                'education': ['business', 'computer science', 'engineering', 'marketing'],
                'description': 'Leads product development and strategy to meet business goals.',
                'growth_path': [
                    'associate product manager',
                    'product manager',
                    'senior product manager',
                    'product director',
                    'head of product'
                ]
            },
            'devops_engineer': {
                'required_skills': [
                    'ci/cd', 'cloud computing', 'containerization',
                    'infrastructure as code', 'monitoring', 'automation'
                ],
                'preferred_skills': [
                    'kubernetes', 'docker', 'aws', 'azure', 'gcp',
                    'python', 'shell scripting', 'system administration'
                ],
                'education': ['computer science', 'information technology', 'systems engineering'],
                'description': 'Manages and automates infrastructure and deployment processes.',
                'growth_path': [
                    'devops engineer',
                    'senior devops engineer',
                    'devops architect',
                    'platform engineer',
                    'site reliability engineer'
                ]
            }
        }

    def _load_skill_weights(self):
        """Load weights for different skill categories."""
        return {
            'required_skills': 1.0,
            'preferred_skills': 0.7,
            'education': 0.8,
            'interests': 0.5
        }

    def get_recommendations(self, skills, education, interests=None):
        """Get career path recommendations based on skills, education, and interests."""
        if interests is None:
            interests = []
        
        # Calculate scores for each career path
        scores = {}
        for career, requirements in self.career_paths.items():
            score = self._calculate_career_score(
                skills,
                education,
                interests,
                requirements
            )
            scores[career] = score
        
        # Sort careers by score
        sorted_careers = sorted(
            scores.items(),
            key=lambda x: x[1],
            reverse=True
        )
        
        # Prepare recommendations
        recommendations = []
        for career, score in sorted_careers:
            if score > 0:  # Only include careers with positive scores
                career_info = self.career_paths[career]
                recommendations.append({
                    'career': career,
                    'score': round(score * 100, 2),
                    'description': career_info['description'],
                    'growth_path': career_info['growth_path'],
                    'missing_skills': self._get_missing_skills(
                        skills,
                        career_info['required_skills'] + career_info['preferred_skills']
                    ),
                    'matching_skills': self._get_matching_skills(
                        skills,
                        career_info['required_skills'] + career_info['preferred_skills']
                    )
                })
        
        # Save recommendations to history
        self._save_to_history(recommendations, skills, education, interests)
        
        return recommendations

    def _calculate_career_score(self, skills, education, interests, requirements):
        """Calculate a score for a career path based on user profile."""
        weights = self.skill_weights
        
        # Calculate required skills score
        required_skills_score = self._calculate_skill_match(
            skills,
            requirements['required_skills']
        ) * weights['required_skills']
        
        # Calculate preferred skills score
        preferred_skills_score = self._calculate_skill_match(
            skills,
            requirements['preferred_skills']
        ) * weights['preferred_skills']
        
        # Calculate education score
        education_score = self._calculate_education_match(
            education,
            requirements['education']
        ) * weights['education']
        
        # Calculate interests score if interests are provided
        interests_score = 0
        if interests:
            interests_score = self._calculate_interests_match(
                interests,
                requirements['required_skills'] + requirements['preferred_skills']
            ) * weights['interests']
        
        # Combine scores
        total_score = (
            required_skills_score +
            preferred_skills_score +
            education_score +
            interests_score
        ) / sum(weights.values())
        
        return total_score

    def _calculate_skill_match(self, user_skills, required_skills):
        """Calculate how well user skills match required skills."""
        if not required_skills:
            return 0
        
        # Convert to sets for easier comparison
        user_skills_set = set(skill.lower() for skill in user_skills)
        required_skills_set = set(skill.lower() for skill in required_skills)
        
        # Calculate match
        matching_skills = user_skills_set.intersection(required_skills_set)
        return len(matching_skills) / len(required_skills_set)

    def _calculate_education_match(self, user_education, required_education):
        """Calculate how well user education matches required education."""
        if not required_education:
            return 0
        
        # Convert to sets for easier comparison
        user_education_set = set(edu.lower() for edu in user_education)
        required_education_set = set(edu.lower() for edu in required_education)
        
        # Calculate match
        matching_education = user_education_set.intersection(required_education_set)
        return len(matching_education) / len(required_education_set)

    def _calculate_interests_match(self, interests, skills):
        """Calculate how well user interests align with career skills."""
        if not interests or not skills:
            return 0
        
        # Convert to sets for easier comparison
        interests_set = set(interest.lower() for interest in interests)
        skills_set = set(skill.lower() for skill in skills)
        
        # Calculate match
        matching_interests = interests_set.intersection(skills_set)
        return len(matching_interests) / len(skills_set)

    def _get_missing_skills(self, user_skills, required_skills):
        """Get list of skills that user is missing."""
        user_skills_set = set(skill.lower() for skill in user_skills)
        required_skills_set = set(skill.lower() for skill in required_skills)
        
        return list(required_skills_set - user_skills_set)

    def _get_matching_skills(self, user_skills, required_skills):
        """Get list of skills that user has."""
        user_skills_set = set(skill.lower() for skill in user_skills)
        required_skills_set = set(skill.lower() for skill in required_skills)
        
        return list(user_skills_set.intersection(required_skills_set))

    def _save_to_history(self, recommendations, skills, education, interests):
        """Save recommendations to history."""
        import datetime
        
        timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f'recommendations_{timestamp}.json'
        filepath = os.path.join(self.recommendation_history_dir, filename)
        
        history_entry = {
            'timestamp': timestamp,
            'user_profile': {
                'skills': skills,
                'education': education,
                'interests': interests
            },
            'recommendations': recommendations
        }
        
        with open(filepath, 'w') as f:
            json.dump(history_entry, f, indent=2)

    def get_recommendation_history(self):
        """Retrieve recommendation history."""
        history = []
        for filename in os.listdir(self.recommendation_history_dir):
            if filename.endswith('.json'):
                with open(os.path.join(self.recommendation_history_dir, filename), 'r') as f:
                    history.append(json.load(f))
        
        return sorted(history, key=lambda x: x['timestamp'], reverse=True)

    def get_recommendations_from_resume(self, resume_data):
        """Generate career recommendations based on resume data."""
        try:
            recommendations = []
            
            # Extract key information from resume
            skills = resume_data.get('skills', [])
            experience = resume_data.get('experience', [])
            education = resume_data.get('education', [])
            
            # Analyze skills and experience to determine career paths
            career_paths = self._analyze_career_paths(skills, experience, education)
            
            # Generate recommendations for each career path
            for path in career_paths:
                recommendations.append({
                    'career_path': path['title'],
                    'description': path['description'],
                    'required_skills': path['required_skills'],
                    'missing_skills': path['missing_skills'],
                    'next_steps': path['next_steps'],
                    'salary_range': path['salary_range'],
                    'job_market': path['job_market']
                })
            
            return recommendations
        except Exception as e:
            raise Exception(f"Error generating resume recommendations: {str(e)}")

    def _analyze_career_paths(self, skills, experience, education):
        """Analyze skills and experience to determine potential career paths."""
        career_paths = []
        
        # Define career paths and their requirements
        paths = {
            'Software Engineer': {
                'required_skills': ['Python', 'JavaScript', 'SQL', 'Git', 'Algorithms'],
                'description': 'Design, develop, and maintain software applications and systems.',
                'salary_range': '$80,000 - $150,000',
                'job_market': 'High demand, competitive'
            },
            'Data Scientist': {
                'required_skills': ['Python', 'R', 'SQL', 'Machine Learning', 'Statistics'],
                'description': 'Analyze complex data sets to help guide business decisions.',
                'salary_range': '$90,000 - $160,000',
                'job_market': 'High demand, growing field'
            },
            'DevOps Engineer': {
                'required_skills': ['Linux', 'Docker', 'Kubernetes', 'CI/CD', 'Cloud Platforms'],
                'description': 'Manage and optimize software development and deployment processes.',
                'salary_range': '$85,000 - $155,000',
                'job_market': 'High demand, specialized'
            },
            'Product Manager': {
                'required_skills': ['Agile', 'Product Strategy', 'User Research', 'Data Analysis', 'Communication'],
                'description': 'Lead product development and strategy.',
                'salary_range': '$90,000 - $170,000',
                'job_market': 'High demand, leadership role'
            },
            'UX/UI Designer': {
                'required_skills': ['Figma', 'User Research', 'Wireframing', 'Prototyping', 'Design Systems'],
                'description': 'Create user-centered digital experiences.',
                'salary_range': '$75,000 - $140,000',
                'job_market': 'Growing demand, creative field'
            }
        }
        
        # Analyze each career path
        for title, requirements in paths.items():
            # Check required skills
            missing_skills = [skill for skill in requirements['required_skills'] if skill.lower() not in [s.lower() for s in skills]]
            
            # Determine next steps based on missing skills and experience
            next_steps = []
            if missing_skills:
                next_steps.append(f"Learn or improve: {', '.join(missing_skills[:3])}")
            
            # Add experience-based recommendations
            if not experience:
                next_steps.append("Gain relevant work experience through internships or projects")
            elif len(experience) < 2:
                next_steps.append("Build more professional experience in the field")
            
            # Add education-based recommendations
            if not education:
                next_steps.append("Consider pursuing relevant certifications or degrees")
            
            # Add general career development steps
            next_steps.extend([
                "Build a portfolio of projects",
                "Network with professionals in the field",
                "Stay updated with industry trends and technologies"
            ])
            
            # Calculate match percentage based on skills
            match_percentage = (len(requirements['required_skills']) - len(missing_skills)) / len(requirements['required_skills']) * 100
            
            # Only include paths with at least 20% match
            if match_percentage >= 20:
                career_paths.append({
                    'title': title,
                    'description': requirements['description'],
                    'required_skills': requirements['required_skills'],
                    'missing_skills': missing_skills,
                    'next_steps': next_steps,
                    'salary_range': requirements['salary_range'],
                    'job_market': requirements['job_market'],
                    'match_percentage': match_percentage
                })
        
        # Sort by match percentage
        career_paths.sort(key=lambda x: x['match_percentage'], reverse=True)
        
        return career_paths 