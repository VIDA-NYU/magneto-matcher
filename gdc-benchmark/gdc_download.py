import json
import os
import requests
import pandas as pd


with open('papers_info.json', 'r') as file:
    papers_info = json.load(file)


data_folder = 'data'
download_folder = os.path.join(data_folder, 'downloads')
prepared_folder = os.path.join(data_folder, 'input-tables')
os.makedirs(download_folder, exist_ok=True)
os.makedirs(prepared_folder, exist_ok=True)


def extract_csv_from_excel(excel_file_name, sheet_name):
    try:
        df = pd.read_excel(excel_file_name, sheet_name=sheet_name)
        return df
    except Exception as e:
        print(f"Error extracting sheet {sheet_name} from {excel_file_name}: {str(e)}")
        return None


for paper in papers_info:
    print(f"Processing {paper}:")
    dataset_url = papers_info[paper]['Dataset URL']
    if dataset_url:
        response = requests.get(dataset_url)
        if response.status_code == 200:
            download_file_name = os.path.join(
                download_folder, os.path.basename(dataset_url))
            with open(download_file_name, 'wb') as f:
                f.write(response.content)

            print(f"Downloaded {dataset_url} to {download_file_name}")

            if download_file_name.endswith('.xlsx'):
                sheet_name = papers_info[paper]['Sheet Name']

                df = extract_csv_from_excel(download_file_name, sheet_name)

                if paper == "Vasaikar.csv":
                    # remove incompatible rows in Vasaikar dataset
                    df = df.iloc[1:-1]

                if paper == "McDermott.csv":
                    # remove tab characters from column names
                    df.rename(columns={
                        "Age in Months at Time of Tissue Procurement \t": "Age in Months at Time of Tissue Procurement",
                    }, inplace=True)

                if paper == "Clark.csv":
                    # fix typo in values "Whte" to "White" in column Ethnicity_Self_Identify
                    if 'Ethnicity_Self_Identify' not in df.columns:
                        raise ValueError(f'Expected column Ethnicity_Self_Identify but not found in table from paper {paper}')
                    df['Ethnicity_Self_Identify'] = df['Ethnicity_Self_Identify'].replace("Whte", "White")

                if paper == "Wang.csv":
                    # clean values in column "secondhand_smoke_exposure"
                    df['secondhand_smoke_exposure'] = df['secondhand_smoke_exposure'].replace("No or minimal exposure to secondhand smoke", "No")
                    df['secondhand_smoke_exposure'] = df['secondhand_smoke_exposure'].replace("Exposed in childhood houshold", "Yes")
                    df['secondhand_smoke_exposure'] = df['secondhand_smoke_exposure'].replace("Exposed in current household", "Yes")

                if df is not None:
                    csv_file_name = os.path.join(prepared_folder, paper)
                    df.to_csv(csv_file_name, index=False)
                    print(f"Created CSV file: {csv_file_name}")
        else:
            print(f"Failed to download {dataset_url}")
    print("")