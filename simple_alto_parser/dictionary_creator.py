import csv

def from_geonames(csv_file_path):
    # Open Tsv
    with open(csv_file_path, encoding='utf-8') as f:
        csv_reader = csv.reader(f, delimiter='\t')
        row_id = 0
        for row in csv_reader:
            if row[6] == 'P':
                print(
                    row[0],  # geonames_id
                    row[1],  # name
                    row[2],  # asciiname
                    row[3],  # alternatenames
                    row[4],  # latitude
                    row[5],  # longitude
                    row[6],  # feature_class
                    row[7],  # feature_code
                    row[8],  # country_code
                    row[9],  # cc2
                    row[10],  # admin1_code
                    row[11],  # admin2_code
                    row[12],  # admin3_code
                    row[13],  # admin4_code
                    row[14],  # population
                    row[15],  # elevation
                    row[16],  # dem
                    row[17],  # timezone
                    row[18]  # modification_date
                )


            row_id += 1
            if row_id > 20:
                break


from_geonames('../assets/dicts/CH.tsv')