import csv

header = ["user_id", "user_name", "goodkpt", "kusa", "wwww"]

aggregate_file = "result.csv"
minify_file = "result2.csv"

with open(aggregate_file, 'r') as input_csv:
    csvreader = csv.reader(input_csv)
    input_header = next(csvreader)
    goodkpt_index = input_header.index("goodkpt")
    kusa_index = input_header.index("kusa")
    wwww_index = input_header.index("wwww")
    with open(minify_file, 'w') as output_csv:
        csvwriter = csv.writer(output_csv)
        csvwriter.writerow(header)

        for row in csvreader:
            goodkpt = row[goodkpt_index]
            kusa = row[kusa_index]
            wwww = row[wwww_index]

            csvwriter.writerow([row[0], row[1], row[goodkpt_index], row[kusa_index], row[wwww_index]])
