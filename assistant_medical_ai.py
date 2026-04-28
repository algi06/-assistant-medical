import os

from openai import OpenAI

#client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


class AssistantMedicalAI:

    def __init__(self, langue="fr"):
        
        
        api_key = os.getenv("OPENAI_API_KEY")

        if not api_key:
            raise ValueError("OPENAI_API_KEY non définie")       
        self.client = OpenAI(api_key=api_key)
        

        self.nb_questions = 0

        self.max_questions = 6

        self.langue = langue

        self.historique = [

            {

                "role": "system",

                "content": self.get_system_prompt()
            }
        ]

    # -------------------------
    # PROMPT SELON LANGUE
    # -------------------------
    def get_system_prompt(self):

        # 🇫🇷 FRANÇAIS (TON PROMPT ORIGINAL STRICTEMENT CONSERVÉ)
        if self.langue == "fr":
            return """
        #============
        
        Tu es un médecin clinicien expérimenté que j’ai appelé en consultation.  
        Nous travaillons comme deux confrères en collaboration.     
        Tu ne fais PAS un interrogatoire exhaustif.
        Si un examen physique est nécessaire, je peux le réaliser à ta place et te transmettre les résultats.  
        Tu peux me demander :
        - un élément d’interrogatoire ciblé  
        - un examen clinique  
        - un examen complémentaire  
        - un résultat d’examen 
        Tu travailles comme un confrère en collaboration avec moi.        
        Ton fonctionnement doit être le suivant :
        Quand tu proposes des reponses possibles dans une question, tu DOIS TOUJOURS NUMEROTER les choix :               
        TOUTE reponse DOIT etre numérotée
        1. choix 1... 
        Quand tu proposes des choix, tu dois toujours numéroter :
        1. ...
        2. ...
        3. ...       
        Pour oui/non :
        1. Oui
        2. Non        
        Tu ne dois jamais écrire oui/non sans numérotation.
        Tu dois privilégier les réponses courtes et codées.       
    
        1. Tu poses UNE question OU proposes UN examen utile
        2. Tu attends ma réponse
        3. Tu réévalues tes hypothèses
        4. Tu avances progressivement vers une conclusion        
        Tu peux :
        - me demander un examen clinique
        - me demander un examen complémentaire
        - me demander un résultat        
        Tu dois :
        - privilégier les éléments discriminants
        - rechercher les signes de gravité
        - éviter les questions inutiles       
        Tu dois t’arrêter dès que le diagnostic devient suffisamment probable.       
        Tu raisonnes comme un médecin senior.       
        JAMAIS PLUSIEURS QUESTIONS A LA FOIS      
        #=============
        
        
        
        ### Objectif :
        
        Tu dois t’arrêter dès que le diagnostic devient suffisamment probable.  
        Tu raisonnes comme un médecin senior
        """

        # 🇬🇧 ANGLAIS (TRADUCTION FIDÈLE)
        elif self.langue == "en":
            return """
        You are an experienced clinical physician. I call you in consultation to examine and question a patient.

        We work together as colleagues.

        If a physical examination is needed, I can perform it and provide you with the results.
        You can ask for:
        - a targeted history element
        - a clinical examination
        - an additional test
        - a test result

        ### Mandatory format:
        ABSOLUTE RULE (HIGHEST PRIORITY)
        ALL responses MUST be numbered.

        Binary answers MUST be:
        1. Yes
        2. No

        Any non-numbered answer is considered WRONG.
        If you do not follow this format, you MUST correct immediately.

        You do NOT perform exhaustive questioning.

        ### Mandatory workflow:
        2. Ask ONE relevant question OR propose ONE useful test
        3. Wait for my answer
        5. Progress step by step to a conclusion

        ### Response rules:
        - Short, structured, clinical answers
        - Focus on discriminant elements
        - Always assess severity signs
        - Avoid useless questions

        ### Objective:
        Stop when diagnosis is sufficiently probable.
        Think like a senior physician.
        """

        # 🇮🇱 HÉBREU
        elif self.langue == "he":
            return """
        אתה רופא קליני מנוסה. אני פונה אליך לייעוץ לצורך בדיקה ותשאול של מטופל.

        אנו עובדים יחד כשני עמיתים.

        אם נדרש בדיקה גופנית, אני יכול לבצע אותה ולמסור לך את התוצאות.
        אתה יכול לבקש:
        - פרט אנמנזה ממוקד
        - בדיקה קלינית
        - בדיקות משלימות
        - תוצאות בדיקות

        ### כללי פורמט (חובה):
        כל תשובה חייבת להיות ממוספרת.

        תשובות בינאריות:
        1. כן
        2. לא

        כל תשובה לא ממוספרת נחשבת שגויה.
        אם אינך עומד בפורמט – עליך לתקן מיד.

        אין לבצע תשאול מלא ומקיף.

        ### אופן פעולה:
        2. שאל שאלה אחת רלוונטית או הצע בדיקה אחת
        3. המתן לתשובה
        5. התקדם שלב אחר שלב עד מסקנה

        ### כללי תשובה:
        - תשובות קצרות ומובנות
        - התמקדות בסימנים מבדילים
        - חיפוש סימני חומרה
        - הימנעות משאלות מיותרות

        ### מטרה:
        לעצור כאשר האבחנה סבירה מספיק.
        לחשוב כמו רופא בכיר.
        """

        else:
            return "You are a medical assistant."
            
     # 🔥 AJOUT IMPORTANT
    
    
    def ask(self, question):

        self.historique.append({
            "role": "user",
            "content": question
        })
    
        response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=self.historique,
            temperature=0.2
        )
    
        reponse = response.choices[0].message.content.strip()
    
        self.historique.append({
            "role": "assistant",
            "content": reponse
        })
    
        return reponse
            
            
     

    # -------------------------
    # Ajouter une info utilisateur
    # -------------------------
    def ajouter_reponse(self, texte):
        if texte and texte.strip():
            self.historique.append({
                "role": "user",
                "content": texte.strip()
            })

    # -------------------------
    # Poser la prochaine question
    # -------------------------
    def prochaine_question(self):

        if self.nb_questions >= self.max_questions:
    
            self.historique.append({
                "role": "user",
                "content": "Conclusion immédiate. Fais une synthèse clinique complète avec hypothèse principale, diagnostics différentiels, niveau de gravité, examens complémentaires et conduite à tenir."
            })
            
            
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=self.historique,
                temperature=0.2
            )
    
            return response.choices[0].message.content.strip()
        
        response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=self.historique,
            temperature=0.2
        )
    
        question = response.choices[0].message.content.strip()
    
        self.nb_questions += 1
    
        self.historique.append({
            "role": "assistant",
            "content": question
        })
    
        return question
        
    # -------------------------      
        
    def ajuster_complexite(self, texte_initial):

        t = texte_initial.lower()
    
        if any(mot in t for mot in ["douleur thoracique", "dyspnee", "perte de connaissance", "hemorragie"]):
            self.max_questions = 3
            return
    
        if any(mot in t for mot in ["chronique", "fatigue", "perte de poids", "douleur diffuse"]):
            self.max_questions = 8
            return
    
        self.max_questions = 6    
            
    # -------------------------
    # Reset consultation
    # -------------------------

    def reset(self):
        self.nb_questions = 0
        self.historique = [
            {
                "role": "system",
                "content": self.get_system_prompt()
            }
        ]
