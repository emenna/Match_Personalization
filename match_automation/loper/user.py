from functools import partial
from os import walk
from os.path import join

import pandas as pd
from typing import Dict, List


class User:

    def __init__(self,
                 name: str,
                 username: str,
                 email_addr: str,
                 phone_number: str,
                 gender: str,
                 race: str,
                 ethnicity: str,
                 grad_year: str,
                 gpa_band: str,
                 match_answers: pd.DataFrame,
                 school_matches: pd.DataFrame):

        # user data
        self.name = name
        self.username = username
        self.email_addr = email_addr
        self.phone_number = phone_number
        self.gender = gender
        self.race = race
        self.ethnicity = ethnicity
        self.grad_year = grad_year
        self.gpa_band = gpa_band

        # match data
        self.match_answers = match_answers
        self.school_matches = school_matches

    def get_user_data(self) -> Dict[str, str]:
        return {
            'name': self.name,
            'username': self.username,
            'email_addr': self.email_addr,
            'phone_number': self.phone_number,
            'gender': self.gender,
            'race': self.race,
            'ethnicity': self.ethnicity,
            'grad_year': self.grad_year,
            'gpa_band': self.gpa_band
        }


def read_user_from_disk(file_path: str) -> User:
    output_tab_df = pd.read_excel(io=file_path, sheet_name='Output Tab')
    summary_schools_df = pd.read_excel(io=file_path, sheet_name='Summary_Schools')
    var_dict = output_tab_df.set_index('Variable').to_dict('index')

    return User(name=f'{var_dict["fname"]["Value"]} {var_dict["lname"]["Value"]}',
                username='N/A',
                email_addr=var_dict['email']['Value'],
                phone_number=var_dict['phone']['Value'],
                gender=var_dict['gender']['Value'],
                race=var_dict['race']['Value'],
                ethnicity=var_dict['ethnicity']['Value'],
                grad_year=var_dict['gradyear']['Value'],
                gpa_band=var_dict['gpaband']['Value'],
                match_answers=output_tab_df,
                school_matches=summary_schools_df)


def read_school_data_from_disk(file_path: str) -> pd.DataFrame:
    return pd.read_excel(io=file_path, sheet_name='Master_Storage', header=1)


def get_personalized_school_notes_for_user(user: User, content_df: pd.DataFrame) -> Dict[str, List[str]]:
    included_schools = user.school_matches[user.school_matches['INCLUDE']]

    # apply foundational preferences
    row_mask = pd.Series(data=[False] * len(content_df))
    var_dict = user.match_answers.set_index('Variable').to_dict('index')

    if var_dict['foundational_preferences_social']['Value']:
        row_mask = row_mask | (content_df['Social'])
    if var_dict['foundational_preferences_extracurriculars']['Value']:
        row_mask = row_mask | (content_df['Extracurriculars'])
    if var_dict['foundational_preferences_campus']['Value']:
        row_mask = row_mask | (content_df['Campus'])
    if var_dict['foundational_preferences_career']['Value']:
        row_mask = row_mask | (content_df['Career'])
    if var_dict['foundational_preferences_diversity']['Value']:
        row_mask = row_mask | (content_df['Diversity'])
    if var_dict['foundational_preferences_athletics']['Value']:
        row_mask = row_mask | (content_df['Athletics'])
    if var_dict['foundational_preferences_community']['Value']:
        row_mask = row_mask | (content_df['Community'])

    triggers = [k for k, v in var_dict.items() if v == {'Value': 'R'}]
    row_mask = row_mask | content_df['Trigger(s)'].isin(triggers)
    filtered_content_df = content_df[row_mask].fillna('')

    filtered_content_df['notes'] = filtered_content_df[['(If applicable) Hyperlink used', '(If applicable) Text written']].apply(list, axis=1)
    content_dict = filtered_content_df.groupby('UNITID')['notes'].apply(list).to_dict()
    return {school_row['INSTNM']: content_dict.get(school_row['UNITID'], [['', '']])
            for index, school_row in included_schools.iterrows()}


def get_personalized_school_notes_for_users(user_dir_path: str, content_file_path: str) -> pd.DataFrame:
    user_filenames = [join(user_dir_path, filename) for filename in next(walk(user_dir_path), (None, None, []))[2]]
    content_df = read_school_data_from_disk(file_path=content_file_path)
    get_notes = partial(get_personalized_school_notes_for_user, content_df=content_df)

    data = []
    for user_filename in user_filenames:
        user = read_user_from_disk(file_path=user_filename)
        try:
            school_to_notes_dict = get_notes(user=user)
            for school, notes in school_to_notes_dict.items():
                for note in notes:
                    data.append({
                        'name': user.name,
                        'email': user.email_addr,
                        'school': school,
                        'note': note[1],
                        'link': note[0]
                    })
        except Exception as e:
            data.append({
                'name': user.name,
                'email': user.email_addr,
                'school': 'ERROR!',
                'note': e,
                'link': ''
            })

    personalized_notes_df = pd.DataFrame(data)
    return personalized_notes_df[personalized_notes_df['note'] != '']
