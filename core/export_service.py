import os
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, HRFlowable
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from models.schemas import SummaryResult, VideoMetadata
from config.settings import EXPORTS_DIR

def export_summary_txt(meta: VideoMetadata, result: SummaryResult) -> str:
    file_path = os.path.join(EXPORTS_DIR, f"Summary_{meta.video_id}.txt")
    content = []
    content.append(f"AI VIDEO SUMMARIZER REPORT")
    content.append("=" * 40)
    content.append(f"Title: {result.title}")
    content.append(f"Source: {meta.source_type.title()} ({meta.url_or_path})")
    content.append(f"Duration: {meta.duration_formatted}\n")
    content.append("SUMMARY OVERVIEW:")
    content.append(result.summary_paragraph)
    content.append("\nKEY HIGHLIGHTS:")
    for kp in result.key_points:
        content.append(f" • {kp}")
        
    content.append("\nIMPORTANT MOMENTS:")
    for h in result.highlights:
        content.append(f" [{h.timestamp}] {h.title} ({h.duration}) - {h.description}")
        
    content.append("\nCHAPTERS:")
    for c in result.chapters:
        content.append(f" [{c.timestamp}] {c.title}: {c.description}")
        
    with open(file_path, "w", encoding="utf-8") as f:
        f.write("\n".join(content))
        
    return file_path

def export_summary_pdf(meta: VideoMetadata, result: SummaryResult) -> str:
    file_path = os.path.join(EXPORTS_DIR, f"Summary_{meta.video_id}.pdf")
    doc = SimpleDocTemplate(file_path, pagesize=letter, rightMargin=36, leftMargin=36, topMargin=36, bottomMargin=36)
    styles = getSampleStyleSheet()
    primary_color = colors.HexColor("#6C5CE7")
    dark_color = colors.HexColor("#0F172A")
    title_style = ParagraphStyle('DocTitle', parent=styles['Heading1'], fontSize=22, textColor=primary_color, spaceAfter=8)
    sub_style = ParagraphStyle('DocSub', parent=styles['Normal'], fontSize=10, textColor=colors.gray, spaceAfter=15)
    h2_style = ParagraphStyle('SectionHeader', parent=styles['Heading2'], fontSize=14, textColor=dark_color, spaceBefore=12, spaceAfter=6)
    body_style = ParagraphStyle('Body', parent=styles['Normal'], fontSize=10, leading=14, textColor=dark_color, spaceAfter=6)
    bullet_style = ParagraphStyle('Bullet', parent=styles['Normal'], fontSize=10, leading=14, leftIndent=15, spaceAfter=4)
    
    elements = []
    elements.append(Paragraph("AI Video Summarizer Report", title_style))
    elements.append(Paragraph(f"Video: <b>{result.title}</b> | Duration: {meta.duration_formatted}", sub_style))
    elements.append(HRFlowable(width="100%", thickness=1, color=primary_color, spaceAfter=12)) 
    elements.append(Paragraph("Executive Summary", h2_style))
    elements.append(Paragraph(result.summary_paragraph, body_style))
    elements.append(Paragraph("Key Insights", h2_style))
    for kp in result.key_points:
        elements.append(Paragraph(f"• {kp}", bullet_style))
        
    elements.append(Paragraph("Key Highlights & Moments", h2_style))
    for h in result.highlights:
        elements.append(Paragraph(f"<b>[{h.timestamp}] {h.title}</b> ({h.duration})<br/>{h.description}", bullet_style))
        
    elements.append(Paragraph("Chapters", h2_style))
    for c in result.chapters:
        elements.append(Paragraph(f"<b>[{c.timestamp}] {c.title}</b> - {c.description}", bullet_style))
        
    doc.build(elements)
    return file_path