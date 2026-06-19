from flask import Flask, render_template, request
import os
from dotenv import load_dotenv
import google.generativeai as genai
from markdown import markdown
import time
load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-2.5-flash")

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():

    report = None
    company = None

    if request.method == "POST":

        company = request.form.get("company")

        prompt = f"""

        Generate a professional Company Intelligence Report for {company}.

        Use:
        Proper bullet points
        Proper spacing between sections
        
        Do not write content on a single line.
        Each heading and label must appear on a separate line.

        Return the report in VALID MARKDOWN format.

        Use:

        * ## for section headings
        * ### for subsection headings
        * **bold** labels
        * Proper bullet points
        * Proper spacing between sections

        Do not write content on a single line.
        Each heading and label must appear on a separate line.

        ## 1. Company Overview

        Provide:

        * What the company does
        * Industry
        * Scale
        * Geographic presence

        ## 2. Key Business Information

        Provide:

        * Major offerings
        * Recent developments
        * Expansion plans
        * Important public information

        ## 3. Potential Business Challenges

        Identify and explain:

        ### Operational Bottlenecks

        Reasoning:
        Explanation

        ### Sales Challenges

        Reasoning:
        Explanation

        ### Customer Experience Challenges

        Reasoning:
        Explanation

        ## 4. AI Opportunities

        Suggest 3 company-specific AI opportunities.

        For EACH opportunity use EXACTLY this structure:

        ### Opportunity Name

        **Problem:**

        Explanation

        **AI Solution:**

        Explanation

        **Business Impact:**

        Explanation

        Leave a blank line between every field.

        Do NOT write:

        * Problem: ...
        * AI Solution: ...
        * Business Impact: ...

        Each label must appear on its own line.

        Focus on practical opportunities related to:

        * Automation
        * Customer Engagement
        * Sales
        * Operations
        * Analytics
        * Document Processing

        Recommendations must be specific to the company.

        ## 5. Personalized CEO Pitch

        Assume you are meeting the CEO in person.

        Start directly with:

        Dear [CEO Name],

        If the CEO name is unknown, use:

        Dear CEO,

        Do not introduce yourself.

        Do not mention:

        * Your name
        * Your role
        * Consultant
        * Consultancy
        * Organization
        * Contact information
        * Signature blocks

        Start by referencing the company, its operations, growth strategy, or business challenges.

        Example style:

        "After reviewing the company's operations, expansion plans, and market position, several opportunities stand out where AI can create measurable business value."

        End the pitch with a concise summary of expected business outcomes such as:

        * Improved project delivery
        * Higher sales efficiency
        * Better customer satisfaction
        * Reduced operational costs

        The pitch must:

        * Address the CEO directly
        * Explain why you are reaching out
        * Reference specific business challenges identified in this report
        * Reference specific AI opportunities identified in this report
        * Recommend practical AI solutions
        * Explain expected business impact
        * Demonstrate understanding of the company's industry, operations, and growth strategy
        * Be tailored specifically to the company

        Writing Style Requirements:

        * Direct business language
        * Executive tone
        * Recommendation-driven
        * Clear and concise
        * Maximum 350 words
        * One page only

        Avoid:

        * Marketing language
        * Sales language
        * "Imagine..."
        * "Consider..."
        * "Transform..."
        * "Revolutionize..."
        * "Unlock potential..."
        * Future-looking promotional statements

        The pitch should read like an executive recommendation prepared after analyzing the company, not a sales proposal.

        """

        try:
            start = time.time()

            response = model.generate_content(prompt)

            print(f"Time Taken: {time.time() - start:.2f} seconds")
            clean_text = response.text
            clean_text = clean_text.replace("- ##", "##")
            clean_text = clean_text.replace("* ##", "##")
            clean_text = clean_text.replace("```markdown", "")
            clean_text = clean_text.replace("```", "")

            report = markdown(clean_text)



        except Exception as e:

            print("ERROR:", e)

            if "429" in str(e):

                report = """
                       <div class="error-box">
                           <h2>API Quota Exceeded</h2>
                           <p>Please try again later.</p>
                       </div>
                       """

            else:

                report = f"""
                       <div class="error-box">
                           <h2>Something Went Wrong</h2>
                           <p>{str(e)}</p>
                       </div>
                       """

    return render_template(
        "index.html",
        report=report,
        company=company
    )

if __name__ == "__main__":
    app.run(debug=True)