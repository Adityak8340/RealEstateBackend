from groq import Groq
from config import GROQ_API_KEY

if GROQ_API_KEY is None:
    raise ValueError("GROQ_API_KEY is not set in the environment variables")
groq_client = Groq(api_key=GROQ_API_KEY)

def generate_analysis(main_project_name, main_project_aqi, projects):
    project_details = "\n".join([
        f"Name: {project['name']}\nDistance: {project['distance']} m\nCategories: {project['categories']}\n"
        f"Address: {project['address']}\nPostcode: {project['postcode']}\nCountry: {project['country']}\n"
        f"Developer Reputation: {project['developer_reputation']}\nAir Quality Index (AQI): {project.get('aqi', 'Unknown')}\n"
        f"Nearby Facilities:\n    " + "\n    ".join([f"{facility.get('name', 'Unknown')} ({facility.get('distance', 'Unknown')} m away)" for facility in project.get('facilities', [])])
        for project in projects
    ])

    text_content = f"Main Project Name: {main_project_name}\nAir Quality Index (AQI): {main_project_aqi}\n\nCompetitive Projects:\n{project_details}"
    user_query = "Compare the main project with the competitive projects and determine which is the best. Provide reasoning and grades for each project."

    return generate_groq_response(user_query, text_content)

def generate_groq_response(user_prompt, text_content):
    try:
        system_prompt = (
            "You help with Real Estate Project Analysis. Given a main project and its competitors, you need to analyze the competitive projects. "
            "You also need to provide information about the air quality and nearby facilities. "
            "Make logical reasoning for comparing projects, and tell which one will be the best project with grades for each project. "
        )

        chat_completion = groq_client.chat.completions.create(
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Document Text: {text_content}\n\nUser Query: {user_prompt}"}
            ],
            model="llama3-8b-8192",
        )

        return chat_completion.choices[0].message.content.strip()
    except Exception as e:
        return f"An error occurred: {str(e)}"