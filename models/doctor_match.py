import faiss
import numpy as np
from models.embedding import embedding_model

doctor_specialties = [
    "Family Medicine",
    "Internal Medicine",
    "Dentist",
    "Social Worker",
    "Pediatrics",
    "Nurse Anesthetist, Certified Registered",
    "Chiropractor",
    "Emergency Medicine",
    "Psychologist",
    "Anesthesiology",
    "Obstetrics & Gynecology",
    "Radiology",
    "Physical Therapist",
    "Optometrist",
    "Psychiatrist"
]

doctor_specialties += [
    "Counselor",
    "Orthopaedic Surgery",
    "Surgery",
    "Ophthalmology",
    "Pharmacist",
    "Cardiovascular Disease",
    "Podiatrist",
    "Pathologist",
    "Neurologist",
    "General Practice",
    "Registered Nurse",
    "Physical Medicine & Rehabilitation",
    "Gastroenterology",
    "Urology",
    "Dermatology",
    "Otolaryngology"
]

doctor_specialties += [
    "Occupational Therapist",
    "Behavior Technician",
    "Pulmonary Disease",
    "Specialist/Technologist, Athletic Trainer",
    "Dietitian",
    "Internal Medicine, Hematology & Oncology",
    "Internal Medicine, Nephrology",
    "Audiologist",
    "Geriatric Medicine",
    "Allergy & Immunology",
    "Infectious Disease",
    "Surgery, Vascular Surgery",
    "Thoracic Surgery (Cardiothoracic Vascular Surgery)",
    "Neurological Surgery",
    "Critical Care Medicine"
]

doctor_specialties += [
    "Endocrinology, Diabetes & Metabolism",
    "Midwife",
    "Rheumatology",
    "Plastic Surgery",
    "Hospitalist",
    #"Pain Medicine",
    "Medical Oncology",
    "Nurse Practitioner, Women’s Health",
    "Interventional Cardiology",
    "Licensed Practical Nurse",
    "Neuromusculoskeletal Medicine & OMM",
    "Nurse Practitioner, Psych/Mental Health",
    "Case Manager/Care Coordinator",
    "Clinical Neuropsychologist",
    "Colon & Rectal Surgery"
]

doctor_specialties += [
    "Oral & Maxillofacial Surgery",
    "Sports Medicine",
    "Behavior Analyst",
    "Marriage & Family Therapist",
    "Surgery, Surgery of the Hand",
    "Clinical Cardiac Electrophysiology",
    "Addiction Medicine",
    "Technician, Personal Care Attendant",
    "Medical Genetics",
    "Optician",
    "Nuclear Medicine",
    "Massage Therapist",
    "Day Training/Habilitation Specialist",
    "Preventive Medicine, Occupational Medicine",
    "Hematology"
]

doctor_specialties += [
    "Nurse Practitioner, Neonatal",
    "Nurse Practitioner, Acute Care",
    "Surgery, Plastic and Reconstructive Surgery",
    "Nurse Practitioner, Primary Care",
    "Home Health Aide",
    "Family Medicine, Adult Medicine",
    "Occupational Therapist, Hand",
    "Preventive Medicine, Preventive Medicine/Occupational Environmental Medicine",
    "Adolescent Medicine",
    "Perfusionist",
    "Peer Specialist",
    "Community Health Worker",
    "Internal Medicine, Sleep Medicine",
    "Hospice and Palliative Medicine",
    "Surgery, Trauma Surgery",
    "Preventive Medicine, Public Health & General Preventive Medicine"
]

doctor_specialties += [
    "Surgery, Pediatric Surgery",
    "Legal Medicine",
    "Surgery, Surgical Critical Care",
    "Orthotist",
    "Acupuncturist",
    "Military Health Care Provider",
    "Psychiatry & Neurology, Sleep Medicine",
    "Kinesiotherapist",
    "Recreation Therapist",
    "Rehabilitation Practitioner",
    "Nurse Practitioner, Neonatal, Critical Care",
    "Preventive Medicine, Undersea and Hyperbaric Medicine",
    "Preventive Medicine, Aerospace Medicine",
    "Surgery, Surgical Oncology",
    "Prosthetic/Orthotic Supplier"
]

doctor_specialties += [
    "Clinical Nurse Specialist, Psych/Mental Health, Child & Adolescent",
    "Physical Medicine & Rehabilitation, Pediatric Rehabilitation Medicine",
    "Music Therapist",
    "Prosthetist",
    "Nurse Practitioner, Critical Care Medicine",
    "Adult Congenital Heart Disease",
    "Physical Medicine & Rehabilitation, Neuromuscular Medicine",
    "Clinical Nurse Specialist, Psych/Mental Health",
    "Advanced Heart Failure and Transplant Cardiology",
    "Durable Medical Equipment & Medical Supplies",
    "Clinical Nurse Specialist, Oncology",
    "Naturopath",
    "Orthotic Fitter",
    "Technician, Health Information",
    "Doula"
]

doctor_specialties += [
    "Internal Medicine, Transplant Hepatology",
    "Cardiology",
    "Psychiatry & Neurology, Behavioral Neurology & Neuropsychiatry",
    "Specialist/Technologist, Rehabilitation, Blind",
    "Technician/Technologist, Ocularist",
    "Nurse Practitioner, Occupational Health",
    "Clinical Nurse Specialist, Adult Health",
    "Electrodiagnostic Medicine",
    "Anesthesiologist Assistant",
    "Nursing Care",
    "Clinical Nurse Specialist, Neuroscience",
    "Clinical Nurse Specialist",
    "Transplant Surgery",
    "Occupational Therapist, Neurorehabilitation",
    "Preventive Medicine, Clinical Informatics Specialist"
]

doctor_specialties += [
    "Reflexologist",
    "Spec/Tech, Cardiovascular",
    "Family Medicine, Bariatric Medicine",
    "Psychiatry & Neurology, Neurocritical Care",
    "Clinical Nurse Specialist, Psych/Mental Health, Community",
    "Respiratory Therapist, Certified",
    "Clinical Nurse Specialist, Medical-Surgical",
    "Specialist/Technologist, Other, Electroneurodiagnostic",
    "Independent Medical Examiner",
    "Clinical Nurse Specialist, Acute Care",
    "Home Health",
    "Respiratory Therapist, Registered"
]

doctor_descriptions = [
    "Provides comprehensive and continuing healthcare to individuals and families across all ages, genders, and diseases.",
    "Focuses on the prevention, diagnosis, and treatment of adult diseases, managing both common and complex illnesses.",
    "Diagnoses, prevents, and treats problems related to teeth, oral cavity, and related structures of the head and neck.",
    "Supports patients and families by providing psychosocial counseling, connecting them with resources, and helping navigate social challenges.",
    "Specializes in the medical care of infants, children, and adolescents, monitoring growth and developmental milestones.",
    "Provides anesthesia and related care before, during, and after surgical, therapeutic, diagnostic, and obstetrical procedures.",
    "Focuses on diagnosing and treating musculoskeletal disorders, especially those involving the spine, through manual adjustment or manipulation.",
    "Delivers immediate evaluation, diagnosis, and care for patients with acute illnesses or injuries.",
    "Assesses, diagnoses, and treats mental, emotional, and behavioral disorders through therapy and counseling.",
    "Manages pain and patient stability before, during, and after surgery, overseeing anesthesia and vital functions.",
    "Provides care for women’s reproductive health, including pregnancy, childbirth, and disorders of the reproductive system.",
    "Utilizes imaging techniques (X-ray, MRI, CT, etc.) to diagnose and sometimes treat diseases within the body.",
    "Helps patients improve mobility, reduce pain, and restore function through exercise, manual therapy, and other interventions.",
    "Examines, diagnoses, and manages eye conditions; prescribes corrective lenses and detects eye diseases.",
    "A medical doctor who diagnoses, treats, and helps prevent mental, emotional, and behavioral disorders, often with medication."
]

doctor_descriptions += [
    "Provides guidance and support to help people manage emotional, mental, and behavioral challenges.",
    "Specializes in diagnosing and treating musculoskeletal conditions, including bones, joints, ligaments, and muscles.",
    "Performs operative procedures to treat diseases, injuries, or deformities by manual or instrumental means.",
    "Specializes in eye and vision care, including surgical and medical treatments for eye disorders.",
    "Prepares and dispenses medications; offers expertise in safe medication use and therapy.",
    "Diagnoses and treats conditions related to the heart and blood vessels in adult patients.",
    "Addresses issues involving the foot, ankle, and related structures of the leg, including both medical and surgical treatments.",
    "Investigates the causes and effects of diseases by examining tissues, organs, and bodily fluids.",
    "Specializes in diagnosing and treating disorders of the nervous system, including the brain and spinal cord.",
    "Provides primary care services, often covering a wide range of common health issues in all age groups.",
    "Delivers patient care, educates patients about health conditions, and provides advice and emotional support.",
    "Aims to enhance and restore functional ability and quality of life to those with physical impairments or disabilities.",
    "Focuses on the digestive system and its disorders, including the esophagus, stomach, intestines, and liver.",
    "Deals with the urinary tract in both sexes and the male reproductive system, diagnosing and treating related disorders.",
    "Diagnoses and treats skin, hair, and nail disorders, and provides advice on skin care and appearance.",
    "Also known as ENT (Ear, Nose, and Throat), deals with conditions of the head and neck."
]

doctor_descriptions += [
    "Helps people develop, recover, or maintain meaningful activities (occupations) despite physical or cognitive limitations.",
    "Works under the supervision of a behavior analyst to provide direct behavioral interventions, often for individuals with autism or related disorders.",
    "Specializes in lung and respiratory disorders, including asthma, COPD, and other breathing problems.",
    "Prevents, diagnoses, and treats muscle and bone injuries and illnesses in athletes and other active people.",
    "Assesses nutritional needs, develops dietary plans, and educates patients on healthy eating behaviors.",
    "Focuses on blood disorders (hematology) and cancer (oncology) in adults.",
    "Diagnoses and manages kidney function and kidney-related diseases.",
    "Specializes in identifying, diagnosing, and treating hearing and balance disorders.",
    "Provides care and treatment tailored to the complex needs of older adults.",
    "Diagnoses and treats allergic conditions and immune system disorders, such as asthma and autoimmune diseases.",
    "Deals with the diagnosis, treatment, and prevention of infectious diseases caused by bacteria, viruses, and more.",
    "Specializes in the treatment of blood vessel (arteries and veins) disorders, often through surgical procedures.",
    "Manages surgical treatment of organs inside the thorax (chest), including the heart and lungs.",
    "Performs surgical procedures on the brain, spine, and other parts of the nervous system.",
    "Focuses on patients with life-threatening conditions, typically working in intensive care units."
]

doctor_descriptions += [
    "Treats hormone imbalances, metabolic disorders, and conditions like diabetes and thyroid disease.",
    "Provides care and support during pregnancy, childbirth, and the postpartum period, often with a holistic approach.",
    "Deals with arthritis and other rheumatic diseases affecting joints, muscles, and bones.",
    "Involves repairing or reconstructing physical defects and performing cosmetic procedures.",
    "Specializes in the general medical care of hospitalized patients, coordinating overall treatment plans.",
    #"Manages acute, chronic, and cancer-related pain using a variety of medical and therapeutic approaches.",
    "Specializes in cancer treatment using chemotherapy, targeted therapy, and other medications.",
    "Provides advanced nursing care and health services specifically for women, focusing on reproductive, obstetric, and gynecological health.",
    "Uses minimally invasive, catheter-based techniques to treat cardiovascular diseases (e.g., stent placement).",
    "Provides basic nursing care under the direction of registered nurses and doctors.",
    "Uses osteopathic manipulative medicine techniques to treat musculoskeletal disorders.",
    "Focuses on mental health assessment, diagnosis, and treatment, including prescribing psychiatric medications.",
    "Oversees and organizes patient care plans, ensuring smooth transitions between services and effective resource usage.",
    "Assesses cognitive function and treats the psychological effects of brain injury or neurological conditions.",
    "Specializes in the surgical treatment of diseases and disorders of the colon, rectum, and anus."
]


doctor_descriptions += [
    "Deals with surgical procedures involving the face, mouth, and jaw, often including tooth extractions and reconstructive surgery.",
    "Addresses health and performance of athletes, focusing on prevention and treatment of sports-related injuries.",
    "Studies and applies principles of behavior to help modify and improve socially significant behaviors.",
    "Provides counseling focused on interpersonal relationships and family dynamics.",
    "Specializes in diagnosing and treating conditions affecting the hand, wrist, and forearm, often surgically.",
    "Manages heart rhythm disorders using devices like pacemakers and defibrillators.",
    "Focuses on the prevention, evaluation, diagnosis, and treatment of substance use disorders.",
    "Assists patients with daily living tasks, monitoring their well-being under the guidance of healthcare professionals.",
    "Diagnoses and manages hereditary disorders, providing genetic testing and counseling for patients and families.",
    "Designs, verifies, and fits eyeglass lenses and frames, following prescriptions from optometrists or ophthalmologists.",
    "Uses small amounts of radioactive materials for diagnostic imaging and treatment of various diseases.",
    "Manipulates soft tissues of the body to relieve pain, reduce stress, and promote relaxation.",
    "Provides services and supports to individuals with disabilities, enhancing their daily living skills and independence.",
    "Focuses on workplace health, preventing injury and illness in the occupational environment.",
    "Diagnoses and treats blood-related disorders, including anemia, clotting disorders, and hematologic malignancies."
]

doctor_descriptions += [
    "Provides advanced care to newborns, particularly those who are premature or critically ill.",
    "Manages and cares for patients with acute, complex conditions, often in hospital settings.",
    "Restores function and form, performing reconstructive procedures for trauma, birth defects, or cosmetic enhancement.",
    "Delivers comprehensive healthcare for common medical conditions, focusing on health promotion and disease prevention.",
    "Assists individuals in their homes with daily living tasks, monitoring basic health needs.",
    "Concentrates on the general medical care of adult patients within the scope of family practice.",
    "Specializes in rehabilitation of the hand and upper limb to improve function and independence.",
    "Combines preventive care with workplace and environmental health, ensuring safety and hazard reduction.",
    "Addresses the physical, emotional, and social health of adolescents and young adults.",
    "Operates the heart-lung machine and other equipment during cardiac surgery to maintain blood flow and oxygenation.",
    "Provides support based on personal experience with mental health or substance use recovery, guiding and mentoring peers.",
    "Works in community settings to facilitate access to healthcare services and improve health outcomes through education and outreach.",
    "Diagnoses and treats sleep-related disorders such as sleep apnea and insomnia.",
    "Focuses on symptom relief, comfort, and end-of-life care for patients with serious illnesses.",
    "Specializes in the surgical treatment of acute injuries, often in emergency and critical care settings.",
    "Addresses community health, disease prevention, and health promotion strategies."
]


doctor_descriptions += [
    "Provides surgical care for infants, children, and adolescents, treating congenital and acquired conditions.",
    "Bridges the gap between medicine and law, advising on legal aspects of medical practice and forensic evaluations.",
    "Manages critically ill surgical patients, often in intensive care units following major operations or severe trauma.",
    "Designs and fits orthopedic braces and other devices to support limbs and the spine.",
    "Uses thin needles inserted into specific body points to alleviate pain and treat various physical, mental, and emotional conditions.",
    "Delivers medical services within military settings, addressing both combat and non-combat healthcare needs.",
    "Combines psychiatric and neurologic expertise to manage complex sleep disorders.",
    "Uses exercise and movement science to rehabilitate individuals with musculoskeletal, neuromuscular, or cardiopulmonary conditions.",
    "Uses recreational activities to enhance or restore function, promote independence, and improve quality of life.",
    "Provides treatments and strategies to improve or restore physical function after injury or illness.",
    "Delivers advanced care to critically ill newborns in neonatal intensive care units.",
    "Deals with the medical aspects of diving and hyperbaric chamber treatments for certain conditions.",
    "Ensures the health, safety, and performance of individuals involved in air and space travel.",
    "Specializes in the surgical management of cancer, often working in tandem with medical and radiation oncologists.",
    "Provides prostheses (artificial limbs) and orthotic devices for patients with limb loss or musculoskeletal conditions."
]



doctor_descriptions += [
    "Offers advanced mental health nursing care specifically for children and adolescents.",
    "Focuses on rehabilitation for children with physical and developmental disabilities.",
    "Uses music-based interventions to address physical, emotional, cognitive, and social needs of individuals.",
    "Designs and fits artificial limbs and other prosthetic devices for patients with missing or impaired body parts.",
    "Manages critically ill patients, stabilizing acute conditions and coordinating complex care.",
    "Focuses on adults living with congenital heart defects, offering specialized monitoring and treatments.",
    "Treats disorders affecting nerve and muscle function, aiming to improve mobility and quality of life.",
    "Provides advanced psychiatric nursing care, consultation, and treatment planning for mental health issues.",
    "Manages complex heart failure patients, including those needing or who have undergone heart transplants.",
    "Supplies products like wheelchairs, walkers, and other equipment essential for patient care at home.",
    "Offers advanced nursing expertise in cancer care, from diagnosis through treatment and survivorship.",
    "Emphasizes holistic healing and natural remedies, focusing on the body’s self-healing processes.",
    "Fits and adjusts pre-fabricated orthotic devices to support and align limbs or the spine.",
    "Manages, organizes, and secures healthcare data and patient records.",
    "Provides physical, emotional, and informational support to a mother before, during, and shortly after childbirth."
]


doctor_descriptions += [
    "Focuses on advanced liver disease and the management of liver transplant patients.",
    "A branch of medicine focused on diseases and disorders of the heart and circulatory system.",
    "Addresses cognitive, emotional, and behavioral symptoms related to brain disorders.",
    "Assists visually impaired or blind individuals to achieve greater independence through rehabilitation training.",
    "Specializes in fitting and fabricating ocular prostheses (artificial eyes).",
    "Provides advanced healthcare services in workplace settings, focusing on injury prevention and employee health.",
    "Offers expert nursing care for adults with a range of health conditions, providing consultation and patient management.",
    "Uses electrical recordings (e.g., EMG, nerve conduction studies) to diagnose neuromuscular disorders.",
    "Works under the direction of an anesthesiologist to develop and implement anesthesia care plans.",
    "General provision of nursing services in diverse settings, focusing on patient safety and comfort.",
    "Provides advanced care for patients with neurological conditions, including brain and spinal disorders.",
    "A master’s or doctoral-prepared nurse who provides expert clinical practice, research, education, and consultation in a specialty area.",
    "Performs surgical procedures for organ transplants, ensuring donor organ suitability and recipient care.",
    "Specializes in rehabilitative interventions for patients with neurological disorders or injuries.",
    "Optimizes healthcare delivery through the use of health information technology and data analysis."
]


doctor_descriptions += [
    "Uses pressure points on the feet, hands, or ears thought to correspond to different body organs and systems to promote relaxation and wellness.",
    "Assists in diagnostic and interventional cardiac procedures, such as cardiac catheterizations and echocardiograms.",
    "Addresses obesity and weight-related health issues through medical and sometimes surgical interventions.",
    "Provides specialized care for patients with life-threatening neurological and neurosurgical conditions.",
    "Focuses on mental health within a community setting, providing advanced nursing interventions and education.",
    "Evaluates and treats patients with breathing or cardiopulmonary disorders, administering therapies and monitoring ventilators.",
    "Delivers advanced nursing care in a broad range of medical and surgical units, leading quality improvement.",
    "Performs and interprets tests that evaluate electrical activity in the brain and nervous system.",
    "Provides objective medical evaluations and expert opinion, often for legal or insurance purposes.",
    "Offers high-level nursing expertise for acutely ill patients, typically in hospital or critical care settings.",
    "Provides healthcare services in the patient’s home to improve health outcomes and maintain independence.",
    "Treats and cares for patients with respiratory disorders, often providing advanced therapies and ventilator support."
]

# Build the FAISS index from combined text (for better embedding context)
def build_doctor_index(save_path="doctor_specialty_index.faiss"):
    combined_texts = [f"{spec} — {desc}" for spec, desc in zip(doctor_specialties, doctor_descriptions)]
    embeddings = embedding_model.encode(combined_texts)
    index = faiss.IndexFlatL2(embeddings.shape[1])
    index.add(np.array(embeddings))
    faiss.write_index(index, save_path)
    print(f"Doctor specialty index saved to {save_path}")


def load_doctor_index(path="doctor_specialty_index.faiss"):
    return faiss.read_index(path)

def match_doctor(user_input, top_k=3):

    keyword_boost_map = {
        "tooth": "Dentist",
        "teeth": "Dentist",
        "gums": "Dentist",
        "molars": "Dentist",
        "molar": "Dentist",
        "wisdom tooth": "Dentist",
        "dental": "Dentist",
        "oral": "Dentist",
        "cavity": "Dentist",
        "fillings": "Dentist",
        "cavities": "Dentist",
        "root canal": "Dentist",
        "braces": "Dentist",
        "retainer": "Dentist",
        "skin": "Dermatology",
        "rash": "Dermatology",
        "itch": "Dermatology",
        "acne": "Dermatology",
        "eczema": "Dermatology",
        "psoriasis": "Dermatology",
        "scalp": "Dermatology",
        "baby": "Pediatrics",
        "infant": "Pediatrics",
        "child": "Pediatrics",
        "toddler": "Pediatrics",
        "kid": "Pediatrics",
        "ear": "Otolaryngology",
        "hearing": "Audiologist",
        "ringing in ears": "Audiologist",
        "ear infection": "Otolaryngology",
        "sinus": "Otolaryngology",
        "eyesight": "Optometrist",
        "vision": "Optometrist",
        "blurry vision": "Optometrist",
        "dry eyes": "Optometrist",
        "glasses": "Optometrist",
        "cough": "Internal Medicine",
        "shortness of breath": "Internal Medicine",
        "chest pain": "Internal Medicine",
        "heart": "Cardiology",
        "palpitations": "Cardiology",
        "blood pressure": "Cardiology",
        "bone": "Orthopaedic Surgery",
        "joint pain": "Orthopaedic Surgery",
        "fracture": "Orthopaedic Surgery",
        "muscle": "Physical Therapist",
        "sprain": "Physical Therapist",
        "rehab": "Physical Therapist"
    }

    modified_input = user_input.lower()
    for keyword, specialty in keyword_boost_map.items():
        if keyword in modified_input:
            print(f"[KEYWORD WEIGHT] Boosting with specialty '{specialty}' due to keyword '{keyword}'")
            # Append the specialty name to the input to bias the embedding subtly
            modified_input += f" {specialty} {specialty}"

    # Create embedding from modified input
    query_embedding = embedding_model.encode(modified_input).reshape(1, -1)
    index = load_doctor_index()
    distances, indices = index.search(query_embedding, top_k)

    results = []
    for i in indices[0]:
        if i < len(doctor_specialties):
            results.append({
                "specialty": doctor_specialties[i],
                "description": doctor_descriptions[i]
            })

    return results