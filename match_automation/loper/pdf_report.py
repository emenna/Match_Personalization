from os import walk
from os.path import join, abspath, dirname
from typing import List
from functools import partial
from pdfkit import from_file

from user import User, get_personalized_school_notes_for_user, read_user_from_disk, read_school_data_from_disk


class PdfReport:

    def __init__(self, user: User, customized_messages):
        self.user = user
        self.customized_messages = customized_messages


def generate_school_pdf_report_for_student(user_file_path: str, content_file_path: str, media_dir: str) -> PdfReport:
    user = read_user_from_disk(file_path=user_file_path)
    content_df = read_school_data_from_disk(file_path=content_file_path)
    customized_messages = get_personalized_school_notes_for_user(user=user, content_df=content_df)
    return PdfReport(user=user, customized_messages=customized_messages)


def generate_school_pdf_reports_for_students(user_dir_path: str,
                                             content_file_path: str,
                                             media_dir: str) -> List[PdfReport]:
    user_filenames = [join(user_dir_path, filename) for filename in next(walk(user_dir_path), (None, None, []))[2]]
    gen_pdf_report = partial(generate_school_pdf_report_for_student,
                             content_file_path=content_file_path,
                             media_dir=media_dir)
    return [gen_pdf_report(user_file_path=user_file_path) for user_file_path in user_filenames]


def write_match_pdf_report_to_disk(output_dir: str, pdf_report: PdfReport):

    from_file(input=join(dirname(abspath(__file__)), 'resources', 'templates', 'pdf_report_v1.html'),
              output_path='out.pdf', options={'quiet': ''})
