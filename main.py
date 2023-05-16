import tkinter as tk
import urllib.request
import json

class MyApp:
    API_URL = "https://bb33-2402-8100-2261-2d83-438-77a7-4ec-9adc.ngrok-free.app/get-all"
    DELETE_API_URL = "https://bb33-2402-8100-2261-2d83-438-77a7-4ec-9adc.ngrok-free.app/remove"

    def __init__(self, master):
        # Create three frames as columns
        delete_frame = tk.Frame(master, borderwidth=1, relief="solid")
        data_frame = tk.Frame(master, borderwidth=1, relief="solid")
        misc_frame = tk.Frame(master, borderwidth=1, relief="solid")
        
        # Add widgets to the delete frame
        tk.Label(delete_frame, text="Delete Section", font=("Arial", 16)).pack()
        delete_input_form = tk.Frame(delete_frame)
        tk.Label(delete_input_form, text="Index to be deleted:", font=("Arial", 12), pady=10).pack(side="left")
        self.delete_index_entry = tk.Entry(delete_input_form, font=("Arial", 12))
        self.delete_index_entry.pack(side="left", padx=5)
        delete_input_form.pack()
        delete_button = tk.Button(delete_frame, text="DELETE", font=("Arial", 12), command=self.delete_data)
        delete_button.pack(pady=(0, 10))
        
        # Add widgets to the data frame
        tk.Label(data_frame, text="Data Section", font=("Arial", 16)).pack()
        self.data_text = tk.Text(data_frame, height=50, width=50)
        self.data_text.pack()
        
        # Add widgets to the misc frame
        tk.Label(misc_frame, text="Misc Section", font=("Arial", 16)).pack()
        input_form = tk.Frame(misc_frame)
        tk.Label(input_form, text="Question:").pack(side="left")
        self.question_entry = tk.Entry(input_form)
        self.question_entry.pack(side="left")
        tk.Label(input_form, text="Answer:").pack(side="left")
        self.answer_entry = tk.Entry(input_form)
        self.answer_entry.pack(side="left")
        input_form.pack()
        submit_button = tk.Button(misc_frame, text="Submit", command=self.submit_form)
        submit_button.pack()
        
        # Pack the frames side by side with vertical borders
        delete_frame.grid(row=0, column=2, sticky="nsew", padx=10, pady=10)
        data_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        misc_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)

                # configure grid layout to expand columns evenly
        master.columnconfigure(0, weight=10)
        master.columnconfigure(1, weight=1)
        master.columnconfigure(2, weight=1)
        master.rowconfigure(0, weight=1)

    def delete_data(self):
        try:
            delete_index = self.delete_index_entry.get()
            data = {"index": delete_index}
            json_data = json.dumps(data).encode('utf-8')
            headers = {'Content-type': 'application/json'}
            request = urllib.request.Request(self.DELETE_API_URL, data=json_data, headers=headers, method='POST')
            response = urllib.request.urlopen(request)
            print(response.read().decode('utf-8'))
            self.fetch_data_from_api(None)
        except Exception as e:
            print(e)

    def fetch_data_from_api(self, frame):
        try:
            api_url = self.API_URL
            response = urllib.request.urlopen(api_url)
            data = response.read().decode('utf-8')
            parsed_data = json.loads(data)
            self.data_text.delete("1.0", tk.END)
            for index, entry in enumerate(parsed_data['faqs'], 0):
                question = entry['question']
                answer = entry['answer']
                self.data_text.insert(tk.END, f"#{index}\n")
                self.data_text.insert(tk.END, f"Question: {question}\n")
                self.data_text.insert(tk.END, f"Answer: {answer}\n\n")
        except Exception as e:
            print(e)



    def submit_form(self):
        try:
            question = self.question_entry.get()
            answer = self.answer_entry.get()
            data = {
                "question": question,
                "answer": answer
            }
            json_data = json.dumps(data).encode('utf-8')
            headers = {'Content-type': 'application/json'}
            request = urllib.request.Request("https://bb33-2402-8100-2261-2d83-438-77a7-4ec-9adc.ngrok-free.app/add", data=json_data, headers=headers, method='POST')
            response = urllib.request.urlopen(request)
            print(response.read().decode('utf-8'))
            self.fetch_data_from_api(None)
        except Exception as e:
            print(e)

root = tk.Tk()
app = MyApp(root)
app.fetch_data_from_api(None)
root.mainloop()

