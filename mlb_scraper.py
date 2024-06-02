##### THIS SCRIPT WILL RUN EVERYDAY SCRAPING THE LATEST SCORES #####
import os
import re
import requests as req
from bs4 import BeautifulSoup
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from datetime import datetime, timedelta

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

def main():
    """Shows basic usage of the Sheets API.
    Creates a new spreadsheet and adds worksheets with scraped data.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            ##### Please change the cred.json to the one you have downloaded from the google developer console ########
            flow = InstalledAppFlow.from_client_secrets_file("cred.json", SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open("token.json", "w") as token:
            token.write(creds.to_json())

    try:
        service = build("sheets", "v4", credentials=creds)
        
        # Create a new spreadsheet
        # spreadsheet = {"properties": {"title": "Baseball Data"}}
        # spreadsheet = service.spreadsheets().create(body=spreadsheet, fields="spreadsheetId").execute()
       
       ##### Please change the spreadsheet_id to the one you want to update ########
        spreadsheet_id = "1A00RX1QBu2LbfFOAp_tAEHF6P92NT3mbTssQIPU3JJw"
        print(f"Spreadsheet ID: {spreadsheet_id}")

        # URL of the webpage to scrape
        url = 'https://baseballmonster.com/boxscores.aspx'

        # Fetch the webpage
        response = req.get(url)
        if response.status_code == 200:
            html_content = response.content

            # Parse the HTML
            soup = BeautifulSoup(html_content, 'html.parser')

            # Find all tables with the class 'datatable w3-hoverable'
            tables = soup.find_all('table', {'class': 'datatable w3-hoverable'})

            # Find match details
            find_teams = soup.find_all('p', {'class': 'text minP'})
            match_between_teams = []
            for match in find_teams:
                match_between_teams.append(match.text)

            # Initialize lists to store the extracted data from all tables
            matches_data = []

            # Process tables in pairs
            for i in range(0, len(tables), 2):
                if i + 1 >= len(tables):
                    break
                
                table_bat = tables[i]
                table_pitch = tables[i + 1]

                # Initialize lists to store the extracted data for the current match
                match_data_bat = []
                match_data_pitch = []

                # Process batting table
                thead_bat = table_bat.find('thead')
                if thead_bat:
                    headers_bat = [header.text.strip() for header in thead_bat.find_all('th')]
                    headers_bat.append('Opponent')
                    headers_bat.append('Win/Loss')
                    rows_bat = table_bat.find_all('tr')[1:]  # Skipping the first row which is the header
                    for row in rows_bat:
                        cols_bat = row.find_all('td')
                        cols_bat = [col.text.strip() for col in cols_bat]
                        if not any(cols_bat):
                            continue
                        # Add opponent and win/loss information
                        match_str = match_between_teams[i//2]
                        regex = r"(\b[A-Z]{2,3}\b) \((\d+)\) @ (\b[A-Z]{2,3}\b) \((\d+)\)"
                        regex1 = r'([A-Z]{3}) \((\d+)\) @ ([A-Z]{3}) (\d+) \((\d+)\)'
                        match = re.search(regex, match_str)
                        match1 = re.search(regex1, match_str)
                        if match or match1:
                            if match:
                                team1, score1, team2, score2 = match.groups()
                                score1, score2 = int(score1), int(score2)
                                if cols_bat[6] == team1:
                                    opponent = team2
                                    win_loss = 'W' if score1 > score2 else 'L'
                                elif cols_bat[6] == team2:
                                    opponent = team1
                                    win_loss = 'W' if score2 > score1 else 'L'
                                else:
                                    opponent = '-'
                                    win_loss = '-'
                                cols_bat.append(opponent)
                                cols_bat.append(win_loss)
                            else:
                                team1, score1, team2, score2, mis = match1.groups()
                                score1, score2 = int(score1), int(score2)
                                if cols_bat[6] == team1:
                                    opponent = team2
                                    win_loss = 'W' if score1 > score2 else 'L'
                                elif cols_bat[6] == team2:
                                    opponent = team1
                                    win_loss = 'W' if score2 > score1 else 'L'
                                else:
                                    opponent = '-'
                                    win_loss = '-'
                                cols_bat.append(opponent)
                                cols_bat.append(win_loss)
                        headers_bat[0] = 'Date'
                        player_data_bat = dict(zip(headers_bat, cols_bat))
                        match_data_bat.append(player_data_bat)
                
                # Process pitching table
                thead_pitch = table_pitch.find('thead')
                if thead_pitch:
                    headers_pitch = [header.text.strip() for header in thead_pitch.find_all('th')]
                    headers_pitch.append('Opponent')
                    headers_pitch.append('Win/Loss')
                    rows_pitch = table_pitch.find_all('tr')[1:]  # Skipping the first row which is the header
                    for row in rows_pitch:
                        cols_pitch = row.find_all('td')
                        cols_pitch = [col.text.strip() for col in cols_pitch]
                        if not any(cols_pitch):
                            continue
                        # Add opponent and win/loss information
                        match_str = match_between_teams[i//2]
                        regex = r"(\b[A-Z]{2,3}\b) \((\d+)\) @ (\b[A-Z]{2,3}\b) \((\d+)\)"
                        regex1 = r'([A-Z]{3}) \((\d+)\) @ ([A-Z]{3}) (\d+) \((\d+)\)'
                        match = re.search(regex, match_str)
                        match1 = re.search(regex1, match_str)
                        if match or match1:
                            if match:
                                team1, score1, team2, score2 = match.groups()
                                score1, score2 = int(score1), int(score2)
                                if cols_pitch[6] == team1:
                                    opponent = team2
                                    win_loss = 'W' if score1 > score2 else 'L'
                                elif cols_pitch[6] == team2:
                                    opponent = team1
                                    win_loss = 'W' if score2 > score1 else 'L'
                                else:
                                    opponent = '-'
                                    win_loss = '-'
                                cols_pitch.append(opponent)
                                cols_pitch.append(win_loss)
                            else:
                                team1, score1, team2, score2, mis = match1.groups()
                                score1, score2 = int(score1), int(score2)
                                if cols_pitch[6] == team1:
                                    opponent = team2
                                    win_loss = 'W' if score1 > score2 else 'L'
                                elif cols_pitch[6] == team2:
                                    opponent = team1
                                    win_loss = 'W' if score2 > score1 else 'L'
                                else:
                                    opponent = '-'
                                    win_loss = '-'
                                cols_pitch.append(opponent)
                                cols_pitch.append(win_loss)
                        headers_pitch[0] = 'Date'
                        player_data_pitch = dict(zip(headers_pitch, cols_pitch))
                        match_data_pitch.append(player_data_pitch)
                
                # Append match data to the matches data list
                matches_data.append({
                    'batting': {
                        'headers': headers_bat,
                        'data': match_data_bat
                    },
                    'pitching': {
                        'headers': headers_pitch,
                        'data': match_data_pitch
                    }
                })
            # Function to write match data to a worksheet
            def write_match_data(ws_id, match_data,headers):
                batch_requests = []
                # Append header row
                current_date = (datetime.now() - timedelta(days=1)).strftime('%d %b %Y')
                team_data = []
                for row in match_data:
                    if row['Name'] == 'Totals':
                        for player in team_data:
                       
                          batch_requests.append({
                                'appendCells': {
                                    'sheetId': ws_id,
                                    'rows': [{
                                        'values': [{'userEnteredValue': {'stringValue':  current_date }}] + [{'userEnteredValue': {'stringValue': player.get(header, '')}} for header in headers[1:]]
                                    }],
                                    'fields': 'userEnteredValue'
                                }
                            })
                        

                        team_data = []
                    else:
                        team_data.append(row)
                        
                service.spreadsheets().batchUpdate(spreadsheetId=spreadsheet_id, body={'requests': batch_requests}).execute()

            # Add worksheets for Batting and Pitching
            def add_worksheet(title):
                requests = [{
                    'addSheet': {
                        'properties': {
                            'title': title,
                        }
                    }
                }]
                response = service.spreadsheets().batchUpdate(spreadsheetId=spreadsheet_id, body={'requests': requests}).execute()
                return response['replies'][0]['addSheet']['properties']['sheetId']
            # Write data to the sheets
            for match in matches_data:
                write_match_data('1055982659', match['batting']['data'],match['batting']['headers'])
                write_match_data('423310817', match['pitching']['data'],match['pitching']['headers'])

        return spreadsheet_id

    except HttpError as error:
        print(f"An error occurred: {error}")
        return error

if __name__ == "__main__":
    main()
