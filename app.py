from flask import Flask, render_template, request
from googletrans import Translator
import os
from docx import Document  # To handle .docx files
from PyPDF2 import PdfReader  # To handle .pdf files

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = './uploads'
translator = Translator()

# Ensure the upload folder exists
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

# Sample responses for the chatbot
chatbot_responses = {
    "wear seatbelt": "Always wear your seatbelt while driving. It's not only a safety measure but also a legal requirement in most jurisdictions. Failing to wear a seatbelt can result in fines and increase the risk of injury in an accident.",
    
    "seatbelt": "Wearing a seatbelt reduces the risk of fatal injury by 45%. Remember, it's not just for your safety; it's the law in many places, and you could be fined for not wearing one.",
    
    "drink and drive": "Never drink and drive; it's incredibly dangerous and illegal. Driving under the influence can lead to severe penalties, including fines, license suspension, and imprisonment. Always have a designated driver.",
    
    "speed limit": "Observe the speed limits posted on the road. Speeding not only increases the likelihood of accidents but can also result in hefty fines and points on your driving record.",
    
    "pedestrian": "Always yield to pedestrians at crosswalks. In many regions, failing to do so can result in significant fines. Remember, pedestrians have the right of way!",
    
    "traffic lights": "Follow traffic light signals for safety. Running a red light can lead to serious accidents and legal consequences, including fines and points on your license.",
    
    "road signs": "Understand and follow all road signs. They provide critical information about the road conditions, rules, and safety measures. Ignoring them can lead to accidents and penalties.",
    
    "mobile phone": "Avoid using your mobile phone while driving. Texting or calling diverts your attention from the road and increases your chances of being involved in an accident. Many areas impose fines for distracted driving.",
    
    "weather conditions": "Adjust your driving according to weather conditions. In adverse weather, reduce your speed and increase your following distance to maintain control and safety.",
    
    "bike safety": "Always wear a helmet when riding a bike. It's crucial for your safety, and in many places, it's required by law. Ensure your bike is well-maintained to avoid accidents.",
    
    "lane change": "Signal your intentions when changing lanes. Proper signaling helps other drivers anticipate your moves and can prevent collisions.",
    
    "roundabouts": "Yield to traffic already in the roundabout. This is essential for maintaining flow and safety. Failure to yield can lead to accidents.",
    
    "driving under influence": "Never drive under the influence of drugs or alcohol. It's not just illegal; it endangers everyone on the road. Penalties can include heavy fines, jail time, and loss of driving privileges.",
    
    "fatigue": "Don't drive when you're fatigued; it impairs your reaction time and judgment. If you feel tired, take a break or switch drivers to ensure safety.",
    
    "children": "Watch out for children near schools and playgrounds. Be especially vigilant during school hours. Laws often impose stricter speed limits in these areas for their protection.",
    
    "motorcycles": "Always check for motorcycles before changing lanes. Motorcyclists are harder to see, and failing to check can lead to serious accidents.",
    
    "emergency vehicle": "Yield to emergency vehicles and pull over when you hear sirens. It's crucial to give them the right of way so they can respond to emergencies quickly.",
    
    "crosswalk": "Always stop for pedestrians at crosswalks. Not doing so can result in fines and more importantly, it endangers lives.",
    
    "seat adjustment": "Adjust your seat and mirrors before starting your trip. Proper positioning is vital for maintaining control and visibility while driving.",
    
    "vehicle maintenance": "Regularly check your vehicle's brakes and tires. Proper maintenance can prevent accidents and ensure your vehicle is roadworthy.",
    
    "road rage": "Stay calm and avoid engaging with aggressive drivers. If confronted, it's best to ignore them and focus on driving safely. Road rage can escalate quickly.",
    
    "traffic congestion": "Plan your routes to avoid traffic jams. Utilize traffic apps to find alternate routes to save time and reduce frustration.",
    
    "night driving": "Use headlights and reduce speed when driving at night. Visibility is limited, and driving too fast can lead to accidents.",
    
    "alcohol limit": "Know the legal blood alcohol concentration limit in your area. It varies by jurisdiction, and exceeding it can result in serious legal consequences.",
    
    "driving license": "Always carry your driving license while driving. It's a legal requirement, and not having it can lead to fines and other penalties.",
    
    "insurance": "Ensure your vehicle is insured at all times. Driving without insurance is illegal and can result in severe penalties, including fines and license suspension.",
    
    "school zone": "Reduce speed in school zones during pick-up and drop-off times. It's crucial for the safety of children, and there are usually stricter penalties for speeding in these areas.",
    
    "seat belt laws": "Know the seat belt laws in your area. Not wearing a seatbelt can lead to fines, and it significantly increases your risk of injury in an accident.",
    
    "front and rear lights": "Make sure your vehicle's lights are functioning properly. This is essential for visibility and safety, especially at night or in bad weather.",
    
    "tailgating": "Maintain a safe following distance from the vehicle ahead. Tailgating can lead to rear-end collisions, which can cause serious injuries.",
    
    "carpooling": "Consider carpooling to reduce the number of vehicles on the road. It not only eases traffic but is also better for the environment.",
    
    "road work": "Be cautious and obey signs when approaching road work. Failing to do so can lead to fines and put workers at risk.",
    
    "fog driving": "Use low beam headlights in foggy conditions. High beams can reflect off the fog and reduce visibility.",
    
    "snow and ice": "Use winter tires and drive slowly in snowy or icy conditions. Proper tires and reduced speed can help you maintain control.",
    
    "traffic signs": "Always heed traffic signs and signals. They are placed for your safety, and ignoring them can lead to accidents and penalties.",
    
    "one-way street": "Be aware of one-way streets and obey the direction. Driving the wrong way can lead to serious accidents.",
    
    "pedestrian crossing": "Stop for pedestrians at marked crossings. This is not just courteous; it's often a legal requirement.",
    
    "driving in rain": "Slow down and increase following distance in rain. Wet roads can be slippery, and stopping distances are longer.",
    
    "child safety seat": "Use appropriate child safety seats for young passengers. It's not only safer; it's the law in many places, and there are strict regulations regarding their use.",
    
    "bicycle lane": "Do not drive in designated bicycle lanes. This is not only illegal but can also endanger cyclists.",
    
    "right of way": "Understand the right-of-way rules at intersections. Knowing who goes first can prevent collisions and confusion.",
    
    "road conditions": "Be mindful of road conditions and adjust your speed accordingly. Poor conditions require slower speeds for safety.",
    
    "left turn": "Signal your intention when making a left turn. This allows other drivers to anticipate your actions and helps avoid accidents.",
    
    "right turn": "Check for pedestrians and cyclists before turning right. Be sure to yield to anyone crossing the street.",
    
    "merging": "Yield to traffic when merging onto highways. Proper merging is essential for maintaining safety on high-speed roads.",
    
    "highway driving": "Keep right except to pass on highways. This helps maintain smooth traffic flow and prevents accidents.",
    
    "signaling": "Always use turn signals when changing lanes. Signaling informs other drivers of your intentions and is a key part of safe driving.",
    
    "potholes": "Avoid potholes and report them to local authorities. They can damage your vehicle and pose serious safety risks.",
    
    "vehicle inspection": "Regularly inspect your vehicle for safety. Many jurisdictions require periodic inspections to ensure roadworthiness.",
    
    "headlights": "Use headlights in low visibility conditions. This is critical for your safety and the safety of others on the road.",
    
    "flooded roads": "Do not drive through flooded roadways. The water may be deeper than it appears, and you could become stranded or swept away.",
    
    "distracted driving": "Avoid all distractions while driving. This includes not only mobile devices but also adjusting controls or engaging in conversation.",
    
    "road safety education": "Educate yourself and others about road safety. Understanding the rules can help prevent accidents and save lives.",
    
    "angry drivers": "Do not engage with angry or aggressive drivers. If confronted, remain calm and avoid escalating the situation.",
    
    "motor vehicle laws": "Stay informed about local motor vehicle laws. Laws can change, and knowing them helps you avoid penalties.",
    
    "fines and penalties": "Understand the fines and penalties for traffic violations. Ignorance of the law is not an excuse, and penalties can be severe.",
    
    "insurance coverage": "Check that your insurance coverage is adequate for your needs. Underinsurance can leave you vulnerable in an accident.",
    
    "driving distractions": "Limit distractions like music and conversations. Keeping your focus on the road is essential for safe driving.",
    
    "speed cameras": "Be aware of speed cameras in your area. They are used to enforce speed limits and can result in fines.",
    
    "road etiquette": "Practice good road etiquette and respect other drivers. Being courteous can help reduce road rage incidents.",
    
    "signs of impairment": "Look out for signs of impairment in other drivers, such as erratic driving. If you suspect a driver is impaired, stay clear and report them.",
    
    "roadside assistance": "Have a roadside assistance plan in case of emergencies. This can provide peace of mind and help you in difficult situations.",
    
    "obstructed views": "Ensure your view is not obstructed when driving. This includes removing any objects from your dashboard and ensuring your mirrors are adjusted.",
    
    "backup cameras": "Use backup cameras and mirrors to avoid accidents when reversing. Always check your surroundings before backing up.",
    
    "oncoming traffic": "Be cautious of oncoming traffic when turning left. Ensure the lane is clear before making your turn.",
    
    "tailgating penalties": "Know the penalties for tailgating in your area. Tailgating can lead to accidents and fines.",
    
    "parking rules": "Follow parking rules to avoid fines. Illegal parking can also cause congestion and block emergency vehicles.",
    
    "vehicle recalls": "Stay informed about vehicle recalls for safety. Manufacturers will issue recalls to fix potentially dangerous defects.",
    
    "road signs meanings": "Learn the meanings of different road signs. Understanding these can help you navigate safely and legally.",
    
    "lane discipline": "Maintain lane discipline and avoid sudden lane changes. This helps keep traffic flowing smoothly and prevents accidents.",
    
    "curvy roads": "Slow down when driving on curvy roads. Sharp turns can be hazardous, especially if you're going too fast.",
    
    "accident reporting": "Know how to report an accident properly. This usually involves calling local authorities and exchanging information with other parties.",
    
    "emergency contacts": "Keep emergency contacts handy in your vehicle. This can be crucial in case of an accident or breakdown.",
    
    "rural driving": "Be extra cautious when driving in rural areas. Wildlife and unpaved roads can present unexpected hazards.",
    
    "interstate driving": "Understand the rules for interstate driving. Different states may have varying laws regarding speed limits and driving practices.",
    
    "first aid kit": "Carry a first aid kit in your vehicle. This is essential for treating minor injuries in case of an accident.",
    
    "traffic light sequences": "Know the sequence of traffic light changes. This helps you anticipate when to stop or go, reducing the likelihood of accidents.",
    
    "public transport": "Consider using public transport to reduce road congestion. It's often a safer and more efficient way to travel.",
    
    "road markings": "Understand the meaning of road markings. These markings provide critical information about lane usage and safety.",
    
    "blind spots": "Check your blind spots before changing lanes. Blind spots can hide vehicles that may be in your path.",
    
    "four-way stops": "Know the rules for four-way stops. The first vehicle to arrive generally has the right of way, but always be cautious.",
    
    "rear-end collisions": "Maintain a safe distance to avoid rear-end collisions. Tailgating significantly increases the risk of these types of accidents.",
    
    "car theft prevention": "Take precautions to prevent car theft. Lock your doors, park in well-lit areas, and avoid leaving valuables in sight.",
    
    "fuel efficiency": "Drive efficiently to save fuel. Avoid aggressive driving and excessive idling to improve fuel economy.",
    
    "vehicle weight limits": "Be aware of vehicle weight limits on roads. Overloading can lead to handling issues and increased wear on your vehicle.",
    
    "distracted walking": "Stay alert and avoid distractions while walking. Pay attention to your surroundings, especially near traffic.",
    
    "bicycle safety tips": "Always wear a helmet and follow traffic rules when cycling. This includes obeying signals and riding in designated lanes.",
    
    "defensive driving": "Practice defensive driving to anticipate potential hazards. This mindset helps you react safely to unexpected situations.",
    
    "road trip safety": "Plan your route and take breaks on long road trips. Fatigue is a serious risk; regular stops help maintain alertness.",
    
    "head-on collisions": "Avoid head-on collisions by staying in your lane. This is crucial for your safety and the safety of others.",
    
    "vehicle stability": "Ensure your vehicle is stable and well-maintained. Regular maintenance can prevent mechanical failures that lead to accidents.",
    
    "traffic enforcement": "Be aware of traffic enforcement and obey the rules. Enforcement helps keep roads safe for everyone.",
    
    "safe following distance": "Maintain a safe following distance, especially in poor weather. This allows for adequate reaction time.",
    
    "car seat installation": "Install car seats according to safety guidelines. Proper installation is essential for child safety.",
    
    "urban driving": "Be cautious of pedestrians and cyclists in urban areas. Urban environments have unique challenges and risks.",
    
    "non-motorized vehicles": "Respect the rights of non-motorized vehicles on the road. This includes bicycles, scooters, and pedestrians.",
    
    "road safety apps": "Use road safety apps for real-time traffic updates. These can help you avoid delays and stay informed.",
    
    "road safety campaigns": "Participate in local road safety campaigns. Engaging with community efforts can help spread awareness and promote safe practices.",
    
    "lane splitting": "Motorcyclists should be cautious when lane splitting. While legal in some areas, it can be dangerous if not done carefully.",
    
    "distracted driving laws": "Many areas have strict laws against distracted driving. Know the regulations in your region to avoid fines.",
    
    "emergency preparedness": "Be prepared for emergencies by keeping supplies in your vehicle. This can include water, snacks, and a flashlight.",
    
    "insurance penalties": "Driving without insurance can lead to severe penalties, including fines and potential legal action. Always ensure you are covered.",
    
    "car maintenance tips": "Regularly check your tires, brakes, and lights to ensure your vehicle is safe for the road. Maintenance can prevent accidents.",
    
    "safety training": "Consider taking a defensive driving course to improve your skills. Training can make you a more competent and safer driver.",
    
    "accident investigation": "If you are involved in an accident, remain calm and gather information. Document everything for insurance purposes.",
    
    "road trip planning": "When planning a road trip, check weather conditions and road closures. Being informed helps avoid surprises.",
    
    "gas station safety": "Be cautious when refueling your vehicle. Turn off your engine and avoid using your phone to reduce fire risks.",
    
    "motorcycle helmet laws": "Wearing a helmet while riding a motorcycle is mandatory in many areas. Always comply with local laws for safety.",
    
    "fatigue signs": "Know the signs of fatigue while driving, such as yawning and difficulty concentrating. If you notice these, pull over to rest.",
    
    "road safety statistics": "Stay informed about road safety statistics in your area. Understanding risks can motivate safer driving habits.",
    
    "driving while tired": "Driving while tired is just as dangerous as driving under the influence. Prioritize rest before getting behind the wheel.",
    
    "motor vehicle safety": "Motor vehicle safety encompasses a range of practices, including wearing seatbelts and ensuring vehicles are in good condition.",
    
    "traffic accident prevention": "Traffic accidents can often be prevented by following road rules and practicing safe driving habits. Stay aware and cautious.",
    
    "bike lane respect": "Respect bike lanes and give cyclists adequate space. This is vital for their safety and your own.",
    
    "sign language": "Learn basic sign language for communication in emergencies. This can be useful if you encounter someone in distress.",
    
    "pedestrian awareness": "Always be aware of pedestrians, especially in urban areas. They have the right of way, and being cautious is crucial.",
    
    "deer crossing": "Watch for deer crossing signs, especially in rural areas. Be alert at dawn and dusk when deer are most active.",
    
    "seatbelt reminders": "Some vehicles are equipped with seatbelt reminders. Pay attention to these alerts for your safety.",
    
    "road hazard reporting": "Report road hazards to local authorities to help maintain road safety for everyone.",
    
    "winter driving tips": "Prepare your vehicle for winter by checking antifreeze levels and using winter tires. Safe driving in winter requires extra caution.",
    
    "emergency vehicle rules": "Know the rules regarding emergency vehicles in your area. Always yield to them to help keep everyone safe.",
    
    "parking safety": "Be mindful of your surroundings when parking. Check for pedestrians and other vehicles before exiting your car.",
    
    "railroad crossing": "Always stop at railroad crossings when signals are active. Trains can approach quickly, and safety is paramount.",
    
    "commercial vehicle laws": "Be aware of special laws governing commercial vehicles, including weight restrictions and driver qualifications.",
    
    "road closure awareness": "Stay updated on road closures and detours in your area. Traffic apps can provide real-time information.",
    
    "fueling safety": "When fueling your vehicle, do not smoke or use your phone. These actions can increase the risk of fire.",
    
    "night visibility": "Improve night visibility by ensuring your headlights are clean and properly aimed. This can make a significant difference in safety.",
    
    "safety vests": "When working near traffic, wearing a safety vest can increase visibility. This is crucial for roadside workers' safety.",
    
    "emergency kit contents": "An emergency kit should include items like a flashlight, first aid supplies, and basic tools. Be prepared for unexpected situations.",
    
    "child passenger laws": "Familiarize yourself with child passenger safety laws in your area. These laws vary and are designed to protect children.",
    
    "driving simulation": "Consider using driving simulation apps for practice. These can help improve your skills in a controlled environment.",
    
    "road safety volunteering": "Volunteering for road safety organizations can help spread awareness and promote safer practices in your community.",
    
    "crossing guard": "Respect crossing guards and their directions. They are there to ensure the safety of pedestrians, especially children.",
    
    "bicycle registration": "Registering your bicycle can help recover it if stolen. This adds a layer of safety for cyclists.",
    
    "scooter safety": "If riding a scooter, follow the same rules as cyclists. Wear a helmet and obey traffic signals for safety.",
    
    "infrastructure improvement": "Advocate for infrastructure improvements in your community to enhance road safety. This can include better lighting and signage.",
    
    "traffic court": "If you receive a traffic citation, you may have the option to contest it in traffic court. Understand your rights and the process involved.",
    
    "road safety workshops": "Participate in road safety workshops to learn more about safe driving practices. These can provide valuable knowledge and skills.",
    
    "emergency contact numbers": "Keep emergency contact numbers easily accessible in your vehicle. This can be vital in a crisis.",
    
    "roadside safety tips": "If you break down on the road, stay with your vehicle and call for help. This is generally the safest option.",
    
    "vehicle technology": "Stay informed about new vehicle technologies that enhance safety, such as automatic braking and lane departure warnings.",
    
    "road safety policies": "Support local policies that promote road safety, including speed limits and seatbelt laws. Advocate for the protection of all road users.",
    
    "youth driving programs": "Encourage young drivers to participate in safe driving programs. Education is key to reducing accidents among inexperienced drivers.",
    
    "legal responsibilities": "Understand your legal responsibilities as a driver, including maintaining insurance and obeying traffic laws. Ignorance is not an excuse.",
    
    "awareness campaigns": "Support awareness campaigns that focus on road safety. These initiatives can make a difference in preventing accidents.",
}



def extract_text_from_docx(file_path):
    doc = Document(file_path)
    return "\n".join([paragraph.text for paragraph in doc.paragraphs])

def extract_text_from_pdf(file_path):
    text = ""
    try:
        with open(file_path, "rb") as file:
            reader = PdfReader(file)
            for page in reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text
    except Exception as e:
        print(f"Error reading PDF file: {e}")
    return text if text else None  # Return None if text is empty

@app.route("/", methods=["GET", "POST"])
def index():
    translation = None
    chatbot_response = None

    if request.method == "POST":
        text = request.form.get('text', '')
        language = request.form.get('language', 'en')

        # Handle file upload
        if 'file' in request.files and request.files['file'].filename != '':
            file = request.files['file']
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(file_path)

            # Determine file type and extract text
            if file.filename.endswith('.txt'):
                with open(file_path, 'r', encoding='utf-8') as f:
                    text = f.read()
            elif file.filename.endswith('.docx'):
                text = extract_text_from_docx(file_path)
            elif file.filename.endswith('.pdf'):
                text = extract_text_from_pdf(file_path)
            else:
                return "Unsupported file type", 400

            # Check if text extraction was successful
            if not text:
                return "Unable to extract text from file.", 400

        # Translate if text is available
        if text:
            translation = translator.translate(text, dest=language).text

        # Handle chatbot response
        user_message = request.form.get('chat_message', '').lower()
        if user_message:
            chatbot_response = get_chatbot_response(user_message)

    return render_template("index.html", translation=translation, chatbot_response=chatbot_response)

def get_chatbot_response(message):
    for key in chatbot_responses:
        if key in message:
            return chatbot_responses[key]
    return "I'm sorry, I don't understand that."



if __name__ == "__main__":
    app.run(debug=True)
