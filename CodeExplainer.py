import ollama
import customtkinter
import threading
import webbrowser
import ctypes

client = ollama.Client()
appId = "bcbstudios.codeexplainer.1.0"
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(appId)

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("blue")

app = customtkinter.CTk()
app.geometry("900x600")
app.title("Code Explainer by BCB Studios")
app.iconbitmap("CodeExplainerIcon.ico")

# region Functions
def is_ollama_running():
    try:
        client.list()
        return True
    except:
        return False

def OnClick():
    if not is_ollama_running():
        aiBox.configure(state="normal")
        aiBox.delete("1.0", "end")
        aiBox.insert("end", "❗ Ollama is not running.\nPlease install and start Ollama.")
        aiBox.configure(state="disabled")
        return
    analyzeBtn.configure(state="disabled", text="Analyzing...")

    userCode = codeBox.get("1.0", "end")
    
    codeBox.configure(state="disabled")

    aiBox.configure(state="normal")
    aiBox.delete("1.0", "end")
    aiBox.insert("end", "🔍 Analyzing your code...\nPlease wait...")
    aiBox.configure(state="disabled")

    thread = threading.Thread(target=Ai, args=(userCode,), daemon=True)
    thread.start()

def Ai(userCode):
    aiModel = "codellama:7b"
    aiPrompt = f"""
    You are a friendly Computer Science Teaching Agent.
    Please explain the following code clearly for a student.
    Provide summary and line-by-line explanation.

    CODE:
    {userCode}
    """

    aiResponse = client.generate(model=aiModel, prompt=aiPrompt)

    aiBox.configure(state="normal")
    aiBox.delete("1.0", "end")
    aiBox.insert("end", aiResponse["response"])
    aiBox.configure(state="disabled")

    analyzeBtn.configure(state="normal", text="Analyze Code")
    codeBox.configure(state="normal")

def openBcbStudiosPage(event=None):
    url = "https://bcb-studios.itch.io/"
    
    webbrowser.open(url)
# endregion

# region GUI
title = customtkinter.CTkLabel(app, text="Code Explainer", font=("Segoe UI", 28, "bold"))
title.pack(pady=(30, 5))

subTitle = customtkinter.CTkLabel(app, text="Analyze your Python code privately and instantly", font=("Segoe UI", 14), text_color="gray")
subTitle.pack(pady=(0, 0))

subTitle2 = customtkinter.CTkLabel(app, text="-BCB Studios-", font=("Segoe UI", 14), text_color="gray")
subTitle2.pack(pady=(0, 20))

mainFrame = customtkinter.CTkFrame(app, fg_color="transparent")
mainFrame.pack(fill="both", expand=True, padx=30, pady=20)

leftBox = customtkinter.CTkFrame(mainFrame, corner_radius=20)
leftBox.pack(side="left", fill="both", expand=True, padx=(15,0))

rightBox = customtkinter.CTkFrame(mainFrame, corner_radius=20)
rightBox.pack(side="right", fill="both", expand=True, padx=(15, 0))

codeLabel = customtkinter.CTkLabel(leftBox, text="Paste or Write you code here:-", font=("Segoe UI", 13, "bold"))
codeLabel.pack(anchor="w", padx=15, pady=(15, 5))

codeBox = customtkinter.CTkTextbox(leftBox, font=("Consolas", 12))
codeBox.pack(fill="both", expand=True, padx=15, pady=10)

analyzeBtn = customtkinter.CTkButton(leftBox, text="Analyze Code", hover_color="#2563eb", height=45, font=("Segoe UI", 14, "bold"), command=OnClick)
analyzeBtn.pack(padx=15, pady=(0, 10))

aiLabel = customtkinter.CTkLabel(rightBox, text="Explanation:-", font=("Segoe UI", 18, "bold"), text_color="#4cc9f0")
aiLabel.pack(anchor="w", padx=15, pady=(15, 10))

aiBox = customtkinter.CTkTextbox(rightBox)
aiBox.pack(fill="both", expand=True, padx=15, pady=(0, 15))
aiBox.configure(state="disabled")
# endregion

# region AdBanner
bannerFrame = customtkinter.CTkFrame(app, height=60, fg_color="#1f1f1f")
bannerFrame.pack(fill="x", side="top")

bannerLabel = customtkinter.CTkLabel(bannerFrame, text="🔔 Visit BCB Studios on Itch.io!", font=("Segoe UI", 16, "bold"), text_color="#ffd700")
bannerLabel.pack(pady=10)

bannerLabel.bind("<Button-1>", openBcbStudiosPage)
# endregion

app.mainloop()