

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time



def detect_ai_percentage_selenium(text):
    from selenium.webdriver.chrome.service import Service
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)
    driver.get("https://www.zerogpt.com/")
    wait = WebDriverWait(driver, 20)

    # Find the textarea and paste the text
    textarea = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "textarea#textArea.textarea.notresizable")))
    textarea.clear()
    textarea.send_keys(text)


    # Hide sticky footer and banners if present (ad/cookie/banner overlays)
    try:
        driver.execute_script('var el = document.getElementById("fs-sticky-footer"); if (el) { el.style.display = "none"; }')
        driver.execute_script('var banners = document.getElementsByClassName("banner-a"); for (var i = 0; i < banners.length; i++) { banners[i].style.display = "none"; }')
        # Hide any generic overlays
        driver.execute_script("""
            var overlays = document.querySelectorAll('[style*="z-index"]');
            overlays.forEach(function(el){el.style.display="none";});
        """)
        # Hide header if present
        driver.execute_script('var header = document.getElementById("navbar"); if (header) { header.style.display = "none"; }')
        time.sleep(0.5)
        time.sleep(0.5)
    except Exception:
        pass

    # Find the Detect Text button
    detect_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Detect Text')]")))
    # Scroll button into view
    driver.execute_script("arguments[0].scrollIntoView(true);", detect_btn)
    time.sleep(0.2)
    detect_btn.click()

    # Wait for the result to appear (AI percentage)
    # Wait for the result to appear, try to find any element containing a %
    import re
    time.sleep(3)  # Wait for result to render
    candidates = driver.find_elements(By.XPATH, "//*[contains(text(), '%')]")
    for elem in candidates:
        txt = elem.text.strip()
        print(f"[DEBUG] Candidate: {txt}")
        match = re.search(r"(\d+)%", txt)
        if match:
            ai_percent = int(match.group(1))
            driver.quit()
            return ai_percent
    print("[ERROR] Could not find AI percentage. Candidates:")
    for elem in candidates:
        print(elem.text.strip())
    driver.quit()
    raise Exception("Could not find AI percentage on the page.")



# Paraphrasing step is not automated here, as it would require similar Selenium automation for QuillBot or another tool.

# Basic humanization: shuffle sentences, replace some words, add minor randomization
import random
def paraphrase_text(text):
    print("[INFO] Attempting basic humanization.")
    # Split into sentences
    import re
    sentences = re.split(r'(?<=[.!?]) +', text)
    random.shuffle(sentences)
    new_text = ' '.join(sentences)
    # Replace some common words with synonyms
    replacements = {
        'students': 'learners',
        'teachers': 'educators',
        'AI': 'artificial intelligence',
        'helps': 'assists',
        'improve': 'enhance',
        'problems': 'challenges',
        'value': 'importance',
        'technology': 'innovation',
        'feedback': 'responses',
        'tasks': 'duties',
        'plan': 'prepare',
        'backgrounds': 'histories',
        'difficulties': 'challenges',
        'reminds': 'alerts',
        'responsible': 'thoughtful',
        'fun': 'enjoyable',
        'available': 'accessible',
        'connection': 'relationship',
        'data': 'information',
        'machine': 'device',
        'machines': 'devices',
        'answer': 'respond',
        'answers': 'responses',
        'question': 'query',
        'questions': 'queries',
        'explain': 'clarify',
        'explanation': 'clarification',
        'topic': 'subject',
        'topics': 'subjects',
        'clearly': 'plainly',
        'support': 'assist',
        'supporting': 'assisting',
        'find out': 'discover',
        'watch': 'monitor',
        'monitor': 'observe',
        'suggest': 'recommend',
        'ways': 'methods',
        'good': 'beneficial',
        'uses': 'applications',
        'fear': 'worry',
        'forget': 'overlook',
        'real': 'genuine',
        'remind': 'alert',
        'careful': 'cautious',
        'better': 'improved',
        'more': 'additional',
        'still': 'yet',
        'human': 'person',
        'education': 'learning',
        'personal': 'individual',
        'records': 'logs',
        'time': 'period',
        'plan': 'prepare',
        'lesson': 'session',
        'lessons': 'sessions',
        'style': 'approach',
        'speed': 'pace',
        'match': 'align',
        'countries': 'nations',
        'colleges': 'universities',
        'online': 'virtual',
        'class': 'course',
        'classes': 'courses',
        'translate': 'convert',
        'languages': 'tongues',
        'speaking': 'communicating',
        'reading': 'interpreting',
        'difficulties': 'obstacles',
        'improve': 'advance',
        'teaching': 'instruction',
        'teaches': 'instructs',
        'teaching': 'educating',
        'records': 'logs',
        'plan': 'prepare',
        'reminds': 'alerts',
        'responsible': 'accountable',
        'fun': 'enjoyable',
        'available': 'accessible',
        'connection': 'relationship',
        'important': 'significant',
        'improving': 'advancing',
        'making': 'creating',
        'easier': 'simpler',
        'difficult': 'challenging',
        'problems': 'issues',
        'issue': 'matter',
        'issues': 'matters',
        'remind': 'alert',
        'responsibility': 'duty',
        'responsibilities': 'duties',
        'careful': 'cautious',
        'responsible': 'accountable',
        'value': 'worth',
        'fear': 'concern',
        'depend': 'rely',
        'depend on': 'rely upon',
        'forget': 'overlook',
        'right way': 'proper manner',
        'make': 'create',
        'available': 'obtainable',
        'keeping': 'maintaining',
        'connection': 'link',
        'reminds': 'alerts',
        'responsible': 'accountable',
        'fun': 'pleasurable',
        'available': 'attainable',
        'connection': 'bond',
    }
    for k, v in replacements.items():
        new_text = re.sub(rf'\b{k}\b', v, new_text, flags=re.IGNORECASE)
    # Add a random phrase at the end
    endings = [
        "This is just one perspective.",
        "The future remains to be seen.",
        "Many factors can influence these outcomes.",
        "It's a topic open for discussion.",
        "Further research is always valuable."
    ]
    if random.random() < 0.5:
        new_text += ' ' + random.choice(endings)
    return new_text



def humanize_text(text, threshold=40):
    current_text = text
    attempts = 0
    while attempts < 4:
        ai_percent = detect_ai_percentage_selenium(current_text)
        print(f"AI-detected percentage: {ai_percent}%")
        if ai_percent < threshold:
            return current_text
        current_text = paraphrase_text(current_text)
        attempts += 1
        time.sleep(1)
    print("[WARN] Could not humanize text below threshold after 4 attempts.")
    return current_text


def main():
    input_text = """
    Artificial Intelligence (AI) is changing the way we learn and teach. It helps students by giving them lessons that match their learning style and speed. AI tools can also answer questions, explain topics clearly, and give feedback to help students improve. For teachers, AI can do tasks like checking tests and keeping records. This gives teachers more time to talk with students and plan better lessons.

AI also makes learning easier for people from different countries and backgrounds. It can translate languages and help students with speaking or reading difficulties. In colleges and online classes, AI can watch how students are doing, find out who needs help, and suggest ways to support them.

Even though AI has many good uses, there are some problems too. People worry about how their personal data is used and whether AI is always fair. Some fear that we might depend too much on machines and forget the value of real teachers.

This abstract talks about how AI is helping students and teachers in many ways. It also reminds us to be careful and responsible when using this technology. If used in the right way, AI can make education better, more fun, and available to more people, while still keeping the human connection in learning."""
    result = humanize_text(input_text)
    print("\nHumanized text:\n", result)


if __name__ == "__main__":
    main()
