from flask import Flask, request, jsonify
from pymongo import MongoClient
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neighbors import NearestNeighbors
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# MongoDB Connection Setup
client = MongoClient('mongodb://localhost:27017/')
db = client['linkedin_clone']
users_collection = db['users']

# Sample data for users with job preferences
sample_users = [
    {'id': 1, 'name': 'Rahul Kumar', 'profile': 'Software Engineer', 'job_preferences': 'Python Developer'},
    {'id': 2, 'name': 'Priya Verma', 'profile': 'Data Scientist', 'job_preferences': 'Machine Learning Engineer'},
    {'id': 3, 'name': 'Ananya Patel', 'profile': 'Web Developer', 'job_preferences': 'JavaScript Developer'},
    {'id': 4, 'name': 'Rohit Sharma', 'profile': 'UX/UI Designer', 'job_preferences': 'Product Designer'},
    {'id': 5, 'name': 'Aishwarya Gupta', 'profile': 'Marketing Specialist', 'job_preferences': 'Digital Marketing Manager'},
    {'id': 6, 'name': 'Arjun Singh', 'profile': 'Network Engineer', 'job_preferences': 'Cybersecurity Analyst'},
    {'id': 7, 'name': 'Neha Khanna', 'profile': 'Financial Analyst', 'job_preferences': 'Investment Analyst'},
    {'id': 8, 'name': 'Manish Joshi', 'profile': 'Civil Engineer', 'job_preferences': 'Structural Engineer'},
    {'id': 9, 'name': 'Deepak Singh', 'profile': 'Software Developer', 'job_preferences': 'Java Developer'},
    {'id': 10, 'name': 'Shreya Sharma', 'profile': 'Database Administrator', 'job_preferences': 'SQL Developer'},
    {'id': 11, 'name': 'Vivek Patel', 'profile': 'Frontend Developer', 'job_preferences': 'React Developer'},
    {'id': 12, 'name': 'Pooja Desai', 'profile': 'Backend Developer', 'job_preferences': 'Node.js Developer'},
    {'id': 13, 'name': 'Harish Gupta', 'profile': 'Mobile App Developer', 'job_preferences': 'iOS Developer'},
    {'id': 14, 'name': 'Sneha Jain', 'profile': 'UI/UX Designer', 'job_preferences': 'Graphic Designer'},
    {'id': 15, 'name': 'Rajat Verma', 'profile': 'Data Analyst', 'job_preferences': 'Business Intelligence Analyst'},
    {'id': 16, 'name': 'Simran Kapoor', 'profile': 'Sales Executive', 'job_preferences': 'Account Manager'},
    {'id': 17, 'name': 'Karan Khanna', 'profile': 'Human Resources Manager', 'job_preferences': 'Talent Acquisition Specialist'},
    {'id': 18, 'name': 'Meera Singh', 'profile': 'Content Writer', 'job_preferences': 'Copywriter'},
    {'id': 19, 'name': 'Alok Mishra', 'profile': 'Quality Assurance Engineer', 'job_preferences': 'Automation Tester'},
    {'id': 20, 'name': 'Anjali Yadav', 'profile': 'System Administrator', 'job_preferences': 'Network Administrator'},
    {'id': 21, 'name': 'Vikas Sharma', 'profile': 'Digital Marketing Executive', 'job_preferences': 'SEO Specialist'},
    {'id': 22, 'name': 'Preeti Das', 'profile': 'Product Manager', 'job_preferences': 'Product Owner'},
    {'id': 23, 'name': 'Rohini Kapoor', 'profile': 'Supply Chain Analyst', 'job_preferences': 'Logistics Coordinator'},
    {'id': 24, 'name': 'Amit Patel', 'profile': 'Electrical Engineer', 'job_preferences': 'Power Systems Engineer'},
    {'id': 25, 'name': 'Swati Singh', 'profile': 'Customer Support Representative', 'job_preferences': 'Technical Support Specialist'},
    {'id': 26, 'name': 'Rajesh Kumar', 'profile': 'Legal Consultant', 'job_preferences': 'Corporate Lawyer'},
    {'id': 27, 'name': 'Nisha Gupta', 'profile': 'Public Relations Manager','job_preferences': 'Media Relations Specialist'},
    {'id': 28, 'name': 'Amita Sharma', 'profile': 'Event Planner', 'job_preferences': 'Wedding Coordinator'},
    {'id': 29, 'name': 'Rajeev Verma', 'profile': 'Healthcare Consultant', 'job_preferences': 'Medical Researcher'},
    {'id': 30, 'name': 'Anushka Singh', 'profile': 'Environmental Engineer','job_preferences': 'Sustainability Specialist'},
    
    # Add more sample users as needed
]

# Insert sample users into MongoDB
for user in sample_users:
    users_collection.insert_one(user)

# Create TF-IDF vectorizer
tfidf_vectorizer = TfidfVectorizer(stop_words='english')
user_profiles = [user['profile'] + ' ' + user.get('job_preferences', '') for user in sample_users]
tfidf_matrix = tfidf_vectorizer.fit_transform(user_profiles)

# Train Nearest Neighbors model
knn_model = NearestNeighbors(n_neighbors=10, metric='cosine')
knn_model.fit(tfidf_matrix)

def get_top_matches(query_vector):
    distances, indices = knn_model.kneighbors(query_vector, n_neighbors=10)
    top_matches = [
        {
            'id': sample_users[index]['id'],
            'name': sample_users[index]['name'],
            'job_preferences': sample_users[index].get('job_preferences', ''),
            'distance': distances[0][i]
        }
        for i, index in enumerate(indices[0])
    ]
    return top_matches

@app.route('/')
def home():
    return "Welcome to the LinkedIn Clone API"

@app.route('/search', methods=['POST'])
def search_users():
    data = request.get_json()
    query = data['query']
    query_vector = tfidf_vectorizer.transform([query])

    top_matches = get_top_matches(query_vector)

    return jsonify({'results': top_matches})

if __name__ == '__main__':
    app.run(debug=True)
