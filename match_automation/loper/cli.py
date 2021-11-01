import os

import click

from pdf_report import generate_school_pdf_reports_for_students, write_match_pdf_report_to_disk
from user import get_personalized_school_notes_for_users


@click.command()
@click.option('--user_dir_path', help='The directory where the user Excel files are located')
@click.option('--output_dir', default='.', help='The output directory where the Excel will be written')
@click.option('--content_file_path', default=None, help='The file path to the school content Excel')
def notes(user_dir_path: str, output_dir: str, content_file_path: str):
    print('Generating notes...')
    custom_notes_df = get_personalized_school_notes_for_users(user_dir_path=user_dir_path,
                                                              content_file_path=content_file_path)
    print('Writing custom notes to Excel')
    custom_notes_df.to_excel(excel_writer=os.path.join(output_dir, 'user_custom_notes.xlsx'),
                             sheet_name='User Custom Notes')


@click.command()
@click.option('--user_dir_path', help='The directory where the user Excel files are located')
@click.option('--output_dir', default='.', help='The output directory where the Excel will be written')
@click.option('--content_file_path', default=None, help='The file path to the school content Excel')
def reports(user_dir_path: str, output_dir: str, content_file_path: str, media_dir: str):
    pdf_reports = generate_school_pdf_reports_for_students(user_dir_path=user_dir_path,
                                                           content_file_path=content_file_path,
                                                           media_dir=media_dir)
    for pdf_report in pdf_reports:
        write_match_pdf_report_to_disk(output_dir=output_dir, pdf_report=pdf_report)


if __name__ == '__main__':
    notes()
