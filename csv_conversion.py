import csv
import argparse
import re


def main():
    args = parse_arguments()
    sentences = parse_CSV(args.input_csv)
    write_list_to_text(sentences, args.output_txt)

    return

#Parse args; determine input csv and output text file
def parse_arguments():
    parser = argparse.ArgumentParser(description="a script to do stuff")
    parser.add_argument('-i', '--input_csv', type=str, required=True, help='Input CSV file')
    parser.add_argument('-o', '--output_txt', type=str, required=True, help='Output text file')
    
    args = parser.parse_args()
    return args

#Open, parse, return CSV object
def parse_CSV(input_csv):
    # Notable rows to include in info:    
    '''
    Actual cols, do -1 for access:
    name        2
    tot price   11
    appt date   14
    vehicle     48 
    glasstyp    51
    part#       52
    tot cost    54
    '''
    with open(input_csv, 'r') as csvfile:
        reader = csv.reader(csvfile)
        sentences = []

        # Skip the header row
        next(reader)
        
        # Iterate through rows of completed installations
        for row in reader:
            # Only collecting completed jobs for now
            if row[6] != "InstallationComplete":
                continue
            # Take out any rows that have NULL in the spots we need
            if any(val == "NULL" for val in (row[1], row[47], row[10], row[13], row[53], row[51])):
                continue

            # Separate text from glass type since they're one word
            separated_text = re.sub(r"([A-Z])", r" \1", row[50]).strip()

            # Convert job info into a readable sentence
            sentence  = (
                f"{row[1]} booked a {separated_text} replacement on a {row[47]} for a price of ${row[10]} on "
                f"{row[13]}. Our total cost was {row[53]} and the NAGS part number is {row[51]}"
            )
            sentences.append(sentence)
    
    return sentences

#Create text file, read csv data into file
def write_list_to_text(sentences, filename):
    with open(filename, "w") as f:
        for sentance in sentences:
            f.write(sentance + '\n')
    return

if __name__ == "__main__":
    main()
