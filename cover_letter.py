from .utils.file_utils import read_file_content
from .utils.nlp_utils import NLPProcessor
import re
import random

class CoverLetterGenerator:
    def __init__(self):
        self.nlp_processor = NLPProcessor()
        
        # Templates for different sections
        self.templates = {
            'opening': [
                "I am writing to express my strong interest in the {position} position at {company}. With my background in {field} and experience in {skill}, I believe I would be a valuable addition to your team.",
                "I am excited to apply for the {position} role at {company}. My experience in {field} and expertise in {skill} align perfectly with the requirements of this position.",
                "As a {field} professional with extensive experience in {skill}, I am writing to express my interest in the {position} position at {company}."
            ],
            'body': [
                "Throughout my career, I have developed strong skills in {skill1} and {skill2}. In my previous role, I {achievement}. This experience has prepared me well for the challenges and opportunities at {company}.",
                "My background in {field} has equipped me with valuable expertise in {skill1} and {skill2}. I have successfully {achievement}, which demonstrates my ability to deliver results in this role.",
                "With {years} years of experience in {field}, I have honed my skills in {skill1} and {skill2}. I am particularly proud of {achievement}, which showcases my ability to {skill3}."
            ],
            'closing': [
                "I am excited about the opportunity to bring my skills and experience to {company}. I look forward to discussing how I can contribute to your team's success.",
                "I would welcome the chance to discuss how my background in {field} and skills in {skill} can benefit {company}. Thank you for considering my application.",
                "I am confident that my combination of skills and experience makes me an ideal candidate for this position. I look forward to the possibility of joining {company} and contributing to its continued success."
            ]
        }

    def generate(self, resume_path, job_description):
        """Generate a personalized cover letter based on resume and job description."""
        # Read and analyze both documents
        resume_content = read_file_content(resume_path)
        resume_analysis = self.nlp_processor.extract_skills(resume_content)
        job_skills = self.nlp_processor.extract_skills(job_description)
        
        # Extract company name and position from job description
        company = self._extract_company(job_description)
        position = self._extract_position(job_description)
        
        # Get matching skills
        matching_skills = set(resume_analysis).intersection(set(job_skills))
        if not matching_skills:
            matching_skills = set(resume_analysis)  # Fallback to resume skills
        
        # Get experience summary
        experience = self.nlp_processor.extract_experience(resume_content)
        achievement = self._extract_achievement(experience)
        
        # Generate cover letter sections
        opening = self._generate_opening(position, company, matching_skills)
        body = self._generate_body(matching_skills, achievement, company)
        closing = self._generate_closing(company, matching_skills)
        
        # Combine sections
        cover_letter = f"{opening}\n\n{body}\n\n{closing}"
        
        return {
            'cover_letter': cover_letter,
            'company': company,
            'position': position,
            'highlighted_skills': list(matching_skills)
        }

    def _extract_company(self, job_description):
        """Extract company name from job description."""
        # Simple pattern matching for common company indicators
        patterns = [
            r'at\s+([A-Z][A-Za-z\s]+)',
            r'with\s+([A-Z][A-Za-z\s]+)',
            r'([A-Z][A-Za-z\s]+)\s+is\s+hiring'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, job_description)
            if match:
                return match.group(1).strip()
        
        return "the company"  # Default if company name not found

    def _extract_position(self, job_description):
        """Extract job position from job description."""
        # Look for common position indicators
        patterns = [
            r'position:\s*([A-Za-z\s]+)',
            r'role:\s*([A-Za-z\s]+)',
            r'seeking\s+a\s+([A-Za-z\s]+)',
            r'looking\s+for\s+a\s+([A-Za-z\s]+)'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, job_description, re.IGNORECASE)
            if match:
                return match.group(1).strip()
        
        return "this position"  # Default if position not found

    def _extract_achievement(self, experience):
        """Extract a notable achievement from experience."""
        achievement_indicators = ['achieved', 'increased', 'improved', 'developed',
                                'implemented', 'created', 'led', 'managed']
        
        for sentence in experience:
            if any(indicator in sentence.lower() for indicator in achievement_indicators):
                return sentence
        
        return "delivered significant results"  # Default if no achievement found

    def _generate_opening(self, position, company, skills):
        """Generate opening paragraph."""
        template = random.choice(self.templates['opening'])
        field = list(skills)[0] if skills else "the field"
        skill = list(skills)[1] if len(skills) > 1 else field
        
        return template.format(
            position=position,
            company=company,
            field=field,
            skill=skill
        )

    def _generate_body(self, skills, achievement, company):
        """Generate body paragraph."""
        template = random.choice(self.templates['body'])
        skill_list = list(skills)
        
        return template.format(
            skill1=skill_list[0] if skill_list else "the required skills",
            skill2=skill_list[1] if len(skill_list) > 1 else "related areas",
            skill3=skill_list[2] if len(skill_list) > 2 else "excel in this role",
            achievement=achievement,
            company=company,
            years="several",
            field=skill_list[0] if skill_list else "this field"
        )

    def _generate_closing(self, company, skills):
        """Generate closing paragraph."""
        template = random.choice(self.templates['closing'])
        skill_list = list(skills)
        
        return template.format(
            company=company,
            field=skill_list[0] if skill_list else "this field",
            skill=skill_list[1] if len(skill_list) > 1 else "the required areas"
        )