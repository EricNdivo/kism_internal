import os
import win32com.client as win32
from docx import Document
from docxcompose.composer import Composer
from django.http import HttpResponse
from django.conf import settings

def create_mail_merge_document(template_path, context):
    doc = Document(template_path)

    for paragraph in doc.paragraphs:
        for key, value in context.items():
            if f"{{{{{key}}}}}" in paragraph.text:
                paragraph.text = paragraph.text.replace(f"{{{{{key}}}}}", str(value))


    temp_doc_path = os.path.join(settings.MEDIA_ROOT, 'temp_document.docx')
    doc.save(temp_doc_path)

    return temp_doc_path

def merge_to_pdf(doc_path):
    word = win32.Dispatch('Word.Application')
    word.Visible = False
    doc = word.Documents.Open(doc_path)
    pdf_path = doc_path.replace('.docx', '.pdf')
    doc.SaveAs(pdf_path, FileFormat=17)  
    doc.Close()
    word.Quit()
    return pdf_path

def generate_certificate(context):
    template_path = os.path.join(settings.MEDIA_ROOT, 'templates', 'certificates', 'certificate_template.docx')
    
    
    merged_doc_path = create_mail_merge_document(template_path, context)
    pdf_path = merge_to_pdf(merged_doc_path)
    
    
    with open(pdf_path, 'rb') as pdf_file:
        response = HttpResponse(pdf_file.read(), content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="{context["certificate_number"]}.pdf"'
    
    
    os.remove(merged_doc_path)
    os.remove(pdf_path)

    return response
