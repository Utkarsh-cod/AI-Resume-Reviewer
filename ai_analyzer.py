import os
import json
import re
import google.generativeai as genai

def get_ai_feedback(resume_text, job_title, job_description):
    """
    Sends the resume and job details to the Gemini API, cleans the response, 
    and returns a structured Python dictionary.
    
    Returns:
        A Python dictionary containing the feedback, or None if an error occurs.
    """
    try:
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            print("Error: GEMINI_API_KEY not found in environment variables.")
            return None
            
        genai.configure(api_key=api_key)

        model = genai.GenerativeModel('gemini-1.5-flash-latest')

        prompt_template = f"""
        You are an expert career coach and professional resume reviewer for a top tech company.
        Your task is to analyze a resume based on a specific job title and description.
        Provide a detailed, constructive, and encouraging review.

        IMPORTANT: Your final output must be a single, valid JSON object and nothing else. 
        Ensure your response starts with {{ and ends with }}. Do not include markdown like ```json.
        The JSON object must have the following exact structure:
        {{
            "overall_score": <an integer between 0 and 100>,
            "strengths": [<a list of 2-3 specific strengths as strings>],
            "areas_for_improvement": [<a list of 2-3 specific areas for improvement as strings>],
            "keyword_analysis": {{
                "found": [<a list of relevant keywords from the job description found in the resume>],
                "missing": [<a list of relevant keywords from the job description NOT found in the resume>]
            }},
            "suggested_rewrite": {{
                "original": "<a short, single bullet point from the resume that could be improved>",
                "improved": "<your rewritten, more impactful version of that bullet point>"
            }}
        }}

        Here is the information to analyze:
        ---
        JOB TITLE: {job_title}
        ---
        JOB DESCRIPTION: {job_description}
        ---
        RESUME TEXT: {resume_text}
        ---
        """
        
        response = model.generate_content(prompt_template)
        
        # --- !! ULTRA-ROBUST FIX APPLIED HERE !! ---
        # Find the JSON block even if the AI includes extra text or markdown.
        # This searches for the text between the first '{' and the last '}'
        match = re.search(r'\{.*\}', response.text, re.DOTALL)
        
        if match:
            json_string = match.group(0)
            feedback_dict = json.loads(json_string)
            return feedback_dict
        else:
            print("Error: No valid JSON object found in the AI response.")
            print("---AI Response---")
            print(response.text)
            print("-----------------")
            return None

    except json.JSONDecodeError:
        print("Error: Failed to decode JSON from AI response even after cleaning.")
        print("---AI Response---")
        print(response.text)
        print("-----------------")
        return None
    except Exception as e:
        print(f"An unexpected error occurred in AI analyzer: {e}")
        return None
    

