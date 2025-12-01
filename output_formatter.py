"""
Output formatter for task assignment results
"""
import pandas as pd
from typing import List, Dict
import os
from datetime import datetime
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch


class OutputFormatter:
    def __init__(self):
        pass
    
    def _escape_html(self, text: str) -> str:
        """Escape HTML special characters for PDF Paragraph"""
        if not text:
            return ""
        text = str(text)
        text = text.replace("&", "&amp;")
        text = text.replace("<", "&lt;")
        text = text.replace(">", "&gt;")
        return text
    
    def format_tasks(self, tasks: List[Dict]) -> pd.DataFrame:
        """
        Format tasks into a pandas DataFrame
        
        Args:
            tasks: List of task dictionaries
            
        Returns:
            pandas DataFrame with formatted tasks
        """
        if not tasks:
            return pd.DataFrame()
        
        data = []
        for task in tasks:
            data.append({
                "#": task.get("id", ""),
                "Task": task.get("task", ""),
                "Assigned To": task.get("assigned_to", "Unassigned"),
                "Deadline": task.get("deadline", "Not specified"),
                "Priority": task.get("priority", "Medium"),
                "Dependencies": task.get("dependencies", ""),
                "Reason": task.get("reason", "")
            })
        
        df = pd.DataFrame(data)
        return df
    
    def display_table(self, tasks: List[Dict]):
        """
        Display tasks in a formatted table
        
        Args:
            tasks: List of task dictionaries
        """
        df = self.format_tasks(tasks)
        
        if df.empty:
            print("\nNo tasks identified.")
            return
        
        print("\n" + "="*120)
        print("IDENTIFIED TASKS WITH DETAILS".center(120))
        print("="*120)
        
        pd.set_option('display.max_columns', None)
        pd.set_option('display.width', None)
        pd.set_option('display.max_colwidth', 30)
        
        print(df.to_string(index=False))
        print("="*120)
    
    def save_to_csv(self, tasks: List[Dict], output_path: str = "task_assignments.csv"):
        """
        Save tasks to CSV file
        
        Args:
            tasks: List of task dictionaries
            output_path: Path to save CSV file
        """
        df = self.format_tasks(tasks)
        df.to_csv(output_path, index=False)
        print(f"\nTasks saved to {output_path}")
    
    def save_to_pdf(self, tasks: List[Dict], output_path: str = None, audio_file: str = None):
        """
        Save tasks to PDF file with professional formatting
        
        Args:
            tasks: List of task dictionaries
            output_path: Path to save PDF file (optional, auto-generated if None)
            audio_file: Original audio file name for reference
        """
        if not tasks:
            print("\nNo tasks to save to PDF.")
            return
        
        if output_path is None:
            if audio_file:
                base_name = os.path.splitext(os.path.basename(audio_file))[0]
                output_path = f"{base_name}_task_assignments.pdf"
            else:
                output_path = f"task_assignments_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        
        if not output_path.endswith('.pdf'):
            output_path += '.pdf'
        
        doc = SimpleDocTemplate(
            output_path, 
            pagesize=letter,
            leftMargin=0.5*inch,
            rightMargin=0.5*inch,
            topMargin=0.5*inch,
            bottomMargin=0.5*inch
        )
        story = []
        
        styles = getSampleStyleSheet()
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=20,
            textColor=colors.HexColor('#1a1a1a'),
            spaceAfter=30,
            alignment=1 
        )
        
        heading_style = ParagraphStyle(
            'CustomHeading',
            parent=styles['Heading2'],
            fontSize=14,
            textColor=colors.HexColor('#2c3e50'),
            spaceAfter=20
        )
        
        title = Paragraph("Meeting Task Assignment Report", title_style)
        story.append(title)
        story.append(Spacer(1, 0.2*inch))
        
        if audio_file:
            metadata_text = f"<b>Source Audio:</b> {os.path.basename(audio_file)}<br/>"
        else:
            metadata_text = ""
        metadata_text += f"<b>Generated:</b> {datetime.now().strftime('%B %d, %Y at %I:%M %p')}<br/>"
        metadata_text += f"<b>Total Tasks:</b> {len(tasks)}"
        metadata = Paragraph(metadata_text, styles['Normal'])
        story.append(metadata)
        story.append(Spacer(1, 0.3*inch))
        
        section = Paragraph("Identified Tasks with Details", heading_style)
        story.append(section)
        story.append(Spacer(1, 0.1*inch))
        
        cell_style = ParagraphStyle(
            'CellStyle',
            parent=styles['Normal'],
            fontSize=9,
            leading=11,
            spaceAfter=6,
            spaceBefore=6
        )
        
        header_style = ParagraphStyle(
            'HeaderStyle',
            parent=styles['Normal'],
            fontSize=11,
            textColor=colors.whitesmoke,
            fontName='Helvetica-Bold',
            leading=13
        )
        
        table_data = []
        
        headers = ["#", "Task", "Assigned To", "Deadline", "Priority", "Dependencies", "Reason"]
        header_row = [Paragraph(self._escape_html(str(h)), header_style) for h in headers]
        table_data.append(header_row)
        
        for task in tasks:
            row = [
                Paragraph(self._escape_html(str(task.get("id", ""))), cell_style),
                Paragraph(self._escape_html(task.get("task", "")), cell_style),
                Paragraph(self._escape_html(task.get("assigned_to", "Unassigned")), cell_style),
                Paragraph(self._escape_html(task.get("deadline", "Not specified")), cell_style),
                Paragraph(self._escape_html(task.get("priority", "Medium")), cell_style),
                Paragraph(self._escape_html(task.get("dependencies", "") or "-"), cell_style),
                Paragraph(self._escape_html(task.get("reason", "") or "-"), cell_style)
            ]
            table_data.append(row)
        
        table = Table(table_data, repeatRows=1, colWidths=[
            0.35*inch,  
            2.8*inch,   
            0.9*inch,   
            1.0*inch,   
            0.7*inch,   
            1.0*inch,   
            1.15*inch   
        ])
        
        table_style = TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#34495e')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 11),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('TOPPADDING', (0, 0), (-1, 0), 12),
            
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 9),
            ('BACKGROUND', (0, 1), (-1, -1), colors.white),
            ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
            ('GRID', (0, 0), (-1, -1), 1, colors.grey),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f8f9fa')]),
            ('LEFTPADDING', (0, 0), (-1, -1), 6),
            ('RIGHTPADDING', (0, 0), (-1, -1), 6),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ])
        
        table.setStyle(table_style)
        story.append(table)
        
        doc.build(story)
        print(f"\n✓ PDF report saved to: {output_path}")

