import pypandoc
from rapport_markdown import generate_markdown_report

markdown = generate_markdown_report()

def markdown_to_docx(markdown_report, chemin_sortie):

    pypandoc.convert_text(
        markdown_report,
        "docx",
        format="md",
        outputfile=chemin_sortie,
        extra_args=["--resource-path=."]
    )

markdown_to_docx(markdown, "output/rapport_text.docx")

