import customtkinter as ctk
from google import genai
import os
import pyperclip
from dotenv import load_dotenv

# 1. Cargamos la API Key desde el archivo .env por seguridad
load_dotenv()

class PromptApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Configuración visual de la ventana
        self.title("AI Prompt Optimizer - Rodrigo's Edition")
        self.geometry("700x700")
        ctk.set_appearance_mode("dark")

        # 2. Inicialización del cliente con la sintaxis que te funcionó
        api_key = os.getenv("GEMINI_API_KEY")
        self.client = genai.Client(api_key=api_key)

        self.setup_ui()

    def setup_ui(self):
        # --- SECCIÓN DE ENTRADA ---
        self.label = ctk.CTkLabel(self, text="Prompt Original:", font=("Segoe UI", 16, "bold"))
        self.label.pack(pady=(20, 5))

        self.input_text = ctk.CTkTextbox(self, height=120, width=600)
        self.input_text.pack(pady=5)

        self.btn_clear_input = ctk.CTkButton(
            self, text="Limpiar Entrada 🗑️", 
            command=lambda: self.input_text.delete("1.0", "end"),
            fg_color="#a13333", hover_color="#7a2626", width=120
        )
        self.btn_clear_input.pack(pady=(0, 10))

        # --- BOTÓN DE ACCIÓN PRINCIPAL ---
        self.btn_refine = ctk.CTkButton(
            self, 
            text="Refinar con IA ✨", 
            command=self.refine_prompt,
            fg_color="#3a7ebf",
            hover_color="#2a5a8a",
            height=45,
            font=("Segoe UI", 14, "bold")
        )
        self.btn_refine.pack(pady=20)

        # --- SECCIÓN DE SALIDA ---
        self.label_result = ctk.CTkLabel(self, text="Prompt Optimizado:", font=("Segoe UI", 16, "bold"))
        self.label_result.pack(pady=(10, 5))

        self.output_text = ctk.CTkTextbox(self, height=180, width=600)
        self.output_text.pack(pady=5)

        # Contenedor para botones de salida
        self.button_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.button_frame.pack(pady=10)

        self.btn_copy = ctk.CTkButton(
            self.button_frame, text="Copiar Resultado 📋", 
            command=self.copy_to_clipboard, fg_color="#28a745", hover_color="#218838"
        )
        self.btn_copy.grid(row=0, column=0, padx=10)

        self.btn_clear_output = ctk.CTkButton(
            self.button_frame, text="Limpiar Resultado 🗑️", 
            command=lambda: self.output_text.delete("1.0", "end"),
            fg_color="#a13333", hover_color="#7a2626"
        )
        self.btn_clear_output.grid(row=0, column=1, padx=10)

    def copy_to_clipboard(self):
        text = self.output_text.get("1.0", "end-1c")
        if text.strip():
            pyperclip.copy(text)
            self.btn_copy.configure(text="¡Copiado! ✅")
            self.after(2000, lambda: self.btn_copy.configure(text="Copiar Resultado 📋"))

    def refine_prompt(self):
        user_input = self.input_text.get("1.0", "end-1c")
        
        if not user_input.strip():
            self.output_text.delete("1.0", "end")
            self.output_text.insert("1.0", "⚠️ Escribe algo para poder ayudarte.")
            return

        # Instrucciones para que la mejora sea precisa
        system_instructions = (
            
# Versión anterior:            
#            "Eres un experto en Prompt Engineering. Tu tarea es mejorar el prompt "
#            "del usuario para que sea más claro, tenga contexto y asigne un rol a la IA. "
#            "Responde únicamente con el prompt mejorado."

# Nueva versión mejorada (foforce):
            "Actúa como un Ingeniero de Prompts Senior experto en la optimización de interacciones con modelos de lenguaje (LLM). Tu objetivo es transformar prompts básicos o ambiguos en instrucciones estructuradas, precisas y de alto rendimiento."
            "Para cada solicitud de optimización:"
            "1. **Asigna un Rol:** Define una personalidad experta específica para la IA."
            "2. **Contextualiza:** Explica el propósito de la tarea y el entorno de la solicitud."
            "3. **Define la Tarea:** Describe con claridad la acción principal y los pasos a seguir."
            "4. **Establece Restricciones:** Indica formatos de salida, tono, límites de palabras o elementos prohibidos."
            "5. **Estructura:** Utiliza delimitadores y una jerarquía lógica para facilitar la comprensión del modelo."
            "Responde exclusivamente con el texto del prompt mejorado, sin incluir introducciones, explicaciones ni comentarios adicionales."
        )
        try:
            response = self.client.models.generate_content(
                model="gemini-3-flash-preview", 
                contents=f"{system_instructions}\n\nOptimiza el siguiente prompt: {user_input}"
            )
            
            self.output_text.delete("1.0", "end")
            self.output_text.insert("1.0", response.text)
        except Exception as e:
            self.output_text.delete("1.0", "end")
            self.output_text.insert("1.0", f"❌ Error: {str(e)}")

if __name__ == "__main__":
    app = PromptApp()
    app.mainloop()