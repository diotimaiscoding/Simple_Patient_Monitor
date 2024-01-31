# Written by Çağla Çam
# For Introduction to programming Lecture

import os

def read_file(file_name): #file_name must be a string.

    current_dir_path = os.getcwd() #getting current directory path.
    reading_file_name = file_name
    reading_file_path = os.path.join(current_dir_path, reading_file_name) #file path to read.

    with open(reading_file_path, "r") as f: #"r" for reading.
        data = f.readlines()

    for i in range(len(data)):
        data[i] = data[i].replace("\n", "")
        data[i] = data[i].replace(" Cancer", "xCancer")
        data[i] = data[i].replace(" Therapy", "xTherapy")
        data[i] = data[i].split(" ")
        data[i] = [elem.replace("xCancer", " Cancer") for elem in data[i]]
        data[i] = [elem.replace("xTherapy", " Therapy") for elem in data[i]]
    return data

commands = read_file("doctors_aid_inputs.txt")


patient_list = [] #Information. We can turn this to a csv file later on.


#Checks for if given patient is already recorded or not.

def does_exist(patient_name): 

    #It returns '0' if patient with name 'patient_name' has not recorded.
    statement = 0
    
    for i in range(len(patient_list)):

        if patient_name == patient_list[i][0]:
            #We give it a plus one because we want i to return 'True' even if the index is zero.
            statement = i + 1
                   
    return statement


#Adding Patients to patient_list.

def create(patient_name, diagnosis_accuracy, disease_name, disease_incidence, treatment_name, treatment_risk):

    if does_exist(patient_name):

        return f'Patient {patient_name} cannot be recorded due to duplication.\n'

    else:

        patient_list.append([patient_name, diagnosis_accuracy, disease_name,
                            disease_incidence, treatment_name, treatment_risk])
        return "Patient {} is recorded.\n".format(patient_name)


#Removing Patients from the patient_list.

def remove(patient_name):

    if does_exist(patient_name):

        patient_list.remove(patient_list[does_exist(patient_name)-1]) #Minus one because 'does_exist' function returns i + 1, not i.
        return f'Patient {patient_name} is removed.\n'

    else:

        return f'Patient {patient_name} cannot be removed due to absence.\n'


#Showing patient_list in a table.

def list():

    patient_table = ["Patient\tDiagnosis\tDisease\t\t\tDisease\t\tTreatment\t\tTreatment\n",
                    "Name\tAccuracy\tName\t\t\tIncidence\tName\t\t\tRisk\n",
                    "-------------------------------------------------------------------------\n"] #creating a patient_list table.
    
    if len(patient_list)!=0:
        for i in range(len(patient_list)):

            if len(patient_list[i][0])<4:
                a0 = patient_list[i][0]+"\t\t"
            else:
                a0 = patient_list[i][0]+"\t" #Patient Name.
            a0 = str(a0).replace("ş", "s")

            a1 = str(round(float(patient_list[i][1])*100,2))
            if len(a1) < 5:
                a1 = a1 + "0%\t\t" #Diagnosis Accuracy.
            else:
                a1 = a1 + "%\t\t"

            a2 = patient_list[i][2]
            if len(a2)<4: #Disease Name.
                a2 = a2+"\t\t\t\t"
            elif len(a2)<8:
                a2 = a2+"\t\t\t"
            elif len(a2)<12:
                a2 = a2+"\t\t"
            elif len(a2)<16:
                a2 = a2+"\t"
            else:
                a2 = a2
            
            a3 = str(patient_list[i][3])+"\t" #Disease Incidence.
            
            a4 = str(patient_list[i][4])
            if len(a4)<4: #Treatment Name.
                a4 = a4+"\t\t\t\t"
            elif len(a4)<8:
                a4 = a4+"\t\t\t"
            elif len(a4)<12:
                a4 = a4+"\t\t"
            elif len(a4)<16:
                a4 = a4+"\t"
            else:
                a4 = a4
            
            a5 = str(round(float(patient_list[i][5])*100,2))+"%\n" #Treatment Risk.
            a5 = a5.replace(".0", "")

            elem = a0 + a1 + a2 + a3 + a4 + a5

            patient_table.append(elem)
        
    print_this = ""
    for p in patient_table:
        print_this += p
        
    return print_this


#Calculating and printing probability.

def probability_value(patient_name):
    D_A = float(patient_list[does_exist(patient_name)-1][1]) #Diagnosis Accuracy
    D_I = eval(patient_list[does_exist(patient_name)-1][3]) #Disease Incidence
    probability_value = round((2-D_A**(-1)-D_I**(-1)+(D_I*D_A)**(-1))**(-1)*100, 2) #Probability of True Positive.
    return probability_value
        
    ###CALCULATIONS###
    """ 
    When we construct a confusion matrix, and give x for probability of True Positive, we get probability of
    False Negative is disease_insidence - x and True Negative
    as diagnosis_accuracy - x thus find the probability of False Positive as disease_incidence + x, 
    because True Positive + True Negative = disease_incidence.
    And since True Positives are equal to disease_incidence times diagnosis accuracy which was x, and probablity of
    True Positives is equal to True Positive over True Positive plus False Positive which is equal to x over disease_incidence + 2x,
    We have the probability that given above. It is multiplied by 100 because we were asked to find probability as percentage.
    """


def probability(patient_name):

    if does_exist(patient_name):

        return f'Patient {patient_name} has a probability of {str(probability_value(patient_name)).replace(".0", "")}% of having {str(patient_list[does_exist(patient_name)-1][2]).lower()}.\n'

    else:
        
        return f'Probability for {patient_name} cannot be calculated due to absence.\n'


#Print Recommendations.

def recommendation(patient_name):

    if does_exist(patient_name):

        if probability_value(patient_name)>float(patient_list[does_exist(patient_name)-1][5]):
            return f'System suggests {patient_name} to have the treatment.\n'
        else:
            return f'System suggests {patient_name} NOT to have the treatment.\n'

    else:
        return f'Recommendation for {patient_name} cannot be calculated due toabsence.\n'


#Write file

write_this = ""
if len(commands) != 0:
    for i in range(len(commands)):
        func_name = commands[i][0]
        inside = ""
        for elem in commands[i][1:]:
            inside +=  "\""+elem.replace(",", "")+"\""+","
        attributes = "("+inside+")"
        write_this += eval(func_name + attributes)

def write_file(file_name): #file_name must be a string
    current_dir_path = os.getcwd()
    writing_file_name = file_name
    writing_file_path = os.path.join(current_dir_path, writing_file_name)
    with open(writing_file_path, 'w') as f:
        f.write(write_this)

write_file("doctors_aid_outputs.txt")
