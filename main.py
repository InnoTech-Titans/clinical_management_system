import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

# Model
# Define classes to represent the data structure
class Doctor:
    def __init__(self, doctor_id, first_name, last_name, specialisation):
        # Initialize doctor attributes
        self.doctor_id = doctor_id
        self.first_name = first_name
        self.last_name = last_name
        self.specialisation = specialisation
        self.patients = [] # List of assigned patients
        self.consultations = [] # List of consultations

    def assign_patient(self, patient):
         # Method to assign a patient to the doctor
        self.patients.append(patient)

    def add_consultation(self, consultation):
        # Method to add a consultation to the doctor's record
        self.consultations.append(consultation)

    def get_info(self):
        # Method to get doctor's information
        # This includes doctor ID, name, specialization, list of patients, and list of consultations
        patient_list = ", ".join([f"{patient.first_name} {patient.last_name}" for patient in self.patients])
        consultation_list = "\n".join([f"{consultation.date}: {consultation.description} (Fee: {consultation.fee})" for consultation in self.consultations])

        info = f"Doctor Information:\n"
        info += f"Doctor ID: {self.doctor_id}\n"
        info += f"Full Name: {self.first_name} {self.last_name}\n"
        info += f"Specialization: {self.specialisation}\n"
        info += f"List of Patients: {patient_list}\n"
        info += f"List of Consultations:\n{consultation_list}"

        return info

class Patient:
    def __init__(self, patient_id, first_name, last_name):
        self.patient_id = patient_id
        self.first_name = first_name
        self.last_name = last_name
        self.doctor = None
        self.consultations = []

    def assign_doctor(self, doctor):
        self.doctor = doctor

    def add_consultation(self, consultation):
        self.consultations.append(consultation)

    def get_info(self):
        doctor_info = self.doctor.get_info() if self.doctor else "No Assigned Doctor"
        consultation_list = "\n".join([f"{consultation.date}: {consultation.description} (Fee: {consultation.fee})" for consultation in self.consultations])

        info = f"Patient Information:\n"
        info += f"Patient ID: {self.patient_id}\n"
        info += f"Full Name: {self.first_name} {self.last_name}\n"
        info += f"Doctor Information:\n{doctor_info}\n"
        info += f"List of Consultations:\n{consultation_list}"

        return info

    def get_consultation_report(self):
        consultation_report = ""
        for consultation in self.consultations:
            consultation_report += f"{consultation.date}: {consultation.description} (Fee: {consultation.fee})\n"
        return consultation_report

class Consultation:
    def __init__(self, date, description, fee):
        self.date = date
        self.description = description
        self.fee = fee

# Define similar classes for Patient and Consultation

# View
# Create a graphical user interface using tkinter
class MedicalCenterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Medical Center Management")

        self.doctors = []
        self.patients = []

        self.create_doctor_list_view()
        self.create_patient_list_view()
        self.create_assignment_buttons()
        self.create_consultation_buttons()
        self.create_info_buttons()
        self.create_search_widgets()

        # Load doctors and patients data from text files
        self.load_doctors_data()
        self.load_patients_data()

    def create_doctor_list_view(self):
        doctor_frame = ttk.LabelFrame(self.root, text="Doctors")
        doctor_frame.grid(row=0, column=0, padx=10, pady=10, sticky='nsew')

        self.doctor_list = ttk.Treeview(doctor_frame, columns=("ID", "Name", "Specialization"), show="headings")
        self.doctor_list.heading("ID", text="ID", anchor="center")
        self.doctor_list.heading("Name", text="Name")
        self.doctor_list.heading("Specialization", text="Specialization")
        self.doctor_list.pack(fill="both", expand=True)

        # Load doctor data from Doctor.txt
        doctor_dict = {}

        try:
            with open('Doctor.txt', 'r') as file:
                data = file.readlines()
                for i, j in enumerate(data, start=1000):
                    doctor_dict[i] = j.strip().split(",")

            ids = list(doctor_dict.keys())

            for i in ids:
                id = i
                name = str(doctor_dict[i][0]) + " " + str(doctor_dict[i][1])
                spec = doctor_dict[i][2]

                self.doctor_list.insert("", "end", values=(id, name, spec))
        except FileNotFoundError:
            print("Doctor.txt file not found.")

    def create_patient_list_view(self):
        # Create a list view for patients
        patient_frame = ttk.LabelFrame(self.root, text="Patients")
        patient_frame.grid(row=0, column=1, padx=10, pady=10, sticky='nsew')

        self.patient_list = ttk.Treeview(patient_frame, columns=("ID", "Name", "Assigned Doctor"), show="headings")
        self.patient_list.heading("ID", text="ID")
        self.patient_list.heading("Name", text="Name")
        self.patient_list.heading("Assigned Doctor", text="Assigned Doctor")
        self.patient_list.pack(fill="both", expand=True)

        # Load patient data from Patient.txt
        patient_dict = {}

        try:
            with open('Patient.txt', 'r') as file:
                data = file.readlines()
                for i, j in enumerate(data, start=2000):
                    patient_dict[i] = j.strip().split(",")

            ids = list(patient_dict.keys())

            for i in ids:
                id = i
                name = str(patient_dict[i][0]) + " " + str(patient_dict[i][1])

                self.patient_list.insert("", "end", values=(id, name))
        except FileNotFoundError:
            print("Patient.txt file not found.")
    
    def create_search_widgets(self):
         # Create search widgets for searching doctors or patients by name
        search_frame = ttk.LabelFrame(self.root, text="Search")
        search_frame.grid(row=4, column=0, columnspan=2, padx=10, pady=10, sticky='nsew')

        ttk.Label(search_frame, text="Search Doctor or Patient by Name:").grid(row=0, column=0, padx=5, pady=5)

        self.search_var = tk.StringVar()
        self.search_entry = ttk.Entry(search_frame, textvariable=self.search_var)
        self.search_button = ttk.Button(search_frame, text="Search", command=self.search)

        self.search_entry.grid(row=0, column=1, padx=5, pady=5)
        self.search_button.grid(row=0, column=2, padx=5, pady=5)
    
      
    def search(self):
        # Implement search functionality
        search_text = self.search_var.get().strip().lower()

        if not search_text:
            return

        matching_doctors = [doctor for doctor in self.doctors if search_text in f"{doctor.first_name} {doctor.last_name}".lower()]
        matching_patients = [patient for patient in self.patients if search_text in f"{patient.first_name} {patient.last_name}".lower()]

        if matching_doctors and matching_patients:
            messagebox.showinfo("Search Result", "Matching doctors and patients found.")
        elif not matching_doctors and not matching_patients:
            messagebox.showinfo("Search Result", "No matching doctors or patients found.")
        else:
            messagebox.showinfo("Search Result", "Matching doctors or patients found.")

        self.update_doctor_list(matching_doctors)
        self.update_patient_list(matching_patients)


        
    def update_doctor_list(self, doctors=None):
        # Update the doctor list in the view
        self.doctor_list.delete(*self.doctor_list.get_children())
        doctors_to_display = doctors if doctors is not None else self.doctors
        for doctor in doctors_to_display:
            self.doctor_list.insert('', 'end', values=(doctor.doctor_id, f"{doctor.first_name} {doctor.last_name}", doctor.specialisation))

# Modify the update_patient_list method
    def update_patient_list(self, patients=None):
        # Update the patient list in the view
        self.patient_list.delete(*self.patient_list.get_children())
        patients_to_display = patients if patients is not None else self.patients
        for patient in patients_to_display:
            assigned_doctor = patient.doctor.get_info() if patient.doctor else "No Assigned Doctor"
            self.patient_list.insert('', 'end', values=(patient.patient_id, f"{patient.first_name} {patient.last_name}", assigned_doctor))
    

    def create_assignment_buttons(self):
        # Create widgets for assigning patients to doctors
        assignment_frame = ttk.LabelFrame(self.root, text="Assignments")
        assignment_frame.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky='nsew')

        ttk.Label(assignment_frame, text="Assign Patient to Doctor:").grid(row=0, column=0, padx=5, pady=5)
        ttk.Label(assignment_frame, text="Patient ID:").grid(row=1, column=0, padx=5, pady=5)
        ttk.Label(assignment_frame, text="Doctor ID:").grid(row=1, column=2, padx=5, pady=5)

        self.patient_id_var = tk.StringVar()
        self.doctor_id_var = tk.StringVar()

        self.patient_id_entry = ttk.Entry(assignment_frame, textvariable=self.patient_id_var)
        self.doctor_id_entry = ttk.Entry(assignment_frame, textvariable=self.doctor_id_var)
        self.assign_button = ttk.Button(assignment_frame, text="Assign", command=self.assign_patient_to_doctor)

        self.patient_id_entry.grid(row=1, column=1, padx=5, pady=5)
        self.doctor_id_entry.grid(row=1, column=3, padx=5, pady=5)
        self.assign_button.grid(row=1, column=4, padx=5, pady=5)

    def create_consultation_buttons(self):
        # Create widgets for adding consultations
        consultation_frame = ttk.LabelFrame(self.root, text="Consultations")
        consultation_frame.grid(row=2, column=0, columnspan=2, padx=10, pady=10, sticky='nsew')

        ttk.Label(consultation_frame, text="Add Consultation:").grid(row=0, column=0, padx=5, pady=5)
        ttk.Label(consultation_frame, text="Patient ID:").grid(row=1, column=0, padx=5, pady=5)
        ttk.Label(consultation_frame, text="Doctor ID:").grid(row=1, column=2, padx=5, pady=5)
        ttk.Label(consultation_frame, text="Date:").grid(row=2, column=0, padx=5, pady=5)
        ttk.Label(consultation_frame, text="Description:").grid(row=2, column=2, padx=5, pady=5)
        ttk.Label(consultation_frame, text="Fee:").grid(row=2, column=4, padx=5, pady=5)

        self.consultation_patient_id_var = tk.StringVar()
        self.consultation_doctor_id_var = tk.StringVar()
        self.consultation_date_var = tk.StringVar()
        self.consultation_description_var = tk.StringVar()
        self.consultation_fee_var = tk.StringVar()

        self.consultation_patient_id_entry = ttk.Entry(consultation_frame, textvariable=self.consultation_patient_id_var)
        self.consultation_doctor_id_entry = ttk.Entry(consultation_frame, textvariable=self.consultation_doctor_id_var)
        self.consultation_date_entry = ttk.Entry(consultation_frame, textvariable=self.consultation_date_var)
        self.consultation_description_entry = ttk.Entry(consultation_frame, textvariable=self.consultation_description_var)
        self.consultation_fee_entry = ttk.Entry(consultation_frame, textvariable=self.consultation_fee_var)
        self.add_consultation_button = ttk.Button(consultation_frame, text="Add Consultation", command=self.add_consultation)

        self.consultation_patient_id_entry.grid(row=1, column=1, padx=5, pady=5)
        self.consultation_doctor_id_entry.grid(row=1, column=3, padx=5, pady=5)
        self.consultation_date_entry.grid(row=2, column=1, padx=5, pady=5)
        self.consultation_description_entry.grid(row=2, column=3, padx=5, pady=5)
        self.consultation_fee_entry.grid(row=2, column=5, padx=5, pady=5)
        self.add_consultation_button.grid(row=3, column=0, columnspan=6, padx=5, pady=5)

    def create_info_buttons(self):
    # Create widgets for viewing information
        info_frame = ttk.LabelFrame(self.root, text="Information")
        info_frame.grid(row=3, column=0, columnspan=2, padx=10, pady=10, sticky='nsew')

        ttk.Label(info_frame, text="View Information:").grid(row=0, column=0, padx=5, pady=5)
        ttk.Label(info_frame, text="ID:").grid(row=1, column=0, padx=5, pady=5)

        self.info_id_var = tk.StringVar()

        self.info_id_entry = ttk.Entry(info_frame, textvariable=self.info_id_var)
        self.view_doctor_button = ttk.Button(info_frame, text="View Doctor Info", command=self.view_doctor_info)
        self.view_patient_button = ttk.Button(info_frame, text="View Patient Info", command=self.view_patient_info)
        self.view_consultation_button = ttk.Button(info_frame, text="View Consultation Report", command=self.view_consultation_report)

        self.info_id_entry.grid(row=1, column=1, padx=5, pady=5)
        self.view_doctor_button.grid(row=1, column=2, padx=5, pady=5)
        self.view_patient_button.grid(row=1, column=3, padx=5, pady=5)
        self.view_consultation_button.grid(row=1, column=4, padx=5, pady=5)

    def load_doctors_data(self):
    # Load doctor data from a text file (Doctor.txt)
        try:
            with open('Doctor.txt', 'r') as file:
                data = file.readlines()
                for i, j in enumerate(data, start=1000):
                    doctor_data = j.strip().split(",")
                    doctor = Doctor(int(i), *doctor_data)
                    self.doctors.append(doctor)
        except FileNotFoundError:
            print("Doctor.txt file not found.")

    def load_patients_data(self):
    # Load patient data from a text file (Patient.txt)
        try:
            with open('Patient.txt', 'r') as file:
                data = file.readlines()
                for i, j in enumerate(data, start=2000):
                    patient_data = j.strip().split(",")
                    patient = Patient(int(i), *patient_data)
                    self.patients.append(patient)
        except FileNotFoundError:
            print("Patient.txt file not found.")

    def assign_patient_to_doctor(self):
    # Implement patient assignment to a doctor
        patient_id = self.patient_id_var.get()
        doctor_id = self.doctor_id_var.get()

        try:
            patient = next(patient for patient in self.patients if patient.patient_id == int(patient_id))
            doctor = next(doctor for doctor in self.doctors if doctor.doctor_id == int(doctor_id))
            patient.assign_doctor(doctor)
            doctor.assign_patient(patient)
            self.update_patient_list()
            self.update_doctor_list()
            messagebox.showinfo("Assignment", f"Patient {patient.first_name} {patient.last_name} assigned to Doctor {doctor.first_name} {doctor.last_name}.")
        except StopIteration:
            messagebox.showerror("Error", "Patient or doctor not found.")

    def add_consultation(self):
    # Implement adding consultations for patients and doctors
        patient_id = self.consultation_patient_id_var.get()
        doctor_id = self.consultation_doctor_id_var.get()
        date = self.consultation_date_var.get()
        description = self.consultation_description_var.get()
        fee = self.consultation_fee_var.get()

        try:
            patient = next(patient for patient in self.patients if patient.patient_id == int(patient_id))
            doctor = next(doctor for doctor in self.doctors if doctor.doctor_id == int(doctor_id))
            consultation = Consultation(date, description, fee)
            patient.add_consultation(consultation)
            doctor.add_consultation(consultation)
            self.update_patient_list()
            self.update_doctor_list()
            messagebox.showinfo("Consultation", f"Consultation added for Patient {patient.first_name} {patient.last_name} with Doctor {doctor.first_name} {doctor.last_name}.")
        except StopIteration:
            messagebox.showerror("Error", "Patient or doctor not found.")

    def view_doctor_info(self):
    # Display doctor information in a separate window
        doctor_id = self.info_id_var.get()
        try:
            doctor = next(doctor for doctor in self.doctors if doctor.doctor_id == int(doctor_id))
            info = doctor.get_info()
            self.display_info(info)
        except StopIteration:
            messagebox.showerror("Error", "Doctor not found.")

    def view_patient_info(self):
    # Display patient information in a separate window
        patient_id = self.info_id_var.get()
        try:
            patient = next(patient for patient in self.patients if patient.patient_id == int(patient_id))
            info = patient.get_info()
            self.display_info(info)
        except StopIteration:
            messagebox.showerror("Error", "Patient not found.")

    def view_consultation_report(self):
    # Display consultation report for a patient in a separate window
        patient_id = self.info_id_var.get()
        try:
            patient = next(patient for patient in self.patients if patient.patient_id == int(patient_id))
            consultation_report = patient.get_consultation_report()
            self.display_info(consultation_report)
        except StopIteration:
            messagebox.showerror("Error", "Patient not found.")

    def display_info(self, info):
    # Display information in a separate window
        info_window = tk.Toplevel(self.root)
        info_window.title("Information")
        info_label = ttk.Label(info_window, text=info, wraplength=400)
        info_label.pack(padx=10, pady=10)

    def update_doctor_list(self):
    # Update the doctor list in the view
        self.doctor_list.delete(*self.doctor_list.get_children())
        for doctor in self.doctors:
            self.doctor_list.insert('', 'end', values=(doctor.doctor_id, f"{doctor.first_name} {doctor.last_name}", doctor.specialisation))

    def update_patient_list(self):
    # Update the patient list in the view
        self.patient_list.delete(*self.patient_list.get_children())
        for patient in self.patients:
            assigned_doctor = patient.doctor.get_info() if patient.doctor else "No Assigned Doctor"
            self.patient_list.insert('', 'end', values=(patient.patient_id, f"{patient.first_name} {patient.last_name}", assigned_doctor))

if __name__ == "__main__":
    root = tk.Tk()
    app = MedicalCenterApp(root)
    root.mainloop()
