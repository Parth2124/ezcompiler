import subprocess
from django.shortcuts import render
from django.http import JsonResponse
import json
import re
import google.generativeai as genai
import os

# Configure Gemini AI
genai.configure(api_key="AIzaSyBiqmM0DFS2poPqU0snddTOTPTA7KfXji4")

def home(request):
    if request.method == "POST":
        data = json.loads(request.body)
        java_question = data.get("java_question", "")

        prompt = f"""
        Generate a **Java program only** for the following request:
        {java_question}

        - Use proper Java syntax.
        - The class should be named `Main`.
        - The code should compile without errors.
        - Do NOT include explanations, markdown, or comments.
        """

        model = genai.GenerativeModel("gemini-1.5-pro")
        response = model.generate_content(prompt)
        raw_code = response.text.strip() if response else "Error generating code."

        # Clean any markdown formatting
        clean_code = re.sub(r"^```[a-zA-Z]*\n|```$", "", raw_code).strip()

        return JsonResponse({"java_code": clean_code})

    return render(request, "index.html")

import subprocess
from django.http import JsonResponse
import json
import os

def run_code(request):
    if request.method == "POST":
        data = json.loads(request.body)
        java_code = data.get("java_code", "")
        user_input = data.get("user_input", [])  # List of inputs

        java_filename = "Main.java"
        class_filename = "Main.class"

        with open(java_filename, "w") as file:
            file.write(java_code)

        try:
            # Compile Java Code
            compile_process = subprocess.run(
                ["javac", java_filename], capture_output=True, text=True
            )

            if compile_process.returncode != 0:
                return JsonResponse({"output": compile_process.stderr})

            # Ensure user input is a string with new lines
            input_text = "\n".join(map(str, user_input)) + "\n" if user_input else ""

            # Run Java Code with interactive input handling
            process = subprocess.Popen(
                ["java", "Main"],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )

            # Provide input and capture output
            stdout, stderr = process.communicate(input_text)

            return JsonResponse({"output": stdout if process.returncode == 0 else stderr})

        except subprocess.TimeoutExpired:
            return JsonResponse({"output": "Error: Code execution timed out."})

        finally:
            # Cleanup files
            if os.path.exists(java_filename):
                os.remove(java_filename)
            if os.path.exists(class_filename):
                os.remove(class_filename)


from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

@csrf_exempt  # Remove this if using CSRF token in frontend
def generate_code(request):
    if request.method == "POST":
        data = json.loads(request.body)
        java_question = data.get("java_question", "")

        # Simulating AI-generated Java Code
        generated_code = f"// Java program for: {java_question}\npublic class Solution {{\n    public static void main(String[] args) {{\n        System.out.println(\"Hello, World!\");\n    }}\n}}"

        return JsonResponse({"java_code": generated_code})

    return JsonResponse({"error": "Invalid request"}, status=400)




# import google.generativeai as genai
# from django.shortcuts import render
# from django.http import JsonResponse
# import subprocess
# import os
# import re  # Import regex for cleaning AI output

# genai.configure(api_key="AIzaSyBiqmM0DFS2poPqU0snddTOTPTA7KfXji4")  # Add your API key

# def home(request):
#     if request.method == "POST":
#         import json
#         data = json.loads(request.body)
#         java_question = data.get("java_question", "")

#         prompt = f"""
#         Generate a **Java program only** for the following request:
#         {java_question}

#         - Use proper Java syntax.
#         - Include `public class Main` with a `main` method.
#         - Do NOT use Python syntax (like `def`, `print()`, `# comments`).
#         - Ensure the program compiles without errors.
#         - Only return the Java code **without explanations or markdown formatting**.
#         """

#         model = genai.GenerativeModel("gemini-1.5-pro")
#         response = model.generate_content(prompt)
#         raw_code = response.text.strip() if response else "Error generating code."

#         # **Fix AI Markdown Formatting Issue**
#         # clean_code = re.sub(r"```[\s\S]*?\n", "", raw_code)  # Remove ```java and ``` markers
#         clean_code = re.sub(r"^```[a-zA-Z]*\n|```$", "", raw_code).strip()

#         clean_code = clean_code.strip()

#         return JsonResponse({"java_code": clean_code})

#     return render(request, "index.html")

# import subprocess
# from django.http import JsonResponse

# import subprocess
# from django.http import JsonResponse
# import json

# def run_code(request):
#     if request.method == "POST":
#         data = json.loads(request.body)

#         java_code = data.get("java_code", "")
#         user_input = data.get("user_input", [])  # List of inputs (e.g., ["5", "10"])

#         java_filename = "Main.java"
#         with open(java_filename, "w") as file:
#             file.write(java_code)

#         # Compile Java Code
#         compile_process = subprocess.run(["javac", java_filename], capture_output=True, text=True)
#         if compile_process.returncode != 0:
#             return JsonResponse({"output": compile_process.stderr})  # Compilation error

#         # Ensure inputs are formatted correctly
#         input_text = "\n".join(map(str, user_input)) if user_input else ""

#         try:
#             # Run Java with Proper Input Handling
#             run_process = subprocess.run(
#                 ["java", "Main"],
#                 input=input_text,  # Ensure input is passed
#                 capture_output=True,
#                 text=True,
#                 timeout=5
#             )

#             return JsonResponse({"output": run_process.stdout if run_process.returncode == 0 else run_process.stderr})

#         except subprocess.TimeoutExpired:
#             return JsonResponse({"output": "Error: Code execution timed out."})

