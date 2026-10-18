import pypandoc
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__))))
from rapport_markdown import generate_markdown_report
from config import OUTPUT_DIR

#markdown = generate_markdown_report()
#chemin_sortie = OUTPUT_DIR

def markdown_to_docx(markdown_report, chemin_sortie):

    pypandoc.convert_text(
        markdown_report,
        "docx",
        format="md",
        outputfile=chemin_sortie,
        extra_args=["--resource-path=."]
    )

if __name__=="__main__":
    print("Well")
    #markdown_to_docx(markdown, chemin_sortie)

