import argparse

EXCLUDE_SYMBOLS = {"IDOK", "IDCANCEL", "IDC_STATIC"}
NEW_SYMBOL_VALUE = -1

#Main
def main():
    args = get_args()
    
    #print(dest_resource_names) #works

    (dialogbox_lines, margins_lines, dlginit_lines, layout_lines) = extract_sections(args)
    
    src_symbols = extract_section_symbols(dialogbox_lines, margins_lines, dlginit_lines, layout_lines) #get all the new symbols to be added for the dialog
    dest_symbols = extract_all_resources(args.dest_h) #get all existing resources in the target for pasting resource file

    new_symbols = extract_new_symbols(src_symbols, dest_symbols)

    inject_new_symbols(args.dest_h, new_symbols)
    

def get_args():
    parser = argparse.ArgumentParser()
    #parser.add_argument("src_h", type=str)
    parser.add_argument("dlg", type=str, help="Enter the ID of the dialog (ex: IDD_JOBCONTROL)")
    parser.add_argument("src_rc", type=str, help="Enter the source .rc file")
    parser.add_argument("dest_h", type=str, help="Enter the destination resource.h file")
    parser.add_argument("dest_rc", type=str, help="Enter the destination .rc file")
    return parser.parse_args()

#For extracting from the source file

def extract_sections(args):


    #define modes
    NONE = 0
    DIALOGBOX = 1
    MARGINS = 2
    DLGINIT = 3
    LAYOUT = 4

    #other constants
    MARGIN_TAB = "    "

    #local vars
    dialogbox_lines = []
    margins_lines = []
    dlginit_lines = []
    layout_lines = []

    mode = NONE
    src_rc_file = open(args.src_rc, 'r')
    for raw_line in src_rc_file:
        line = raw_line
        if (raw_line[-1] == '\n'):
            line = raw_line[:-1]
        #print(line)

        if (mode == NONE):
            vals = line.split(' ')
            if vals[0] == args.dlg and vals[1] == "DIALOGEX":
                mode = DIALOGBOX #note no break, it will run the next line
                #print("Starting Dlgbox")
            elif line == (MARGIN_TAB + args.dlg + ", DIALOG"):
                mode = MARGINS
                #print("Starting margins")
            elif vals[0] == args.dlg and vals[1] == "DLGINIT":
                mode = DLGINIT
                #print("Starting dlginit")
            elif vals[0] == args.dlg and vals[1] == "AFX_DIALOG_LAYOUT":
                mode = LAYOUT
                #print("Starting layout")

        if (mode == DIALOGBOX):
            dialogbox_lines.append(line) #add line to the dialog box
            if line == "END": #note this includes indentation, it cannot be indented so that it is not an internal end, must be bottom level end
                mode = NONE
                print("Found Dialogbox")
                continue 
        elif (mode == MARGINS):
            margins_lines.append(line)
            if line == MARGIN_TAB + "END":
                mode = NONE
                print("Found margins")
                continue
        elif (mode == DLGINIT):
            dlginit_lines.append(line)
            if (line == "END"):
                mode = NONE
                print("Found dlginit")
                continue
        elif (mode == LAYOUT):
            layout_lines.append(line)
            if (line == "END"):
                mode = NONE
                print("Found layout")
                continue
    return (dialogbox_lines, margins_lines, dlginit_lines, layout_lines)

def extract_section_symbols(*sections):
    symbols = set()
    for section in sections:
        for symbol in extract_symbols(section):
            symbols.add(symbol)
      
    return symbols

def extract_symbols(lines):
    symbols = set()
    for line in lines:
        
        for term in line.replace(',', ' ').split(' '):
            if term[:3] == "IDC": #all resource ID's start with IDC
                symbols.add(term)  
    return symbols 


def extract_all_resources(resources_file):
    resource_names = set()
    #resource_ids = {} #map name to id
    with open(resources_file, 'r') as f:
        for line in f:
            vals = line.split(' ') #split along space
            if len(vals)>2 and len(vals[0]) > 0 and vals[0] == "#define":
                resource_names.add(vals[1]) #term 0 is #define, term1 is the ID, term2 is the numarical value
                #resource_ids[vals[1]] = int(vals[2]) #save the actual ID, not sure if we will need this
    return resource_names

def extract_new_symbols(src_symbols, dest_symbols):
    new_symbols = []
    for symbol in src_symbols:
        if not (symbol in EXCLUDE_SYMBOLS) and not (symbol in dest_symbols):#check if it is actually a new symbol or if it already exists
            new_symbols.append(symbol)
            #print(symbol)
    print("\nDialog Symbols=%d\nExisting Target Symbols=%d\nNew Target Symbols=%d" % (len(src_symbols), len(dest_symbols), len(new_symbols)))
    return new_symbols

def inject_new_symbols(resource_file, symbols):

    with open(resource_file, 'r') as f:
        contents = f.readlines()
    
    first_def_line = -1
    DEFINE = "#define"
    for i in range(len(contents)):
        if contents[i][0:len(DEFINE)] == DEFINE:
            first_def_line = i
            break

    print("\nInjecting symbols at line: " + str(first_def_line) + " with value = " + str(NEW_SYMBOL_VALUE))


if __name__ == "__main__":
    main()